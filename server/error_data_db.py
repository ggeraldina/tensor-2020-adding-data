""" Исключение при взаимодействии с БД"""
from datetime import datetime


class ErrorDataDB(Exception):
    """ Исключение при использовании некорректных данных """

    def __init__(self, message):
        super(ErrorDataDB, self).__init__(message)
        self.message = message
        print("INFO: Exception ErrorDataDB.\n\t{}\n\t{}".format(
            datetime.utcnow().isoformat(),
            message
        ))

    def __str__(self):
        return str(self.message)
