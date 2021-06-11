from typing import Tuple, Optional, Dict, Any
import requests
from requests.models import Response
from pydantic import BaseModel, validator, root_validator
from i18naddress import normalize_address
from geocoder_studitemps.config import Settings

class Address(BaseModel):
    street: str
    postal_code: str
    city: str
    country_code: str = "DE"

    @root_validator(pre=False)
    def check_normalization_passes(cls, values):
        normalize_address({
            "street_address" : values["street"] if "street" in values else None,
            "postal_code" : values["postal_code"] if "postal_code" in values else None,
            "city" : values["city"] if "city" in values else None,
            "country_code" : values["country_code"] if "country_code" in values else None,
        })
        return values

    def to_request_string(self) -> str:
        return f"{self.street}, {self.postal_code} {self.city}"

    def __str__(self) -> str:
        return f"<Address ({self.street}, {self.postal_code} {self.city}) ({self.country_code})>"


class Geopoint(BaseModel):
    latitude: float
    longitude: float


class Geocoder:

    def __init__(
        self,
        settings: Settings,
        access_token: str = None
    ) -> None:
        self._settings = settings
        self._access_token = access_token

    def authenticate(self) -> Response:
        """
        Authorize your application with Auth0 and fetch an access_token, which
        can be used for further requests.
        """
        headers = { 'content-type': "application/x-www-form-urlencoded" }
        
        payload = {
            "grant_type" : "client_credentials",
            "client_id" : self._settings.AUTH0_CLIENT_ID,
            "client_secret" : self._settings.AUTH0_CLIENT_SECRET,
            "audience" : self._settings.AUTH0_AUDIENCE
        }

        response = requests.post(self._auth0_url(), data=payload, headers=headers)
        data = response.json()
        
        self._access_token = data["access_token"]
        
        return response

    def coordinates(self, address: Address) -> Optional[Geopoint]:
        response = self._do_request(address)
        return self._handle_response(response)

    def _do_request(self, address: Address):
        headers = {"authorization" : f"Bearer {self._access_token}" }
        params = {"address" : address.to_request_string()}

        result = requests.get(
            self._base_url(),
            params=params,
            headers=headers
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

    def _auth0_url(self) -> str:
        return self._settings.AUTH0_SITE

    def _base_url(self) -> str:
        return f"{self._settings.PROTOCOL}://{self._settings.GEOCODER_HOST}/geocode"

