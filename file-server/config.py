class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = '/server_files'
    JSON_SORT_KEYS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:2458173671@postgres:5432/file_server'

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:2458173671@postgres:5432/file_server'