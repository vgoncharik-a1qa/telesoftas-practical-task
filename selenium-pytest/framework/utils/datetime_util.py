from datetime import datetime


class DatetimeUtil:

    @staticmethod
    def get_str_datetime(exp_format):
        return datetime.now().strftime(exp_format)
