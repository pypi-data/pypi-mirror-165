import logging

_LOGGER = logging.getLogger(__name__)


class Meter:
    def __init__(self, session, **kwargs):
        self.session = session
        self.short_info = kwargs.get('info')
        self.title = kwargs.get('title')
        self.detail = kwargs.get('detail')
        self.capacity = kwargs.get('capacity')
        self.meter_id = kwargs['id_meter']
        self.account_id = kwargs['id_account']
        self.company_id = kwargs['id_company']
        self.precision = kwargs.get('precision')
        self.__info = None
        self.__measure_history = None

    def __fetch_meter_info(self) -> None:
        self.__info = {}
        data = self.session.call('user/account/meter/info',
                                 data={'id_company': self.company_id,
                                       'id_account': self.account_id,
                                       'id_meter': self.meter_id})
        for item in data['info']:
            self.__info[item['field_order']] = item

    def __fetch_history(self) -> None:
        data = self.session.call('user/account/meter/measure/history',
                                 data={'id_company': self.company_id,
                                       'id_account': self.account_id,
                                       'id_meters': [self.meter_id]})
        self.__measure_history = data['meter_measure_history']['meter_measure']

    @property
    def meter_info(self):
        if self.__info is None:
            self.__fetch_meter_info()
        return self.__info

    @property
    def history(self):
        if self.__measure_history is None:
            self.__fetch_history()
        return self.__measure_history

    @property
    def value(self):
        if self.__info is None:
            self.__fetch_meter_info()
        return float(self.meter_info['5']['value'])

    def upload_measure(self, value):
        self.session.call('user/account/meter/measure/set',
                          data={'id_company': self.company_id,
                                'id_account': self.account_id,
                                'id_meter': self.meter_id,
                                'value': value})

        self.__info = None

    def to_json(self, verbose):
        result = {'meter_id': f'{self.company_id}-{self.account_id}-{self.meter_id}',
                  'name': self.title,
                  'value': self.value,
                  'serial_number': self.meter_info['1']['value'],
                  'next_check_date': self.meter_info['4']['value']}

        if verbose > 2:
            result['precision'] = self.precision
            result['capacity'] = self.capacity

        if verbose > 3:
            result['meter_info'] = self.meter_info

        if verbose > 4:
            result['history'] = self.history
            result['detail'] = self.detail
        return result
