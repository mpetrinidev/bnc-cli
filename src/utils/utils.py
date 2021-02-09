class Utils:
    def __init__(self):
        pass

    @staticmethod
    def to_query_string_parameters(values: {}) -> str:
        if not values:
            raise ValueError('values cannot be empty')

        return '&'.join(key + '=' + str(val) for key, val in values.items())
