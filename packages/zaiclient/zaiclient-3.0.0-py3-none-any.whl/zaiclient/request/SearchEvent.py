import time
from zaiclient.request.BaseEvent import BaseEvent

class SearchEvent(BaseEvent):
    
    __default_event_type = "search"
    __default_item_id = "null"
    
    def __init__(self, user_id: str, search_query: str, timestamp: float = time.time()):
        
        if not isinstance(user_id, str):
            raise TypeError("User ID must be a string value.")
        
        if not isinstance(search_query, str):
            raise TypeError("Search Query must be a string value.")
        
        _item_ids = [self.__default_item_id]
        _event_values = [search_query]
        
        super().__init__(user_id, _item_ids, timestamp, self.__default_event_type, _event_values)