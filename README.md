# Flow Cytometry Data Extractor

Extract data from flow cytometry PDFs and store in an Excel sheet.

## Description

The following code converts flow cytometry PDFs to Markdown and JSON formats. Patient metadata,
sample data, and table data are extracted from the Markdown files and stored in a neatly
formatted Excel Spreadsheet.

## Getting Started

### Dependencies

Install the required packages:
```bash
pip install docling
pip install pandas
```
OR
```bash
pip install -r requirements.txt
```

### Python Version
This project requires Python 3.12.

### Installing

Clone the repository:
```bash
git clone https://github.com/kaylakim987/Flow_Cytometry_Extractor.git

# Navigate to the source code
cd Flow_Cytometry_Extractor
cd src
```

Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Executing the Program

The program can be executed in two separate steps:
   
1. Convert PDF to Markdown
```bash
python convert_to_text.py -d <directory-containing-pdfs> -np <number-of-processors-to-use>
```
EXAMPLE:
```bash
python convert_to_text.py -d C:\Users\kkim\Desktop\samples\FlowReports_JTCC -np 1
```
An output folder named "Converted" will be generated in the specified input folder.
The path to the "Converted" folder can be passed as an argument in the next step.

* **When running the program in an IDE (PyCharm or VScode) only use 1 PROCESSOR**

2. Extract data from Markdown
```bash
python main.py -d <directory-containing-markdown-files>
```
The output file `ALL_PATIENTS_FlowCytometry.csv` will be written to the specified 
input directory.

EXAMPLE: 
```bash
python main.py -d C:\Users\username\Documents\FlowReports
```



