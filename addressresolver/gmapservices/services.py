from core.behaviors import Singleton
from .client import GmapClient


class GmapServices(metaclass=Singleton):
    def __init__(self):
        self.client = GmapClient()

    def get_geocoding_from_address(self, address):
        geocoding = self.client.get_geocoding(address)
        if not geocoding or len(geocoding) == 0:
            return None

        return geocoding

    def get_lat_and_lng_from_address(self, address):
        geocoding = self.get_geocoding_from_address(address)

        if not geocoding:
            return None

        location = geocoding[0]["geometry"]["location"]
        return location["lat"], location["lng"]
