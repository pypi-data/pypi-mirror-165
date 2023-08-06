import json
from zaiclient import config
from zaiclient.request.RecommendationRequest import RecommendationRequest

class RelatedItemsRecommendationRequest(RecommendationRequest):
    
    __default_offset = 0
    __default_recommendation_type = "product_detail_page"
    
    def __init__(self, item_id: str, limit: int, offset: int = __default_offset, recommendation_type: str = __default_recommendation_type, options: dict = None):
        _options = options
        if options is not None:
            _options = json.dumps(options)
        if item_id is None:
            raise TypeError('None type is not available for item_id')
        super().__init__(user_id=None, item_id=item_id, item_ids=None, limit=limit, offset=offset, recommendation_type=recommendation_type, options=_options)
    
    def get_path(self, client_id: str) -> str:
        return config.ML_API_PATH_PREFIX.format(client_id) + config.RELATED_ITEMS_RECOMMENDATION_PATH_PREFIX