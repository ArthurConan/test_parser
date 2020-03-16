import pathlib
import os

BASE_DIR = pathlib.Path(__file__).parent.parent
TEMPLATES_DIR = str(BASE_DIR / 'templates')

HOST = os.getenv('HOST', 'localhost')
PORT = os.getenv('PORT', 8000)

REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_NAMESPACE = {
    "base": 1
}
REDIS_URL = f'redis://redis:{REDIS_PORT}/{REDIS_NAMESPACE.get("base")}'

BASE_URL = 'https://clientsapi{}.bkfon-resource.ru/results/results.json.php?locale=en'
