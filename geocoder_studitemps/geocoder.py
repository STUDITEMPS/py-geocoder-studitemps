from typing import Tuple, Optional, Dict, Any
import requests
from requests.models import Response
from pydantic import BaseModel, validator, root_validator
from i18naddress import normalize_address

class Address(BaseModel):
    street: str
    postal_code: str
    city: str
    country_code: str = "DE"

    @root_validator(pre=False)
    def check_normalization_passes(cls, values):
        normalize_address({
            "street_address" : values["street"],
            "postal_code" : values["postal_code"],
            "city" : values["city"],
            "country_code" : values["country_code"]
        })
        return values

    def __str__(self) -> str:
        return f"{self.street}, {self.postal_code} {self.city}"


class Geopoint(BaseModel):
    latitude: float
    longitude: float


class Geocoder:

    def __init__(
        self,
        host: str
    ) -> None:
        self._host = host

    def coordinates(self, address: Address) -> Optional[Geopoint]:
        response = self._do_request(address)
        return self._handle_response(response)

    def _do_request(self, address: Address):
        params = {"address" : str(address)}

        result = requests.get(
            self._base_url(),
            params=params
        )

        return result

    def _handle_response(self, response: Response) -> Optional[Geopoint]:
        if response.status_code == requests.codes.ok:
            data = response.json()
            if len(data) == 0:
                return None
            else:
                return Geopoint(**data)
        else:
            response.raise_for_status()

    def _base_url(self) -> str:
        return f"{self._host}/geocode"

