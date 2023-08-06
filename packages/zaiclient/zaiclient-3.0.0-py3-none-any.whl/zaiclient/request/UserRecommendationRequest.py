import json
from zaiclient import config
from zaiclient.request.RecommendationRequest import RecommendationRequest

class UserRecommendationRequest(RecommendationRequest):
    
    __default_offset = 0
    __default_recommendation_type = "homepage"
    
    def __init__(self, user_id: None, limit: int, offset: int = __default_offset, recommendation_type: str = __default_recommendation_type, options: dict = None):
        _options = options
        if options is not None:
            _options = json.dumps(options)
        super().__init__(user_id=user_id, item_id=None, item_ids=None, limit=limit, offset=offset, recommendation_type=recommendation_type, options=_options)

    def get_path(self, client_id: str) -> str:
        return config.ML_API_PATH_PREFIX.format(client_id) + config.USER_RECOMMENDATION_PATH_PREFIX