from wedeliver_core import WeDeliverCore
from wedeliver_core.helpers.sql import sql
import importlib
import os


def fetch_relational_data(fields,
                          table_name,
                          column_name,
                          compair_operator,
                          column_values, functions=None):
    app = WeDeliverCore.getApp()
    db = app.extensions['sqlalchemy'].db

    relational_data_result = []
    if table_name:
        query = """
        SELECT {fields}
        FROM {table_name}
        WHERE {column_name} {compair_operator} {column_values}
        """.format(
            fields=', '.join(fields),
            table_name=table_name,
            column_name=column_name,
            compair_operator=compair_operator,
            column_values='({})'.format(
                ', '.join([str(val) for val in column_values])) if compair_operator == 'IN' else column_values,
        )
        relational_data_result = sql(query, db)

    def _update_relational_data_result(function_result, fields):
        if relational_data_result:
            for rd in relational_data_result:
                for f in fields:
                    rd[f] = function_result.get(f) if isinstance(function_result,
                                                                 dict) else function_result.__dict__.get(f)
        else:
            fields_dict = dict()
            for f in fields:
                fields_dict[f] = function_result.get(f) if isinstance(function_result,
                                                                      dict) else function_result.__dict__.get(f)
            relational_data_result.append(fields_dict)

    if functions and isinstance(functions, list):
        for func in functions:
            function_file, function_call = os.path.splitext(func.get('name'))
            m = importlib.import_module(function_file)
            method = getattr(m, function_call[1:])

            function_result = method(**func.get('params'))

            fields = func.get('fields')
            if function_result:
                if isinstance(function_result, list):
                    for row in function_result:
                        _update_relational_data_result(row, fields)
                else:
                    _update_relational_data_result(function_result, fields)

    return relational_data_result
