from flask import Flask

app = Flask(__name__)


class BaseConfig(object):
    DEBUG = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./test.db'
    SECRET_KEY = 'iamthekeytothistokenthatiwantyoutouse'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'iamthekeytothistokenthatiwantyoutouse'
    BASE_URL= "http://127.0.0.1:5000/v1"


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./test.db'
    DEBUG = True
    SECRET_KEY = 'iamthekeytothistokenthatiwantyoutouse'


class StagingConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = 'iamthekeytothistokenthatiwantyoutouse'


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'iamthekeytothistokenthatiwantyoutouse'


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}

# if __name__ == "__main__":
#     app.run(debug=True)

