from typing import Union
from pydantic import BaseModel, confloat, constr

class Event(BaseModel):

    user_id: constr(min_length=1, max_length=100)
    item_id: Union[constr(min_length=0, max_length=100), None]
    timestamp: confloat(ge=1_648_871_097., le=2_147_483_647.)
    event_type: constr(min_length=0, max_length=100)
    event_value: constr(min_length=0, max_length=100)
    
    class Config:

        schema_extra = {
            'example': {
                'user_id': '714a93f4-a0bd-4a65-87ba-b268584853d4',
                'item_id': 'P71389478937934',
                'timestamp': 1_648_871_097.,
                'event_type': 'view',
                'event_value': '1'
            }
        }