## Geocoder Python

### Usage

```python

# get geocoordinates for an address
from geocoder_studitemps import Geocoder, Address

# this will create and validate the format of an address, using the 
# the google i18 address api. see: https://chromium-i18n.appspot.com/ssl-address
address = Address(street="Im Mediapark 4a", postal_code="50670", city="Köln")

# now create a geocoder instance
geocoder = Geocoder(host=os.getenv("GEOCODER_HOST"))

# get long/lat values
res = geocoder.coordinates(address)
print(res) # Geopoint(latitude=50.94832, longitude=6.9454159)

# if you enter an address that doesn't exist or can't be found, then currently None is returned.
```