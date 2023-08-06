import flask_sqlalchemy

from wedeliver_core import WeDeliverCore
from wedeliver_core.helpers.exceptions import AppMicroFetcherError, AppFetchServiceDataError
import requests
import json

from wedeliver_core.helpers.get_obj_value import get_obj_value


class MicroFetcher(object):
    base_data = None
    app = None
    service_name = None
    service_url = None
    fields = None
    table_name = None
    column_name = None
    compair_operator = None
    column_values = None
    output_key = None
    lookup_key = None
    module_name = None
    function_params = None

    def __init__(self, service_name):
        self.app = WeDeliverCore.getApp()
        self.service_url = self.app.config.get(service_name)
        self.service_name = service_name
        if not self.service_url:
            raise AppMicroFetcherError('Service {} not defined on Env'.format(self.service_url))

    def join(self, base_data, output_key=None):
        self.base_data = base_data

        if output_key:
            output_key = output_key.split('as ')[1]

        self.output_key = "{}".format(self.service_name.split('_')[0].lower()) if not output_key else output_key
        return self

    def select(self, *args):
        self.fields = list(args)
        return self

    def filter(self, *args):
        against = args[0].split('.')
        self.compair_operator = args[1]
        self.lookup_key = args[2]
        self.column_values = set()
        if isinstance(self.base_data, dict):
            self.column_values.add(get_obj_value(self.base_data, self.lookup_key))
        else:
            if isinstance(self.base_data, flask_sqlalchemy.Pagination):
                data = self.base_data.items
            else:
                data = self.base_data

            for row in data:
                self.column_values.add(get_obj_value(row, self.lookup_key))

        if not len(self.column_values):
            return self
            # raise AppMicroFetcherError('Lookup key {} not found'.format(self.lookup_key))

        self.column_values = list(self.column_values)
        self.column_values = self.column_values[0] if len(self.column_values) == 1 else self.column_values

        if self.compair_operator not in ('=', 'IN'):
            raise AppMicroFetcherError('Only == currently supported')

        self.compair_operator = 'IN' if isinstance(self.column_values, list) else self.compair_operator

        self.table_name = against[0]
        self.column_name = against[1]

        self.fields.append(self.column_name)
        return self

    def fetch(self):
        if self.column_values or self.module_name:
            return self._call_api()
        else:
            return self.base_data

    def with_params(self, **kwargs):
        self.function_params = kwargs
        return self

    def from_function(self, module_name):
        self.module_name = module_name
        return self

    def _call_api(self):

        url = "{}/fetch_relational_data".format(self.service_url)

        payload_dict = {
            "fields": self.fields,
            "table_name": self.table_name,
            "column_name": self.column_name,
            "compair_operator": self.compair_operator,
            "column_values": self.column_values,
        }

        if self.module_name:
            payload_dict.update(
                functions=[
                    dict(
                        name=self.module_name,
                        fields=self.fields,
                        params=self.function_params if self.function_params else dict()
                    )
                ]
            )

        payload = json.dumps(payload_dict)
        headers = {
            'country_code': 'sa',
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code != 200:
            self.app.logger.error(response.text)
            raise AppFetchServiceDataError()

        result = response.json()
        # in case there is no match from relations data
        # if not len(result):
        #     for rel_value in _relations_values:
        #         fetched_object = dict()
        #         fetched_object['id'] = rel_value
        #         for field in fields:
        #             if not fetched_object.get(field):
        #                 fetched_object[field] = None
        #         result.append(fetched_object)
        if self.base_data:
            return self._map_base(result)

        return result

    def _map_base(self, result):
        if isinstance(self.base_data, dict):
            for rd in result:
                if self.base_data.get(self.lookup_key) == rd.get(self.column_name):
                    try:
                        setattr(self.base_data, self.output_key, rd)
                    except AttributeError:
                        self.base_data[self.output_key] = rd
        else:
            if isinstance(self.base_data, flask_sqlalchemy.Pagination):
                data = self.base_data.items
            else:
                data = self.base_data

            for row in data:
                for rd in result:
                    if get_obj_value(row, self.lookup_key) == rd.get(self.column_name):
                        try:
                            setattr(row, self.output_key, rd)
                        except AttributeError:
                            row[self.output_key] = rd

            if isinstance(self.base_data, flask_sqlalchemy.Pagination):
                self.base_data.items = data
            else:
                self.base_data = data

        return self.base_data
