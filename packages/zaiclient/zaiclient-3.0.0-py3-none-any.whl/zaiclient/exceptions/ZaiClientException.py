from requests import HTTPError

class ZaiClientException(Exception):

    def __init__(self, e: HTTPError):
        self.__status_code = e.response.status_code
        
    def get_http_status_code(self):
        return self.__status_code