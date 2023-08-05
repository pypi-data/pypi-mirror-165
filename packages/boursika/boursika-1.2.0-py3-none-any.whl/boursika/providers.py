import pandas as pd
import requests

from .config import BOURSIKA_API_BASE_URL
from .errors import ActionError


class BaseProvider:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def _call_provider_action(self, service_slug: str, action_name: str, parameters: dict):
        endpoint = f'{BOURSIKA_API_BASE_URL}/providers/{service_slug}/actions/{action_name}/calls/'

        try:
            response = requests.post(endpoint, json={
                'parameters': parameters,
            }, headers={
                'ApiKey': self.api_key,
            }, timeout=15)

            response.raise_for_status()

            return response.json().get('result')
        except requests.exceptions.HTTPError as e:
            raise ActionError(message=e.response.json().get('message'))


class TseProvider(BaseProvider):
    def get_all_symbols(self) -> pd.DataFrame:
        raw = super()._call_provider_action(
            service_slug='tse',
            action_name='get_all_symbols',
            parameters={},
        )

        return pd.DataFrame(raw)

    def get_daily_ticks(self, symbol_id: str, page: int = 1) -> pd.DataFrame:
        raw = super()._call_provider_action(
            service_slug='tse',
            action_name='get_daily_ticks',
            parameters={
                'symbol_id': symbol_id,
                'page': page,
            },
        )

        return pd.DataFrame(raw)

    def get_last_daily_tick(self, symbol_id: str) -> pd.Series:
        raw = super()._call_provider_action(
            service_slug='tse',
            action_name='get_last_daily_tick',
            parameters={
                'symbol_id': symbol_id,
            },
        )

        return pd.Series(raw)
