class EmptyBatchException(Exception):
    def __str__(self):
        return "Cannot log empty EventBatch object."