import logging.config

from framework.utils.json_reader import JSONReader
from framework.utils.config_reader import PathProvider
from framework.constants import logger


class Logger(object):
    __logger = None

    @staticmethod
    def get_logger():
        if not Logger.__logger:
            logging.setLoggerClass(CustomLogger)
            json_config = JSONReader.read(PathProvider.get_logging_conf_path())
            logging.config.dictConfig(json_config)
            Logger.__logger = logging.getLogger('web_tests')
        return Logger.__logger


class CustomLogger(logging.Logger):

    def step(self, message):
        msg = logger.STEP_TEMPLATE.format(message)
        self.info(msg=msg)

    def test_name(self, message):
        msg = logger.TEST_NAME_TEMPLATE.format(message)
        self.info(msg=msg)
