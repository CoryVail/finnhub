## Description

The `main.py` script will get the financials for a company using the Finnhub API, and then insert the data into a SQLite database.

## Usage

The `main.py` script takes one required argument and one optional argument.

The `-s` or `--symbol` argument is required and is the stock symbol of the company for which you want to get financials.

The `--replace` argument is optional and will delete all database records for the company (specified by the `-s` or `--symbol` argument) prior to retrieving the data from Finnhub.

## Examples

Get financials for USAC:

```
python3 main.py -s USAC
```

Get financials for USAC and replace all previous database records for USAC:

```
python3 main.py -s USAC --replace
```
