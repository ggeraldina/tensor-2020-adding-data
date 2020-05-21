""" Создание коллекций БД """
from pymongo.write_concern import WriteConcern

from server import MONGO


def create_collections():
    """ Создать коллекции БД """
    # Необходимо создать коллекции заранее,
    # чтобы можно было использовать транзакции.
    # Актуально только для MongoDB версии 4.2
    wc_majority = WriteConcern(w="majority", wtimeout=1000)
    collections = ["counter", "event", "ticket", "booking"]
    for collection in collections:
        if not collection in MONGO.db.collection_names():
            MONGO.db.create_collection(collection, write_concern=wc_majority)
    MONGO.db.event.create_index("start_time")
