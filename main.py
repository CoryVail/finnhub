import argparse
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

    # Connect to the database.
    con = sqlite3.connect('finnhub.db')
    cur = con.cursor()
    # Create the table if it doesn't exist.
    cur.execute("CREATE TABLE IF NOT EXISTS finnhub (symbol text)")
    # Delete the rows for the provided symbol if the user asked for it.
    if args.replace:
        cur.execute(f"DELETE FROM finnhub WHERE symbol = :symbol", {
            'symbol': symbol,
        })
    # Save the changes.
    con.commit()

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

    # Second, check if each column exists and add them if they don't exist.
    for column in columns:
        print(f"Looking for column: {column}")
        try:
            cur.execute(f"SELECT {column} FROM finnhub")
        except sqlite3.OperationalError as error:
            if "no such column" in str(error):
                cur.execute(f"ALTER TABLE finnhub ADD COLUMN {column} text")
                con.commit()
                print(f"Couldn't find column '{column}', so I added it.")

    # Loop through financials and add to database.
    for dict in financials['financials']:
        print(f"Added period '{dict['period']}' for '{symbol}'")
        cur.execute(f"INSERT INTO finnhub (symbol, period) values (:symbol, :period)", {
            'symbol': symbol,
            'period': dict['period'],
        })
        con.commit()
        for key, value in dict.items():
            # Skip the 'period' column since we already inserted it.
            if key == "period":
                continue
            print(f"Updated '{key}' = '{value}' for '{symbol}' on period '{dict['period']}'")
            cur.execute(f"UPDATE finnhub SET {key} = {value} WHERE symbol = :symbol AND period = :period", {
                'symbol': symbol,
                'period': dict['period'],
            })
            con.commit()

    # Close the database connection.
    con.close()

if __name__ == "__main__":
    main()
