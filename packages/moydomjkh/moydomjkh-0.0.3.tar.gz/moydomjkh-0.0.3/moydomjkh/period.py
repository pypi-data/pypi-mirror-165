import logging

_LOGGER = logging.getLogger(__name__)


class BillingPeriod:
    def __init__(self, session, **kwargs):
        self.session = session
        self.year = kwargs.get('year')
        self.month = kwargs.get('month')
        self.period_name = kwargs.get('period_name')
        self.month_name = kwargs.get('month_name')
        self.period_id = kwargs['period']
        self.account_id = kwargs['id_account']
        self.company_id = kwargs['id_company']
        self.__details = None

    def __fetch_details(self) -> None:
        self.__details = {}
        data = self.session.call('user/account/balance/detail',
                                 data={'id_company': self.company_id,
                                       'id_account': self.account_id,
                                       'id_meter': self.period_id})
        self.__details = data['service']

    @property
    def details(self):
        if self.__details is None:
            self.__fetch_details()
        return self.__details

    def to_json(self, verbose):
        result = {'period_id': self.period_id,
                  'year': self.year,
                  'month': self.month,
                  'period_name': self.period_name,
                  'month_name': self.month_name,
                  'details': self.details}

        return result
