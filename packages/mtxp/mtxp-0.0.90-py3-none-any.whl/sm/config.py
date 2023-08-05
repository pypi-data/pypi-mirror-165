import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:  # 基本配置类
    SECRET_KEY = os.getenv(
        "SM_SECRET_KEY", '$kackYeECz)aprJksfs^s@L8YadsS$m702RlksfF7EF8etDFrj;)$AST_^&0DwAa#j23oKEL9q(@#dJKw')
    API_PREFIX = os.environ.get("SM_API_PREFIX", "/smapi")
    HTML_ROOT_DIR = os.environ.get("SM_HTML_ROOT", "/var/www/html")


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(BaseConfig):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
