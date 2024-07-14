import os

from dotenv import load_dotenv

# TODO: Передать сюда путь до файла .env
load_dotenv()

LOG_LEVEL = os.environ.get("LOG_LEVEL")
FS_LOCAL_PATH = os.environ.get("FS_LOCAL_PATH")
GL_SERVER = os.environ.get("GL_SERVER")
GL_PRIVATE_TOKEN = os.environ.get("GL_PRIVATE_TOKEN")
GL_GROUP_PATH = os.environ.get("GL_GROUP_PATH")
GL_GROUP_ID = os.environ.get("GL_GROUP_ID")
