from functools import wraps
from flask import current_app
from invenio_i18n import lazy_gettext as _


def handle_errors(error_placeholder=None, alert_user=False):
    """
    Decorator for metadata resolver functions that:
    - logs any exception that occurs,
    - prevents the error from propagating further,
    - returns the given placeholder if provided,
    otherwise returns None
    """

    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if alert_user and "problems" in kwargs:
                    from .base import ResolverProblem, ResolverProblemLevel
                    self = args[0]
                    kwargs["problems"].append(
                        ResolverProblem(resolver=self.name, message=_("Unexpected error while parsing the metadata."),
                                        level=ResolverProblemLevel.ERROR, original_exception=e))
                current_app.logger.exception(
                    "Function '%s' failed with error: '%s'.",
                    func.__name__,
                    e
                )
            return error_placeholder  # placeholder or discard

        return inner

    return decorator
