class BatchSizeLimitExceededException(Exception):
    def __str__(self):
        return "The number of items in event batch exceeded the size limit."