from sqlalchemy import text


def sql(query, db):
    result = db.engine.execute(text(query))
    result_list = list()
    # app.logger.debug(result)
    for rowproxy in result:
        temp = dict()
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in rowproxy.items():
            # build up the dictionary
            temp = {**temp, **{column: value}}
        result_list.append(temp)

    return result_list
