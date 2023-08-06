class InputTypeNotEqualException(Exception):
    def __str__(self):
        return "The input type of ids and values is not the same."