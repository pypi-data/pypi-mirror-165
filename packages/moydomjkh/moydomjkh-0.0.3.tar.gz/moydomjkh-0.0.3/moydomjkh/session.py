import json
import logging

from requests import session
from requests.exceptions import Timeout, RequestException

from moydomjkh.exceptions import *

_LOGGER = logging.getLogger(__name__)

_BASE_URL = 'https://newlk.erconline.ru/api/v1'


class Session:
    __session = None

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.token = None

    def __establish(self) -> None:
        self.__session = session()
        try:
            resp = self.__session.post(f'{_BASE_URL}/user/login', json={'login': self.login, 'password': self.password},
                                       headers={'Content-Type': 'application/json'})
        except RequestException as e:
            if isinstance(e, Timeout):
                raise SessionTimeout(e)
            else:
                raise SessionException(e)

        if resp.status_code != 200:
            raise InvalidSession(
                f'Error response. status code: {resp.status_code},'
                f' error details: {json.dumps(resp.json(), ensure_ascii=False)}')

        data = resp.json()
        self.token = data['token']

    def call(self, query, data=None, **kwargs) -> dict:

        _LOGGER.debug(f'query={query},data={data}')

        if not self.__session:
            self.__establish()

        try:
            if data:
                resp = self.__session.post(f'{_BASE_URL}/{query}', json=data,
                                           headers={'Content-Type': 'application/json',
                                                    'Authorization': f'Bearer {self.token}'})
            else:
                resp = self.__session.get(f'{_BASE_URL}/{query}',
                                          headers={'Authorization': f'Bearer {self.token}'})

        except RequestException as e:
            if isinstance(e, Timeout):
                raise SessionTimeout(e)
            else:
                raise SessionException(e)

        if resp.status_code == 401 and kwargs.get('retry', True):
            logging.info(f'Session is not valid, reconnecting ({json.dumps(resp.json(), ensure_ascii=False)})')
            self.__session = None
            return self.call(query=query, data=data, retry=False)

        if resp.status_code != 200:
            raise SessionException(
                f'Error response. status code: {resp.status_code},'
                f' error details: {json.dumps(resp.json(), ensure_ascii=False)}')

        return resp.json()

    def check_credentials(self) -> bool:
        _LOGGER.debug(f'trying to login')
        result = True
        if not self.__session:
            try:
                self.__establish()
            except SessionException as e:
                _LOGGER.debug(e)
                result = False
        return result
