![PyPI - Python Version](https://img.shields.io/pypi/pyversions/blockfirates)

Scrape the latest APY rates for BlockFi Interest Accounts

# DISCLAIMER

This package is in no way affiliated in any way, shape or form with BlockFi and as such its use is entirely at the user's own risk.

# BlockFiRates

An unofficial API to easily obtain the interest rates of [BlockFi Interest Accounts (BIA)](https://blockfi.com/rates/).

# Getting Started

### Installing
```
pip install blockfirates
```
### Imports
```
from blockfirates import client
Client=client.BlockFiRates()
```

## Available Functions
* get_all_rates
* get_info

## get_all_rates
Printing info for all currencies:
```
rates = Client.get_all_rates()
for i in rates:
    print(i)
```

## get_info
Standard usage returns values for the "US" and for Tier 1:
```
Client.get_info(symbol="BTC")
```

To get non-US info (i.e. "row" values):
```
Client.get_info(symbol="BTC", category="row")
```

To get info about other tiers:
```
Client.get_info(symbol="BTC", tier=2)
```


### Development
Create a virtual environment using [virtualenv](https://pypi.org/project/virtualenv/), activate it and install necessary dependencies:
```
python -m virtualenv env
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements_dev.txt
pip install -e .
```
Once changes have been committed, create and merge to the master branch on Github and push the new version to PyPi:
```
git push -u origin master

python -m build

twine check dist/*

twine upload dist/* -u $PYPI_USERNAME -p $PYPI_PASSWORD
```
