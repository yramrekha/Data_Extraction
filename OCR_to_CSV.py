import csv
import json

def json_to_csv(output_json, csv_filename):
    # creating kinda of a dictionary to hold the data rows
    data_rows = {}

    # Extract headers from JSON where is_header is true
    headers = []
    for item in output_json:
        if item["is_header"]:
            headers.append(item["content"])

    # next we focus on rows of data from the json file where is_header is false
    for item in output_json:
        if not item["is_header"]:
            row_id = item["row_id"] - 1  
            if row_id not in data_rows:
                data_rows[row_id] = [""] * len(headers)

            column_id = item["column_id"] - 1 
            data_rows[row_id][column_id] = item["content"]

    # this is where we open the csv file for writing
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # making sure the headers are followed by the data as per the row_id
        writer.writerow(headers)

        # Write rows of data sorted by row_id
        for row_id in sorted(data_rows.keys()):
            writer.writerow(data_rows[row_id])

#used the previous ocr file created and converting to csv
if __name__ == "__main__":
    input_json_file = 'ocr_updated.json'  
    output_csv_file = 'samsung_final.csv'  

    with open(input_json_file, 'r') as p:
        output_json = json.load(p)

    json_to_csv(output_json, output_csv_file)
    # the last part is to understand if the script run and was completed
    #print('CSV file creation is a success')
