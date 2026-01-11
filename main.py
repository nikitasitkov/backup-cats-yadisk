import json
import logging
from datetime import datetime

from cataas_client import build_cat_image_url
from yadisk_client import YaDiskClient
from utils import sanitize_filename, sanitize_user_text


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

GROUP_FOLDER = "spd-140"


def make_disk_path(folder_name: str) -> str:
    folder_name = folder_name.strip().strip("/")
    return f"disk:/{folder_name}"


def get_the_backup(text: str, token: str, group_folder: str) -> dict:
    yadisk = YaDiskClient(token=token)

    folder_path = make_disk_path(group_folder)
    logging.info("1) Создаю папку на Я.Диске: %s", folder_path)
    yadisk.create_folder(folder_path)

    logging.info("2) Формирую URL кота с текстом (CATAAS)")
    cat_url = build_cat_image_url(text=text)
    logging.info("   URL кота: %s", cat_url)

    safe_name = sanitize_filename(text)
    filename = f"{safe_name}.jpg"

    dest_path = f"{folder_path}/{filename}"
    logging.info("3) Запускаю загрузку на Я.Диск по URL: %s", dest_path)

    operation_href = yadisk.upload_by_url(source_url=cat_url, dest_path=dest_path)
    logging.info("   Операция: %s", operation_href)

    logging.info("4) Жду завершения операции...")
    yadisk.wait_operation(operation_href=operation_href)

    logging.info("5) Получаю метаданные файла (size)")
    meta = yadisk.get_resource_meta(dest_path)
    size = meta.get("size")

    result_item = {
        "file_name": filename,
        "text": text,
        "yadisk_path": dest_path,
        "size_bytes": size,
        "uploaded_at": datetime.now().isoformat(timespec="seconds"),
        "source_url": cat_url,
    }

    return result_item


def save_report_json(items: list, filename: str = "result.json") -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def main() -> None:
    print("=== Курсовая работа: Резервное копирование котиков на Яндекс.Диск ===")

    text_prompt = "Введите текст для картинки (он станет названием файла): "
    token_prompt = "Введите OAuth-токен Яндекс.Диска (из Полигона): "

    text = sanitize_user_text(input(text_prompt))
    token = sanitize_user_text(input(token_prompt))

    group_folder = GROUP_FOLDER
    print(f"Папка группы: {group_folder}")

    if not text:
        raise ValueError("Текст не должен быть пустым.")
    if not token:
        raise ValueError("Токен не должен быть пустым.")

    logging.info("Старт работы...")

    report_items = []
    item = get_the_backup(text=text, token=token, group_folder=group_folder)
    report_items.append(item)

    save_report_json(report_items, filename="result.json")

    logging.info("Готово! Отчет сохранен в result.json")
    print("\n✅ Успешно! Проверь Яндекс.Диск и файл result.json")


if __name__ == "__main__":
    main()
