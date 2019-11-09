import os
import configparser
from os import environ
from smart_emails.constants import Constants


class ConfigAccessor:
    configParser = None

    def __init__(self):
        self.configParser = configparser.ConfigParser()
        if not self.configParser.read(Constants.instance().config_file_path):
            self.create_config_file_if_doesnt_exist()
        self.configParser.read(Constants.instance().config_file_path)

    def get(self, key: str) -> str:
        env_key = 'SMART_EMAILS__' + key
        if env_key in os.environ:
            return environ.get(env_key)

        key_parts = key.split('__')
        config_value = self.configParser
        for key_part in key_parts:
            config_value = config_value[key_part]
        return config_value

    def get_boolean(self, key: str) -> bool:
        str_value = self.get(key)
        if str_value.lower() in ("yes", "true", "t", "1"):
            return True
        return False

    @staticmethod
    def create_config_file_if_doesnt_exist() -> None:
        if os.path.exists(Constants.instance().config_file_path):
            return

        with open(Constants.instance().config_file_path, 'w+') as configfile:
            config = configparser.ConfigParser()
            config['MAIL'] = {
                'SERVER': 'smtp.gmail.com',
                'PORT': 465,
                'USE_TLS': False,
                'USE_SSL': True,
                'USERNAME': 'username@gmail.com',
                'PASSWORD': 'password',
                'FROM': 'username@gmail.com',
                'TO': 'username@gmail.com'
            }
            config.write(configfile)
