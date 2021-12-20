from framework.utils.config_reader import ConfigReader


class DataReader:
    __data = None

    @staticmethod
    def read_data():
        if not DataReader.__data:
            DataReader.__data = ConfigReader().get_test_data_by_env()
        return DataReader.__data

    @staticmethod
    def get_data(item):
        return DataReader.read_data()['data'][item]

    @staticmethod
    def get_user(user):
        return DataReader.read_data()['users'][user]
