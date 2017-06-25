import logging

from core.behaviors import Singleton
from core.client import AbstractRestClient

from .constants import BASE_GOOGLE_MAPS_API_URL, GET_GEOCODING_URL

logger = logging.getLogger(__name__)


class GmapClient(metaclass=Singleton):
    def __init__(self):
        self.client = AbstractRestClient(base_url=BASE_GOOGLE_MAPS_API_URL)

    def get_geocoding(self, address=None):
        params = {}

        if address:
            params["address"] = address

        try:
            response = self.client.get(GET_GEOCODING_URL, params)
            if response.status_code != 200:
                return None

            return response.json().get("results")

        except Exception as e:
            logger.error(e)
            return None
