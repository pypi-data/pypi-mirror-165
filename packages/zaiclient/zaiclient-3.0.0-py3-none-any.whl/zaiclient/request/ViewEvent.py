import time
from typing import List, Union
from zaiclient.request.BaseEvent import BaseEvent

class ViewEvent(BaseEvent):
    
    __default_event_type = "view"
    __default_event_value = "1"
    
    def __init__(self, user_id: str, item_ids: Union[str, List[str]], timestamp: float = time.time()):
        
        if not isinstance(user_id, str):
            raise TypeError("User ID must be a string value.")
        
        if (isinstance(item_ids, List)):
            if not all(isinstance(item_id, str) for item_id in item_ids):
                raise TypeError("The ids in list do not have the same type.")

        _item_ids = [item_ids] if type(item_ids) == str else item_ids
        _event_values = [self.__default_event_value] * len(_item_ids)
        
        super().__init__(user_id, _item_ids, timestamp, self.__default_event_type, _event_values)