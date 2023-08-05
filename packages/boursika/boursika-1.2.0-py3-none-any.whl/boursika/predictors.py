import requests

from .config import BOURSIKA_API_BASE_URL
from .enums import Trends
from .errors import ActionError
from .providers import TseProvider
from .utils.date_helpers import get_tehran_end_of_day, get_tehran_next_active_day


class BasePredictor:
    def __init__(self, api_key: str):
        self.api_key = api_key

        self.tse_provider = TseProvider(api_key=api_key)

    def _predict(self, target_key: str, target_timestamp: int, payload: dict):
        endpoint = f'{BOURSIKA_API_BASE_URL}/predictors/-/predictions/'

        try:
            response = requests.post(endpoint, json={
                'target_key': target_key,
                'target_timestamp': target_timestamp,
                'payload': payload,
            }, headers={
                'ApiKey': self.api_key,
            }, timeout=15)

            response.raise_for_status()

            return response.json().get('prediction')
        except requests.exceptions.HTTPError as e:
            raise ActionError(message=e.response.json().get('message'))


class TseDailyPriceTrendPredictorClient(BasePredictor):
    def predict(self, symbol_id: str, trend: Trends):
        target_timestamp = int(get_tehran_end_of_day(get_tehran_next_active_day()).timestamp())
        return super()._predict(
            target_key=symbol_id,
            target_timestamp=target_timestamp,
            payload={
                'trend': trend.value,
            },
        )


class TseDailyPricePredictorClient(BasePredictor):
    def predict(self, symbol_id: str, price: int):
        target_timestamp = int(get_tehran_end_of_day(get_tehran_next_active_day()).timestamp())
        return super()._predict(
            target_key=symbol_id,
            target_timestamp=target_timestamp,
            payload={
                'price': price,
            },
        )
