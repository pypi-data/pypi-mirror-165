class IncorrectDataReceivedError(Exception):
    def __str__(self):
        return 'Incorrect message received.'


class ServerError(Exception):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class NonDictInputError(Exception):
    def __str__(self):
        return 'Function arg must be a dictionary'


class ReqFieldMissingError(Exception):
    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'Required field {self.missing_field} missing.'
