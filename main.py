import argparse
import csv
import finnhub
import sqlite3


def main():
    # Get CLI args.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--symbol',
        type=str,
        required=True,
        help="The stock symbol of the company",
    )
    parser.add_argument(
        '--replace',
        action='store_true',
        help="Replace all existing records for the company (if specified)",
    )
    args = parser.parse_args()

    # Try to clean for SQL injections.
    symbol = args.symbol.split(";")[0].strip()

    # Create a new Client object.
    c = finnhub.Client(api_key="sandbox_c620d3aad3iccpc4ang0")
    # Get the financials.
    financials = c.financials(symbol, 'ic','quarterly')

    # Programmatically add columns to the database
    # based on what the Client object contains.
    # First, get the column names.
    columns = []
    for dict in financials['financials']:
        for key, value in dict.items():
            if key not in columns:
                columns.append(key)
    print(f"Columns: {columns}")

    # Loop through financials and add to database.
    data = list(columns)
    for dict in financials['financials']:
        values = []
        for column in columns:
            if column in dict:
                values.append(dict[column])
        data.append(values)
    with open('test.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(data)

if __name__ == "__main__":
    main()
