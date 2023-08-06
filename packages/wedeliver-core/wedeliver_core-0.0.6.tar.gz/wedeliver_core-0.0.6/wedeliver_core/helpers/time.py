from datetime import datetime, timedelta
import pytz

from flask import request

DATABASE_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DATABASE_TIME_FORMAT = "%H:%M:%S"


def get_time_zone():
    time_zone = "UTC"
    if request:
        if request.headers.get("country_code"):
            time_zone = dict(sa="Asia/Riyadh", ps="Asia/Hebron").get(
                request.headers.get("country_code"), "UTC"
            )
    return time_zone


def from_utc_to_datetime_zone(date_time, time_zone=None):
    if isinstance(date_time, str):
        date_time = date_time.replace("T", " ").replace("Z", "")
    # Get the default Time Zone if not sent in parameters
    # Time Zone in KSA for example should be: UTC
    if not date_time:
        return date_time

    if len(str(date_time)) < 12:
        return date_time
    if time_zone is None:
        time_zone = get_time_zone()
    # Check if there is a set timezone, if not, return the datetime as it is
    if not time_zone:
        # app.logger.error(format_exception(traceback.format_exc()))
        return date_time

    # Check the time_zone if it is correct. If it is not defined, return the same date_time without conversion
    try:
        time_zone = pytz.timezone(time_zone)
    except Exception:
        # app.logger.error(format_exception(traceback.format_exc()))
        return date_time
    # Convert the date time to datetime object if it is sent as string
    if isinstance(date_time, str) or isinstance(date_time, timedelta):
        date_time = datetime.strptime(str(date_time)[:19], DATABASE_DATE_FORMAT[:17])
    date_time = pytz.utc.localize(date_time)

    # This method is not working, makes some extra minutes, do not use it!!!!
    # date_time = date_time.replace(tzinfo=pytz.utc)
    # If after checking the date time is not an object valid for conversion, return the object as it is
    if not isinstance(date_time, datetime):
        # app.logger.error(format_exception(traceback.format_exc()))
        return date_time

    # Convert the date_time to the target timezone
    # If the conversion failed, we should return the object as it is
    try:
        date_time = (date_time.astimezone(time_zone)).strftime(DATABASE_DATE_FORMAT)
    except Exception:
        pass
        # app.logger.error(format_exception(traceback.format_exc()))

    return date_time


def from_datetime_zone_to_utc(date_time, time_zone=None, only_date=False, to_string=True):
    if isinstance(date_time, str):
        date_time = date_time.replace("T", " ").replace("Z", "")
        if len(str(date_time)) < 12:
            return date_time
    # Get the default Time Zone if not sent in parameters
    # Time Zone in KSA for example should be: UTC

    if time_zone is None:
        time_zone = get_time_zone()
    # Check if there is a set timezone, if not, return the datetime as it is
    if not time_zone:
        # app.logger.error(format_exception(traceback.format_exc()))
        return date_time

    # Check the time_zone if it is correct. If it is not defined,
    # return the same date_time without conversion
    try:
        time_zone = pytz.timezone(time_zone)
    except Exception:
        # app.logger.error(format_exception(traceback.format_exc()))
        return date_time
    # Convert the date time to datetime object if it is sent as string
    if isinstance(date_time, str) or isinstance(date_time, timedelta):
        date_time = datetime.strptime(str(date_time)[:19], DATABASE_DATE_FORMAT[:17])

        date_time = time_zone.localize(date_time)
    # This method is not working, makes somoe extra minutes, do not use it!!!!
    # date_time = date_time.replace(tzinfo=time_zone)

    # If after checking the date time is not an object valid for conversion, return the object as it is
    if not isinstance(date_time, datetime):
        # app.logger.error(format_exception(traceback.format_exc()))
        return date_time

    # Convert the date_time to the target timezone
    # If the conversion failed, we should return the object as it is
    try:
        date_time = (date_time.astimezone(pytz.timezone(pytz.utc.zone)))
        if only_date:
            date_time = datetime(date_time.year, date_time.month, date_time.day)

        if to_string:
            date_time = date_time.strftime(
                DATABASE_DATE_FORMAT
            )
    except Exception:
        pass
        # app.logger.error(format_exception(traceback.format_exc()))
    return date_time
