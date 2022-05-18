class ReqFieldMissingError(Exception):

    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'Required field is missing: {self.missing_field}.'
