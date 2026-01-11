from utils import url_encode_path_part


CATAAS_BASE_URL = "https://cataas.com"


def build_cat_image_url(text: str, width: int = 600, height: int = 400) -> str:
    encoded_text = url_encode_path_part(text)
    return f"{CATAAS_BASE_URL}/cat/says/{encoded_text}?width={width}&height={height}"
