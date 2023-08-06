class InputLengthNotEqualException(Exception):
    def __str__(self):
        return "All lists in input parameters must be of the same length."