## Geocoder Python

### Usage

#### Step 1: Set environment variables

You will need to create an application in Auth0 or use an existing one.
Now copy the contents of `.env.example` to `.env` and set the evironment variables there, if you want to use `python-dotenv` to read in the required environment variables.
Otherwise set the following environment variables in your `$SHELL` however you want. They are:

```bash
export GEOCODER_HOST="<GEOCODER_HOST>"
export AUTH0_CLIENT_ID="<AUTH0_CLIENT_ID>"
export AUTH0_CLIENT_SECRET="<AUTH0_ZERO_CLIENT_SECRET>"
export AUTH0_SITE="<AUTH0_SITE>"
export AUTH0_AUDIENCE="<AUTH0_AUDIENCE>"
```

### Step 2: Install the package

Make sure you have [Poetry](https://python-poetry.org/docs/#installation) installed.

Now from the project root directory just run the following:

```bash
# install required libs
poetry install

# startup the virtualenv
poetry shell
```

Now you are good to go.

```python

# get geocoordinates for an address
from geocoder_studitemps import (
    Geocoder,
    Address,
    settings
)

# this will create and validate the format of an address, using
# the google i18 address api. see: https://chromium-i18n.appspot.com/ssl-address
address = Address(street="Im Mediapark 4a", postal_code="50670", city="Köln")

# We can also attempt to validate the address if we want to using the i18address API
# This can fail and will raise an InvalidAddress exception
address.validate()

# Now create a Geocoder instance. In general there are two flows
# 1) you can use an existing auth0 token (perhaps you have cached it)
# 2) Directly authenticate with auth0, get a new token and use that one.
# This example shows the second approach

g = Geocoder(settings)

# now authenticate and store the auth_token inside the Geocoder instance
# If authentication fails and exception will be raised.
g.authenticate()

# now we can make geocoding API calls

# get long/lat values
res = geocoder.coordinates(address)
print(res) # Geopoint(latitude=50.94832, longitude=6.9454159)

# if you enter an address that doesn't exist or can't be found,
# then currently None is returned and an Exception will not be raised.
```
