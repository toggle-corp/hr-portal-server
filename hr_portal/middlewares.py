import threading

_threadlocal = threading.local()


def get_current_user():
    req = get_signal_request()
    if req:
        return req.user


def get_signal_request():
    """
    !!! Do not use if your operation is asynchronus !!!
    Allow to access current request in signals
    This is a hack that looks into the thread
    Mainly used for log purpose
    """

    return getattr(_threadlocal, "request", None)


def get_current_user_is_superuser():
    user = get_current_user()
    if user:
        return user.is_superuser


class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # return response
        setattr(_threadlocal, "request", request)
        return self.get_response(request)
