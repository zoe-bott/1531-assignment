class BookingError(Exception):
    def __init__(self, error, msg=None):
        if msg is None:
            msg = "Booking validation error occurred"
        super().__init__(msg)
        self.error = error
class LoginError(Exception):
    def __init__(self, errors, msg=None):
        if msg is None:
            msg = "Login validation error occurred."
        super().__init__(msg)
        self.errors = errors
class EditError(Exception):
     def __init__(self, errors, msg=None):
        if msg is None:
            msg = "Editing validation error occurred."
        super().__init__(msg)
        self.errors = errors