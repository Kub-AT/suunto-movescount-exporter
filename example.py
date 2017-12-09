import datetime
from movescount import export


if __name__ == '__main__':
    login, password = None, None
    date_from = datetime.datetime(2017, 12, 1)
    date_to = datetime.datetime.now()
    assert login and password, 'Set login and password to run an example'
    export(login, password, date_from, date_to, ['fit', 'gpx'])
