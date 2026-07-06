from patterns import *

"""
Prepare raw data for extraction.
    - Convert text to a list of strings (each representing a line).
    - Extract table data only.
"""

def open_file(file_path):
    """ Extract all text and store into a list of strings
        each representing a line in the document.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = [line.strip() for line in f if line]

    return content

def clean_text(text):
    """ Clean raw text by removing spaces and unnecessary photos
    """
    cleaned_text = []

    for line in text:
        # Remove anything after the Disclaimer (photos)
        if "Disclaimer" in line:
            break

        # Add line to list of text
        if line:
            cleaned_text.append(line)

    return cleaned_text

def extract_table_text(text):
    """ Extract ONLY text that is associated with a table
        or a table header (remove everything else).
    """
    table_text = []

    for line in text:
        # Remove all ##
        line = line.replace("#", "").strip()

        # End loop if last table has been processed
        if END_OF_TABLES.search(line):
            break

        # Check if line is table header
        if SPECIMEN_HEADER.search(line) or REGION_HEADER.search(line):
            table_text.append(line)

        # Check if line is table row
        elif "|" in line:
            table_text.append(line)

    cleaned_table_text = clean_table_text(table_text)

    # Return cleaned table text
    return cleaned_table_text

def clean_table_text(table_text):
    """ Clean table text by removing spaces, unnecessary photos,
        special characters, etc.
    """
    cleaned_table_text = []

    # Iterate through list and remove whitespace and special characters
    # OUTPUT : ["Viability", "94.00"]
    for line in table_text:
        # Check if row contains alphanumeric characters (remove -----)
        if not any(char.isalnum() for char in line):
            continue

        # Remove outer and inner pipes
        line = line.replace("|", " ")

        # Remove all # (special characters)
        line = line.replace("#", "")

        # Collapse multiple spaces into one space
        line = re.sub(r"\s+"," ", line).strip()

        cleaned_table_text.append(line)

    return cleaned_table_text

def extract_all_text(file_path):
    """ Extract all text and store into a list of strings
        each representing a line in the document. """

    raw_text = open_file(file_path)
    text = clean_text(raw_text)

    return text