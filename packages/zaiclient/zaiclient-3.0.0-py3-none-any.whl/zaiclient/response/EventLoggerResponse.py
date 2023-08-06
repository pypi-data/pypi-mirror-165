from pydantic import BaseModel, confloat, constr, conint

class EventLoggerResponse(BaseModel):

    message: constr(min_length=0, max_length=1000)
    failure_count: conint(ge=0, le=1000)
    timestamp: confloat(ge=1_648_871_097., le=2_147_483_647.)

    class Config:

        schema_extra = {
            'example': {
                'message': 'The given event was handled successfully.',
                'failed_count': 0,
                'timestamp': 1_648_871_097.
            }
        }