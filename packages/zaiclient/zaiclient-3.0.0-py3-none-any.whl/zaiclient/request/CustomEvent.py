import time
from typing import List, Union
from zaiclient.request.BaseEvent import BaseEvent
from zaiclient.exceptions.InputTypeNotEqualException import InputTypeNotEqualException
from zaiclient.exceptions.InputLengthNotEqualException import InputLengthNotEqualException

class CustomEvent(BaseEvent):
    
    def __init__(self, user_id: str, item_ids: Union[str, List[str]], event_type: str, event_values: Union[str, List[str]], timestamp: float = time.time()):
        
        if not isinstance(user_id, str):
            raise TypeError("User ID must be a string value.")
        
        if not isinstance(event_type, str):
            raise TypeError("Event Type must be a string value.")
            
        if type(item_ids) != type(event_values):
            raise InputTypeNotEqualException
        
        if (isinstance(item_ids, List) and isinstance(event_values, List)):
            if not (all(isinstance(item_id, str) for item_id in item_ids) and all(isinstance(event_value, str) for event_value in event_values)):
                raise TypeError("The ids in list do not have the same type.")
        
        _item_ids = [item_ids] if type(item_ids) == str else item_ids
        _event_values = [event_values] if type(event_values) == str else event_values
        
        if len(_item_ids) != len(_event_values):
            raise InputLengthNotEqualException
        
        super().__init__(user_id, _item_ids, timestamp, event_type, _event_values)