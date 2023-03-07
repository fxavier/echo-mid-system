from datetime import datetime


class DateConversion:

    @staticmethod
    def convert_str_date(strDate):
        if strDate is None:
            date_str_format = '1900-01-01 00:00:00'
            return datetime.strptime(date_str_format, '%Y-%m-%d %H:%M:%S')
        date_format = str(strDate[0:10]) + ' ' + '00:00:00'
        return datetime.strptime(date_format, '%Y-%m-%d %H:%M:%S')
