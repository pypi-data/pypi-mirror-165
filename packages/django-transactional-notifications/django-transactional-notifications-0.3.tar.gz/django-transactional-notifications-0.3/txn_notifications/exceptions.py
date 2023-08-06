class NotificationNotSent(Exception):
    """"""

    def __init__(self, msg, code=None):
        self.code = code

        super().__init__(msg)


class WrapperError(NotificationNotSent):
    """For handling any exception raise by the NotificationWrapper"""

    def __init__(self, msg, code=None):
        if not code:
            code = "wrapper_error"
        super().__init__(msg, code)


class Disallowed(NotificationNotSent):
    def __init__(self, msg, code=None):
        if not code:
            code = "disallowed"
        super().__init__(msg, code)


class CategoryDisallowed(Disallowed):
    def __init__(self, msg, code=None):
        if not code:
            code = "category_disallowed"
        super().__init__(msg, code)


class HandlerDisallowed(Disallowed):
    def __init__(self, msg, code=None):
        if not code:
            code = "handler_disallowed"
        super().__init__(msg, code)
