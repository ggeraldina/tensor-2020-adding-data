""" Функции для выполнения транзакций и коммитов """
import functools

from pymongo.errors import ConnectionFailure, OperationFailure
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import ReadPreference
from pymongo.write_concern import WriteConcern

from .error_data_db import ErrorDataDB


# Транзакции будут работать только с replica set серверами
# и не будут с автономным (standalone) сервером
# https://jira.mongodb.org/browse/CSHARP-2907
#
# Это значит, что транзакции будут работать с MongoDB Atlas,
# т.к. там уже все настроено как replica set;
# и, скорее всего, не будут работать с MongoDB на localhost,
# т.к. localhost без соответствующей настройки - это standalone.
#
# Для standalone при попытке использования транзакций
# выбрасывается исключение OperationFailure с советом
# использовать retryWrites=False, но это не поможет в данном случае.
#
# Для работы транзакций необходима конвертация сервера в replica set
# https://docs.mongodb.com/manual/tutorial/convert-standalone-to-replica-set/
def run_transaction_with_retry(txn_func):
    """ Транзакция txn_func с возможность повторной попытки при неудаче """
    @functools.wraps(txn_func)
    def wrapper(session, *args, **kwargs):
        while True:
            try:
                with session.start_transaction(
                    read_concern=ReadConcern(level="snapshot"),
                    write_concern=WriteConcern(w="majority"),
                    read_preference=ReadPreference.PRIMARY
                ):
                    # Транзакция успешно завершилась commit'ом
                    # и функция успешно вернула результат
                    return txn_func(session, *args, **kwargs)
            except (ConnectionFailure, OperationFailure) as ex:
                if ex.has_error_label("TransientTransactionError"):
                    print(
                        "INFO: TransientTransactionError,"
                        "повторная попытка транзакции ..."
                    )
                    continue
                raise ErrorDataDB("O.o Что-то страшное при попытке транзакции")
    return wrapper


def commit_with_retry(session):
    """ Commit транзакции """
    while True:
        try:
            session.commit_transaction()
            print("INFO: Transaction committed.")
            break
        except (ConnectionFailure, OperationFailure) as ex:
            if ex.has_error_label("UnknownTransactionCommitResult"):
                print(
                    "INFO: UnknownTransactionCommitResult,"
                    "повторная попытка commit операции ..."
                )
                continue
            raise ErrorDataDB("O.o Ошибка во время commit транзакции")
