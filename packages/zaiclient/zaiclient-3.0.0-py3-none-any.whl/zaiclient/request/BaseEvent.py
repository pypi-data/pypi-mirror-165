import json
from typing import List
from zaiclient import config
from zaiclient.exceptions.BatchSizeLimitExceededException import BatchSizeLimitExceededException
from zaiclient.exceptions.EmptyBatchException import EmptyBatchException

from zaiclient.request.Event import Event


class BaseEvent(object):
    
    def __init__(self, user_id: str, item_ids: List[str], timestamp: float, event_type: str, event_values: List[str]) -> None:        
        events = []
        self._timestamp = timestamp
        tmp_timestamp = timestamp
        
        for item_id, event_value in zip(item_ids, event_values):
            events.append(
                json.loads(Event(
                    user_id=user_id, 
                    item_id=item_id, 
                    timestamp=tmp_timestamp, 
                    event_type=event_type, 
                    event_value=event_value
                ).json())
            )
            tmp_timestamp += config.EPSILON
        
        if len(events) > config.BATCH_REQUEST_CAP:
            raise BatchSizeLimitExceededException()
        
        if len(events) == 0:
            raise EmptyBatchException()
        
        if len(events) == 1:
            self._payload = events[0]
        else:
            self._payload = events

    def get_payload(self):
        return self._payload

    def get_timestamp(self):
        return self._timestamp