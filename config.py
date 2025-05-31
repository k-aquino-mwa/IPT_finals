class Config:
    # Base configuration settings
    SECRET_KEY = 'your_secret_key_here'
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5000

    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Additional configuration options
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = None
    MAIL_PASSWORD = None

    @classmethod
    def init_app(cls, app):
        """
        Initialize application with configuration settings.
        Allows for flexible configuration extension.
        """
        # Set core configurations
        app.config['SECRET_KEY'] = cls.SECRET_KEY
        app.config['DEBUG'] = cls.DEBUG

        # Optional configurations (only set if not None)
        optional_configs = [
            'SQLALCHEMY_DATABASE_URI', 
            'SQLALCHEMY_TRACK_MODIFICATIONS',
            'MAIL_SERVER', 
            'MAIL_PORT', 
            'MAIL_USE_TLS',
            'MAIL_USERNAME', 
            'MAIL_PASSWORD'
        ]

        for config in optional_configs:
            value = getattr(cls, config, None)
            if value is not None:
                app.config[config] = value

        return app

class DevelopmentConfig(Config):
    DEBUG = True
    # Development-specific configurations
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_database.db'

class ProductionConfig(Config):
    DEBUG = False
    # Production-specific configurations
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/proddb'

class TestingConfig(Config):
    TESTING = True
    # Testing-specific configurations
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Mapping of config names to classes
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}