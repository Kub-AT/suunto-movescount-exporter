import datetime
import os

from .scraper import Movescount

SAVE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'activities')


def export(login: str, password: str, date_from: datetime.datetime, date_to: datetime.datetime, formats: list) -> None:
    service = Movescount(formats, login=login, password=password)
    for activity in service.fetch_moves(date_from, date_to):
        print(activity)
        service.export(activity, SAVE_PATH)
    return
