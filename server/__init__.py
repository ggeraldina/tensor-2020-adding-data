""" Билетная касса театра """
import os
from datetime import datetime
import threading

from bson import ObjectId
from flask import Flask, jsonify, request, send_from_directory
from flask_pymongo import PyMongo

from .transaction import commit_with_retry, run_transaction_with_retry
from .error_data_db import ErrorDataDB

APP = Flask(__name__, static_folder="../client")
APP.config["JSON_AS_ASCII"] = False
APP.config["MONGO_URI"] = os.environ["MONGO_URI"]
MONGO = PyMongo(APP)

from .database import create_collections
create_collections()

@APP.route("/", methods=["GET", "POST"])
@APP.route("/index", methods=["GET", "POST"])
def add_new_event():
    """ Добавление мероприятия.

    Для добавления только хороших данных. (Временное решение)
    Время - строка в ISO-формате
    """
    if request.method == "POST":
        try:
            event, price, color = parse_data()        
            thread = threading.Thread(target=add_event_data, args=(event, price, color))
            thread.daemon = True
            thread.start()
        except ErrorDataDB as error_db:
            return jsonify({"message": error_db.message})            
        except Exception:
            return jsonify({"message": "Ошибка при добавлении данных"}) 

        return jsonify({"message": "Данные добавляются в фоновом режиме. Это занимает пару минут"})

    return send_from_directory(APP.static_folder, "index.html")

def parse_data():
    try:
        event = {
            "title": request.form.get("title"),
            "author": request.form.get("author"),
            "photo": request.form.get("photo"),
            "start_time": datetime.fromisoformat(request.form.get("start_time")),
            "end_time": datetime.fromisoformat(request.form.get("end_time")),
            "description": request.form.get("description"),
            "director": request.form.get("director"),
            "actors": request.form.get("actors")
        }
        price = {
            "1-3": float(request.form.get("price_1-3")) if request.form.get("price_1-3") != "" else 800,
            "4-5": float(request.form.get("price_4-5")) if request.form.get("price_4-5") != "" else 1000,
            "6-8": float(request.form.get("price_6-8")) if request.form.get("price_6-8") != "" else 1500,
            "9-10": float(request.form.get("price_9-10")) if request.form.get("price_9-10") != "" else 1200,
            "11-13": float(request.form.get("price_11-13")) if request.form.get("price_11-13") != "" else 900
        }
        color = {
            "1-3": request.form.get("color_1-3") if request.form.get("color_1-3") != "" else "#9497ff",
            "4-5": request.form.get("color_4-5") if request.form.get("color_4-5") != "" else "#86fcbd",
            "6-8": request.form.get("color_6-8") if request.form.get("color_6-8") != "" else "#f0fc62",
            "9-10": request.form.get("color_9-10") if request.form.get("color_9-10") != "" else "#ffcf70",
            "11-13": request.form.get("color_11-13") if request.form.get("color_11-13") != "" else "#ffa570"
        }
    except Exception:
        raise ErrorDataDB("Ошибка при парсинге данных") 
    return event, price, color     


def add_event_data(event, price, color):
    with MONGO.cx.start_session() as session:    
        txn_add_event(session, event, price, color)


@run_transaction_with_retry
def txn_add_event(session, event, price, color):
    event["_id"] = get_next_id("event", session=session)
    MONGO.db.event.insert_one(event, session=session)    
    add_tickets(event["_id"], price, color, session=session)
    commit_with_retry(session)
    return True


def get_next_id(collection_name, session=None):
    """ Получить следующий идентификатор """
    result = MONGO.db.counter.find_one_and_update(
        filter={"_id": collection_name},
        update={"$inc": {"count": 1}},
        upsert=True,
        new=True,
        session=session
    )
    # ObjectId - 24-character hex string
    return ObjectId(str(result["count"]).zfill(24))


def add_tickets(id_event, price, color, session=None):
    """ Добавление билетов """
    for i in range(1, 14):
        for j in range(1, 22):
            ticket = {
                "_id": get_next_id("ticket", session=session),
                "row": i,
                "seat": j,
                "event": id_event,
                "is_booked": False
            }
            if i <= 3:
                ticket["price"] = price["1-3"]
                ticket["color_zone"] = color["1-3"]
            elif 3 < i <= 5:
                ticket["price"] = price["4-5"]
                ticket["color_zone"] = color["4-5"]
            elif 5 < i <= 8:
                ticket["price"] = price["6-8"]
                ticket["color_zone"] = color["6-8"]
            elif 8 < i <= 10:
                ticket["price"] = price["9-10"]
                ticket["color_zone"] = color["9-10"]
            else:
                ticket["price"] = price["11-13"]
                ticket["color_zone"] = color["11-13"]
            ticket["_id"] = MONGO.db.ticket.insert_one(ticket, session=session).inserted_id


# @APP.route("/events_list")
# def events_list():
#     """ Mock list events GET """
#     return send_from_directory(APP.static_folder, 'mock_pages/events_list_get_request.html')


# @APP.route("/booking")
# def booking():
#     """ Mock booking POST """
#     return send_from_directory(APP.static_folder, 'mock_pages/booking_post_request.html')


# @APP.route("/event")
# def event():
#     """ Mock event GET """
#     return send_from_directory(APP.static_folder, 'mock_pages/event_get_request.html')


# @APP.route("/bookings_list")
# def bookings_list():
#     """ Mock bookings list GET """
#     return send_from_directory(APP.static_folder, 'mock_pages/bookings_list_get_request.html')


# @APP.route("/cancel_booking_post")
# def cancel_booking_post():
#     """ Mock cancel booking list GET """
#     return send_from_directory(APP.static_folder, 'mock_pages/canceling_booking_post_request.html')
