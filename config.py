from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv()


class Config(object):
    DEBUG = False
    TESTING = False
    FLASK_DEBUG = 1
    LOG_TO_STDOUT = environ.get('LOG_TO_STDOUT', False)


class DevelopmentConfig(Config):
    load_dotenv(path.join(basedir, 'dev.env'))
    MYSQL_HOST = environ["MYSQL_HOST"]
    MYSQL_USER_NAME = environ["MYSQL_USER_NAME"]
    MYSQL_PASSWORD = environ["MYSQL_PASSWORD"]
    MYSQL_DATABASE_NAME = environ["MYSQL_DATABASE_NAME"]
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{MYSQL_USER_NAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE_NAME}"
    MAIL_SERVER = environ["MAIL_SERVER"]
    MAIL_PORT = environ["MAIL_PORT"]
    MAIL_USERNAME = environ["MAIL_USERNAME"]
    MAIL_PASSWORD = environ["MAIL_PASSWORD"]
    MAIL_DEFAULT_SENDER = environ["MAIL_DEFAULT_SENDER"]
    MAIL_USE_TLS = environ.get('MAIL_USE_TLS', False)
    MAIL_USE_SSL = environ.get('MAIL_USE_SSL', True)
    SESSION_TIMEOUT = environ.get('SESSION_TIMEOUT', 5)
    DEBUG = True


class ProductionConfig(Config):
    load_dotenv(path.join(basedir, 'prod.env'))


config_data = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

config_name = environ.get('APP_CONFIG', 'development')
config = config_data[config_name]
