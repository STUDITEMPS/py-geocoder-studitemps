from typing import Tuple, Optional, Dict, Any
import requests
from requests.models import Response
from pydantic import BaseModel, validator, root_validator
from i18naddress import normalize_address
from geocoder_studitemps.config import Settings


class Address(object):

    def __init__(self, street, postal_code, city, country_code = "DE"):
        self.street = street
        self.postal_code = postal_code
        self.city = city
        self.country_code = country_code

    def validate(self):
        normalize_address({
            "street_address" : self.street if self.street else None,
            "postal_code" : self.postal_code if self.postal_code else None,
            "city" : self.city if self.city else None,
            "country_code" : self.country_code if self.country_code else None,
        })

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
        access_token: str = None,
        timeout: int = 5
    ) -> None:
        self._settings = settings
        self._access_token = access_token
        self._timeout = timeout

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

    def get_access_token(self) -> str:
        return self._access_token

    def _do_request(self, address: Address):
        headers = {"authorization" : f"Bearer {self._access_token}" }
        params = {"address" : address.to_request_string()}

        result = requests.get(
            self._base_url(),
            params=params,
            headers=headers,
            timeout=self._timeout
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

