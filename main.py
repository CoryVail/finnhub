import argparse
import csv
import finnhub
import xlsxwriter


def create_csv(client, symbol, type):
    # Get the financials.
    financials = client.financials(symbol, type, 'quarterly')

    # Isolate the column names from the Client response.
    columns = []
    for dict in financials['financials']:
        for key, value in dict.items():
            if key not in columns:
                columns.append(key)
    print(f"Columns: {columns}")

    # Loop through financials and add to CSV.
    data = []
    for dict in financials['financials']:
        values = []
        for column in columns:
            if column in dict:
                values.append(dict[column])
            else:
                values.append('')
        data.append(values)

    with open(f"{symbol}_{type}.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        writer.writerows(data)

def main():
    # Get CLI args.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--symbol',
        type=str,
        required=True,
        help="The stock symbol of the company",
    )
    args = parser.parse_args()

    # Get the stock symbol.
    symbol = args.symbol.split(";")[0].strip()

    # Create a new Client object.
    c = finnhub.Client(api_key="c63bv9qad3id43aa47t0")

    # Create the CSVs.
    types = ['cf', 'ic', 'bs']
    for type in types:
        create_csv(c, symbol, type)

    # Create the Excel file.
    workbook = xlsxwriter.Workbook(f"{symbol}.xlsx")
    for type in types:
        row = 0
        with open(f"{symbol}_{type}.csv", 'r') as file:
            worksheet = workbook.add_worksheet(type)
            for line in file.readlines():
                col = 0
                for item in line.split(","):
                    worksheet.write(row, col, item)
                    col += 1
                row += 1

    workbook.close()

if __name__ == "__main__":
    main()
