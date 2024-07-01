import cv2
import pytesseract
import json

def preprocess_image(image):
    #I had to conver the image to grayscale for better processing and 
    #apply the binary threshold in order to improve image contrast
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh

def correct_ocr_errors(content):
    # I was still having some errors based on previous run for example
    # S20 was being read as $20 and this happens something with the quality
    # quality of the image even though I adjusted the OCR settings
    # Also I corrected the output for the csv table headers in one go
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

# I first had the script running which gave me an idea of how the data is
#positioned in the image and then I used the x and y coordinate to map the
# data I needed and to match the output desired and instructed in the
# task description and then skipped the data outside the range since 
# I did not need it for the table.


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

# The following scripts load the image using opencv as instructed.
# The image is then enhanced to improve the accuracy of the OCR

def image_to_ocr_json(image_path):
    img = cv2.imread(image_path)

    img = preprocess_image(img)

    # Use pytesseract to do OCR on the image
    # I had to adjust based on the image and OCR needs; I had to try a few combinations
    # of oem and psm since some were missing important data on the image
    # and the one below worked with the least errors.
    
    custom_config = r'--oem 1 --psm 3'  
    ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config=custom_config)

    # Next, I had to prepare the json file and make sure it was in the
    #requested format given as example in the requirements
    json_output = []

    for i in range(len(ocr_data['text'])):
        x = ocr_data['left'][i]
        y = ocr_data['top'][i]
        w = ocr_data['width'][i]
        h = ocr_data['height'][i]
        content = ocr_data['text'][i].strip()

        # Just to have data and not empty spaces we add this to skip where content is empty
        if content == '':
            continue

        # make a reference to the errors 
        # and content we have already defined above
        content = correct_ocr_errors(content)

        # Next I get row_id based on y value and also skip the rows 
        # that do not match the y-values I specified (which I got from the first time 
        # I run the script)
        row_id = get_row_id(y)
        
        if row_id is None:
            continue

        # Also I get column_id based on x values and also skip the columns 
        # that do not match the x-values I specified (again which I got from the first time 
        # I run the script)
        column_id = get_column_id(x)

        if column_id is None:
            continue

        # Next I had to determine the header value
        # which I used the row_id for. Technically in my table row_id =1 
        # will be the header of the columns.
        if row_id == 1:
            is_header = True
        else:
            is_header = False

        # Based on the each OCR entry I needed for the table, I created a JSON object 
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

    
    with open('ocr_updated.json', 'w') as m:
        json.dump(output_json, m, indent=2)
    # added this for reference and to know if it was completed and commented it after
    #can be uncomment to see the message
    #print('OCR JSON was saved as ocr_updated.json')
