**Data Extraction**

This repository contains scripts and solutions for processing OCR data from images and converting it into CSV format. The project is broken into two main scripts to tackle the task efficiently. 

**Files and Structure**

1. `Model_OCR.py`
- Purpose: Reads the image and outputs a JSON file named `OCR_updated.json`.
- Description: This script was developed in two phases. Initially, it identifies the rough xy coordinates of the necessary data. In the second phase, it uses this information to extract and output the required data as specified in the task.

2. `OCR_to_CSV.py`
- Purpose: Converts the JSON file (`OCR_updated.json`) into a CSV file named `samsung_final.csv`.
- Description: This script processes the JSON output from `Model_OCR.py` and formats it into a structured CSV file.

3. `Model.py`
- Purpose: Combines the functionalities of `Model_OCR.py` and `OCR_to_CSV.py` to perform the entire task in one go.
- Description: This script merges the two separate processes into a single workflow, offering an alternative for those who prefer a unified approach.

**Future Improvements**
Considerations for future enhancements include:
- Combined CSV Script: Integrating a feature into `Model.py` that continuously adds data from new scanned invoices to the existing CSV file, updating it as necessary.

**Usage**
1. Running `Model_OCR.py` and `OCR_to_CSV.py` Separately:
    - Execute `Model_OCR.py` to generate `OCR_updated.json`.
    - Run `OCR_to_CSV.py` to convert the JSON output to `samsung_final.csv`.

2. Running `Model.py`:
    - Execute `Model.py` to perform the entire process in one go, from reading the image to generating the final CSV file.

**Conclusion**
These scripts provide a flexible approach to OCR data processing, allowing users to choose between a step-by-step method or an all-in-one solution. Detailed explanations and reasoning behind the code decisions are included within the scripts.
