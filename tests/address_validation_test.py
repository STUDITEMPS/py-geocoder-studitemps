import pytest
from pydantic import ValidationError
from geocoder_studitemps.geocoder import Address
from i18naddress import InvalidAddress


def test_works_on_valid_addresses():
    addresses = [
        {
            "data" : {
                "street" : "im mediapark 4a",
                "postal_code" : "50670",
                "city" : "köln"
            },
            "str" : "<Address (im mediapark 4a, 50670 köln) (DE)>",
            "req_str" : "im mediapark 4a, 50670 köln",
        }
    ]

    for addr_info in addresses:
        addr = Address(**addr_info["data"])

        assert addr.country_code == "DE"
        assert addr.to_request_string() == addr_info["req_str"]
        assert str(addr) == addr_info["str"]


def test_raises_validation_error_on_invalid_addresses():
    addresses = [
        {
            "data" : {
                "street" : "im mediapark 4a",
                "postal_code" : "800 45",
                "city" : "Madrid"
            },
            "err" : r"Invalid address*"
        }
    ]

    for addr_info in addresses:
        with pytest.raises(InvalidAddress, match=addr_info["err"]):
            addr = Address(**addr_info["data"])
            addr.validate()