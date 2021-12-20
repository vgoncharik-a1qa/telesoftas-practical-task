import os
from pathlib import Path

from configuration import config
from framework.utils.json_reader import JSONReader


class ConfigReader:
    def get_env(self):
        return os.getenv('ENV', config.ENV)

    def get_browser(self):
        return os.getenv('BROWSER', config.BROWSER)

    def is_remote(self):
        return os.getenv('REMOTE', config.REMOTE).lower() in ("yes", "true", "t", "1")

    def get_remote_url(self):
        return os.getenv('REMOTE_URL', config.REMOTE_URL)

    def is_headless(self):
        return os.getenv('HEADLESS', config.HEADLESS).lower() in ("yes", "true", "t", "1")

    def get_config_by_env(self):
        return JSONReader.read(PathProvider.get_config_path(self.get_env()))

    def get_test_data_by_env(self):
        return JSONReader.read(PathProvider.get_test_data_path('dev' if self.get_env() in ['prod'] else self.get_env()))

    def get_host_url(self):
        return self.get_config_by_env()['host_url']


class PathProvider:
    @staticmethod
    def get_project_path():
        return Path(__file__).parent.parent.parent

    @staticmethod
    def get_env_base_path(environment):
        return Path(PathProvider.get_project_path(), 'configuration', 'environments', environment)

    @staticmethod
    def get_config_path(environment):
        return Path(PathProvider.get_env_base_path(environment), 'config.json')

    @staticmethod
    def get_test_data_path(environment):
        return Path(PathProvider.get_env_base_path(environment), 'test_data.json')

    @staticmethod
    def get_logging_conf_path():
        return Path(PathProvider.get_project_path(), 'configuration', 'logging.json')

    @staticmethod
    def get_temp_dir():
        return Path(PathProvider.get_project_path(), 'temp')

    @staticmethod
    def get_screenshots_path():
        return Path(PathProvider.get_temp_dir(), 'screenshots')
