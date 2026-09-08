import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


def load_config(config_path: Optional[str] = None) -> dict:
    """
    .env faylidagi o'zgaruvchilarni yuklash.
    
    Args:
        config_path: .env fayl joylashuvi (None bo'lsa, hozirgi papkadan qidiradi)
    
    Returns:
        O'zgaruvchilar dict
    """
    if config_path is None:
        config_path = Path(__file__).parent / ".env"
    
    # .env fayl mavjudligini tekshirish
    if os.path.exists(config_path):
        load_dotenv(config_path)
    
    config = {
        "KIMI_API_KEY": os.getenv("KIMI_API_KEY", ""),
        "KIMI_API_URL": os.getenv("KIMI_API_URL", "https://api.kimi.com/v1"),
        "KIMI_MODEL": os.getenv("KIMI_MODEL", "kimi-k2p6"),
        "CHUNK_SIZE": int(os.getenv("CHUNK_SIZE", "15000")),
        "MAX_RETRIES": int(os.getenv("MAX_RETRIES", "3")),
        "TIMEOUT": int(os.getenv("TIMEOUT", "60")),
    }
    
    return config


if __name__ == "__main__":
    cfg = load_config()
    print("Konfiguratsiya:")
    for key, value in cfg.items():
        if key == "KIMI_API_KEY" and value:
            print(f"  {key}: {'*' * len(value)}")
        else:
            print(f"  {key}: {value}")
