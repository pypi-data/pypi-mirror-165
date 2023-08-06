import traceback
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError

from wedeliver_core import WeDeliverCore
from wedeliver_core.wedeliver_core.helpers.auth import Auth
from wedeliver_core.wedeliver_core.helpers.format_exception import format_exception
from wedeliver_core.wedeliver_core.helpers.notification_center import (
    send_critical_error,
)
from wedeliver_core.wedeliver_core.helpers.validate_parameters import (
    validate_parameters,
)


def handle_exceptions(func):
    app = WeDeliverCore.getApp()

    @wraps(func)
    def inner_function(*args, **kws):
        try:
            result = func(*args, **kws)
            return result

        except Exception as e:
            # If the error related to the Database, then close the database session if it is open
            if isinstance(e, SQLAlchemyError):
                try:
                    db = app.extensions['sqlalchemy'].db
                    db.session.close()
                except Exception:
                    pass

            notification_channel = None
            if func is not None:
                if not validate_parameters(function=func):
                    notification_channel = "empty-parameters"

            if hasattr(e, "custom_exception"):
                public_message = e.args[0] if e.args else e.message if hasattr(e, 'message') else 'Unknown'
                status_code = e.code
            else:
                public_message = "Unhandled Exception"
                status_code = 500
                message = format_exception(
                    exception=traceback.format_exc(), user=Auth.get_user(), app=app
                )
                app.logger.error(message)
                send_critical_error(message=message, channel=notification_channel, app=app)

            return public_message, status_code

    return inner_function
