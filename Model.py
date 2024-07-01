import cv2
import pytesseract
import json
import csv

def preprocess_image(image):
   
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh

def correct_ocr_errors(content):
    corrections = {
        '$20': 'S20',
        '$22': 'S22',
        'Vom': 'UOM',
        'Quote': 'Position',
        'Ord': 'Quantity',
        'Item': 'Vendor Name',
        'Description': 'Model Name',
        'Price': 'Unit Price'
    }
    return corrections.get(content, content)


def get_row_id(y):
    if 1200 <= y <= 1205:
        return 1
    elif y == 1313:
        return 2
    elif y == 1530:
        return 3
    else:
        return None 

def get_column_id(x):
    if 250 < x < 320:
        return 1
    elif 450 < x < 520:
        return 2
    elif 720 < x < 740:
        return 3
    elif 800 < x < 830:
        return 3
    elif 950 < x < 1140:
        return 4
    elif 1140 < x < 1240:
        return 5
    elif 1700 < x < 1850:
        return 6
    else:
        return None  


def image_to_ocr_json(image_path):
    img = cv2.imread(image_path)

    img = preprocess_image(img)
    
    custom_config = r'--oem 1 --psm 3'  
    ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config=custom_config)

    json_output = []

    for i in range(len(ocr_data['text'])):
        x = ocr_data['left'][i]
        y = ocr_data['top'][i]
        w = ocr_data['width'][i]
        h = ocr_data['height'][i]
        content = ocr_data['text'][i].strip()

        if content == '':
            continue

        content = correct_ocr_errors(content)
        row_id = get_row_id(y)
        
        if row_id is None:
            continue

        column_id = get_column_id(x)

        if column_id is None:
            continue

        if row_id == 1:
            is_header = True
        else:
            is_header = False

        json_obj = {
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "content": content,
            "row_id": row_id,
            "column_id": column_id,
            "is_header": is_header
        }
        json_output.append(json_obj)

    return json_output


if __name__ == "__main__":
    image_path = 'samsung.png' 
    output_json = image_to_ocr_json(image_path)

    
    with open('ocr_updated_model.json', 'w') as m:
        json.dump(output_json, m, indent=2)
 
def json_to_csv(output_json, csv_filename):

    data_rows = {}

 
    headers = []
    for item in output_json:
        if item["is_header"]:
            headers.append(item["content"])

    for item in output_json:
        if not item["is_header"]:
            row_id = item["row_id"] - 1  
            if row_id not in data_rows:
                data_rows[row_id] = [""] * len(headers)

            column_id = item["column_id"] - 1 
            data_rows[row_id][column_id] = item["content"]

    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(headers)

        for row_id in sorted(data_rows.keys()):
            writer.writerow(data_rows[row_id])
            
if __name__ == "__main__":
    input_json_file = 'ocr_updated_model.json'  
    output_csv_file = 'samsung_final_model.csv'  

    with open(input_json_file, 'r') as p:
        output_json = json.load(p)

    json_to_csv(output_json, output_csv_file)
  
    print('CSV file creation is a success')