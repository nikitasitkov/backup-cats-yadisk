import time
from typing import Dict

import requests


YADISK_API_BASE = "https://cloud-api.yandex.net/v1/disk"


class YaDiskClient:

    def __init__(self, token: str, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"OAuth {token}",
                "Accept": "application/json",
            }
        )

    def create_folder(self, folder_path: str) -> None:
        url = f"{YADISK_API_BASE}/resources"
        params = {"path": folder_path}

        resp = self.session.put(url, params=params, timeout=self.timeout)

        if resp.status_code in (201, 409):
            return

        if resp.status_code in (401, 403):
            raise RuntimeError(
                "Ошибка доступа к Яндекс.Диску. Проверь OAuth-токен (401/403). "
                f"Ответ: {resp.text}"
            )

        raise RuntimeError(
            f"Не удалось создать папку. HTTP {resp.status_code}: {resp.text}"
        )

    def upload_by_url(self, source_url: str, dest_path: str, overwrite: bool = True) -> str:
        url = f"{YADISK_API_BASE}/resources/upload"
        params = {
            "path": dest_path,
            "url": source_url,
            "overwrite": "true" if overwrite else "false",
        }

        resp = self.session.post(url, params=params, timeout=self.timeout)

        if resp.status_code == 401 or resp.status_code == 403:
            raise RuntimeError(
                "Ошибка доступа к Яндекс.Диску. Проверь OAuth-токен (401/403). "
                f"Ответ: {resp.text}"
            )

        if resp.status_code != 202:
            raise RuntimeError(
                f"Не удалось запустить загрузку по URL. HTTP {resp.status_code}: {resp.text}"
            )

        data = resp.json()
        href = data.get("href")
        if not href:
            raise RuntimeError(f"Ответ без href: {data}")

        return href

    def wait_operation(
            self, operation_href: str, poll_interval: float = 1.0, max_wait: int = 120
    ) -> None:
        start = time.time()

        while True:
            resp = self.session.get(operation_href, timeout=self.timeout)
            if resp.status_code != 200:
                raise RuntimeError(
                    f"Не удалось проверить операцию. HTTP {resp.status_code}: {resp.text}"
                )

            data = resp.json()
            status = data.get("status")

            if status == "success":
                return

            if status == "failed":
                raise RuntimeError(f"Операция завершилась с ошибкой: {data}")

            if time.time() - start > max_wait:
                raise TimeoutError("Операция загрузки слишком долго выполняется (таймаут).")

            time.sleep(poll_interval)

    def get_resource_meta(self, path: str) -> Dict:
        url = f"{YADISK_API_BASE}/resources"
        params = {"path": path, "fields": "name,path,size,type"}

        resp = self.session.get(url, params=params, timeout=self.timeout)

        if resp.status_code in (401, 403):
            raise RuntimeError(
                "Ошибка доступа к Яндекс.Диску. Проверь OAuth-токен (401/403). "
                f"Ответ: {resp.text}"
            )

        if resp.status_code != 200:
            raise RuntimeError(
                f"Не удалось получить метаданные. HTTP {resp.status_code}: {resp.text}"
            )

        return resp.json()
