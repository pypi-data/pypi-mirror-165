import logging

from moydomjkh.meter import Meter
from moydomjkh.period import BillingPeriod

_LOGGER = logging.getLogger(__name__)


class AccountException(BaseException):
    pass


class Account:
    def __init__(self, session, **kwargs):
        self.session = session
        self.inn = kwargs.get('inn')
        self.status = kwargs.get('status')
        self.account = kwargs.get('account')
        self.address = kwargs.get('address')
        self.account_id = kwargs['id_account']
        self.company_id = kwargs['id_company']
        self.status_text = kwargs.get('status_text')
        self.company_name = kwargs.get('company_name')
        self.company_full_name = kwargs.get('company_full_name')
        self.__meters = None
        self.__info = None
        self.__balances = None
        self.__pays = None
        self.__periods = None

    def __fetch_balances(self) -> None:
        data = self.session.call('user/account/balances',
                                 data={'id_company': self.company_id, 'id_account': self.account_id})
        self.__balances = {'year': data.get('year'), 'debt': data.get('dolg')}

    def __fetch_pays(self) -> None:
        data = self.session.call('user/account/pays',
                                 data={'id_company': self.company_id, 'id_account': self.account_id})
        self.__pays = {'year': data.get('year'), 'last_pay': data.get('last_pay')}

    def __fetch_periods(self) -> None:
        self.__periods = {}
        data = self.session.call('user/account/available_period',
                                 data={'id_company': self.company_id, 'id_account': self.account_id})

        for item in data['periods']:
            item['id_company'] = self.company_id
            item['id_account'] = self.account_id
            self.__periods[item['period']] = BillingPeriod(self.session, **item)

    def __fetch_info(self) -> None:
        self.__info = {}
        data = self.session.call('user/account/info',
                                 data={'id_company': self.company_id, 'id_account': self.account_id})
        for item in data['info']:
            self.__info[item['field_order']] = item

    def __fetch_meters(self) -> None:
        self.__meters = {}
        data = self.session.call('user/account/meters',
                                 data={'id_company': self.company_id, 'id_account': self.account_id})
        for item in data['meter']:
            item['id_company'] = self.company_id
            item['id_account'] = self.account_id
            obj = Meter(session=self.session, **item)
            self.__meters[f'{item["id_company"]}-{item["id_account"]}-{item["id_meter"]}'] = obj

    @property
    def meters(self):
        if self.__meters is None:
            self.__fetch_meters()
        return self.__meters

    @property
    def balance_history(self):
        if self.__balances is None:
            self.__fetch_balances()
        return self.__balances

    @property
    def billing_periods(self):
        if self.__periods is None:
            self.__fetch_periods()
        return self.__periods

    @property
    def payment_history(self):
        if self.__pays is None:
            self.__fetch_pays()
        return self.__pays

    @property
    def account_info(self):
        if self.__info is None:
            self.__fetch_info()
        return self.__info

    def generate_payment_url(self, payment_value=None):
        preview = self.session.call('user/account/payonline/preview',
                                    data={'id_company': self.company_id,
                                          'id_account': self.account_id,
                                          'pay_type': '2'})['merchant'][0]

        if payment_value is None:
            payment_value = float(preview['itog']['value'])

        if payment_value < 5.:
            payment_value = 5.

        data = self.session.call('/user/account/payonline',
                                 data={'id_company': self.company_id,
                                       'id_account': self.account_id,
                                       'period': preview['period'],
                                       'id_merchant': preview['id_merchant'],
                                       'id_merchant_pay_system': preview['id_merchant_pay_system'],
                                       'sum_pay': payment_value})
        return data['url']

    def to_json(self, verbose):
        result = {'account_id': f'{self.company_id}-{self.account_id}',
                  'account_name': self.account,
                  'meters': {k: v.to_json(verbose) for k, v in self.meters.items()},
                  'balance': self.account_info['5']['value'],
                  'fine_balance': self.account_info['6']['value'],
                  'status': self.status}

        if verbose > 1:
            result['status'] = self.status

        if verbose > 2:
            result['address'] = self.address
            result['area'] = self.account_info['3']['value']
            result['company_name'] = self.company_name

        if verbose > 3:
            result['balance_history'] = self.balance_history
            result['payment_history'] = self.payment_history

        if verbose > 4:
            result['status_text'] = self.status_text
            result['company_full_name'] = self.company_full_name
            result['inn'] = self.inn
            result['info'] = self.account_info
        return result
