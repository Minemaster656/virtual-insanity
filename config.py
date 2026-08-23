from ollama import Client
from platformdirs import PlatformDirs
import logging

dirs = PlatformDirs("VirtualInsanity", "SoftwareUndefined", ensure_exists=True)

client = Client()
MODEL = "gemma4:e4b-it-qat"
CHARACTER_MAX_ITERATIONS = 32

logging.basicConfig(
    level=logging.INFO,
    filename="app.log",  # только файл
    filemode="a",  # добавление (или 'w' для перезаписи)
    format="%(asctime)s - %(levelname)s - %(message)s",
)
