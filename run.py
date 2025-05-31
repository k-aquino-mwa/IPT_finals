import os
from app import create_app
from config import config

config_name = os.getenv('FLASK_CONFIG', 'default')

app = create_app(config[config_name])

if __name__ == '__main__':
    app.run(
        host=config[config_name].HOST, 
        port=config[config_name].PORT, 
        debug=config[config_name].DEBUG
    )