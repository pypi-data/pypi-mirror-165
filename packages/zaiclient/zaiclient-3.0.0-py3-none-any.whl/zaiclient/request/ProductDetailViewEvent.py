import time
from zaiclient.request.BaseEvent import BaseEvent

class ProductDetailViewEvent(BaseEvent):
    
    __default_event_type = "product_detail_view"
    __default_event_value = "null"
    
    def __init__(self, user_id: str, item_id: str, timestamp: float = time.time()):
        
        if not isinstance(user_id, str):
            raise TypeError("User ID must be a string value.")
        
        if not isinstance(item_id, str):
            raise TypeError("Item ID must be a string value.")
        
        _item_ids = [item_id]
        _event_values = [self.__default_event_value]
        
        super().__init__(user_id, _item_ids, timestamp, self.__default_event_type, _event_values)