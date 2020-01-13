import os

SECRET_KEY = 'sd323sdffre$()Dfgddfg'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'postgresql://admin:qwerty@localhost/todo'
JSON_AS_ASCII = False
SQLALCHEMY_ECHO = False
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {"jpg", "png", "doc", "docx", "xls", "xlsx", "mp4", "pdf"}
MAX_CONTENT_LENGTH = 100 * 1024 * 1024 # 16 mb
