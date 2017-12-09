import datetime
import json
import os

import arrow
import requests

from .models import MoveActivity


class Movescount:
    AVAILABLE_FORMATS = ['gpx', 'kml', 'fit', 'tcx', 'xlsx']
    USER_AGENT = ('Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 '
                  'Safari/537.36 ')

    class Urls:
        LOGIN = 'https://servicegate.suunto.com/UserAuthorityService/'
        TOKEN = 'https://www.movescount.com/services/UserAuthenticated'
        OVERVIEW = 'http://www.movescount.com/overview'
        EXPORT = 'http://www.movescount.com/move/export'

    def __init__(self, formats: list, **settings):
        assert len(list(set(formats) & set(self.AVAILABLE_FORMATS))) == len(formats)
        session = requests.Session()
        session.headers['User-Agent'] = self.USER_AGENT

        self.formats = formats
        self.session = session
        self.settings = settings

    def _login(self):
        response = self.session.get(self.Urls.LOGIN, params={
            'service': 'Movescount',
            'emailAddress': self.settings.get('login'),
            'password': self.settings.get('password'),
        })
        response.raise_for_status()
        response = self.session.post(self.Urls.TOKEN, json={
            'token': response.text[1:-1],
            'utcOffset': '60',
            'redirectUri': '/overview',
        })
        response.raise_for_status()

    def fetch_moves(self, date_from: datetime.datetime, date_to: datetime.datetime):
        self._login()
        response = self.session.get(self.Urls.OVERVIEW)
        response.raise_for_status()
        data = response.text.split('mc.OverviewPage.default.main(')[1].split(');')[0]

        config = json.loads(data)
        user_id = config['activityFeed']['targetUserID']
        api_base_url = config['config']['activityRecordsData']['activityRecordsBaseUrl']
        api_token = config['config']['activityRecordsData']['token']
        response = self.session.get(f'{api_base_url}/moves/getmoves', headers={'authorization': api_token}, params={
            'startDateString': arrow.get(date_from).floor('day').isoformat().replace('+00:00', 'Z'),
            'endDateString': arrow.get(date_to).ceil('day').isoformat().replace('+00:00', 'Z'),
            'userId': user_id
        })
        response.raise_for_status()
        return [MoveActivity(move) for move in response.json()['Moves']]

    def export(self, activity: MoveActivity, path: str):
        for _format in self.formats:
            self._export_single(activity, path, _format)

    def _export_single(self, activity: MoveActivity, path: str, _format: str):
        resp = self.session.get(self.Urls.EXPORT, params={
            'id': activity.id,
            'format': _format
        })
        resp.raise_for_status()
        time = activity.time.format('YYYY-MM-DD HH:mm:ss')
        path = os.path.join(path, f'{activity.id}-{time}.{_format}')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(resp.content)
        return path
