import logging

from moydomjkh import Account

_LOGGER = logging.getLogger(__name__)


class User:
    def __init__(self, session):
        self.session = session
        self.__accounts = None
        self.__profile = None

    def __fetch_accounts(self) -> None:
        self.__accounts = {}
        data = self.session.call('user/accounts')
        for item in data['accounts']:
            obj = Account(session=self.session, **item)
            self.__accounts[f'{item["id_company"]}-{item["id_account"]}'] = obj

    def __fetch_profile(self) -> None:
        data = self.session.call('user/profile')
        del data['success']
        self.__profile = data

    @property
    def accounts(self):
        if self.__accounts is None:
            self.__fetch_accounts()
        return self.__accounts

    @property
    def profile(self):
        if self.__profile is None:
            self.__fetch_profile()
        return self.__profile

    def to_json(self, verbose):
        result = {'accounts': {k: v.to_json(verbose) for k, v in self.accounts.items()}}
        if verbose > 4:
            result['profile'] = self.profile
        return result
