# extract_metadata.py

import pandas as pd
from patterns import *

""" 
Extract patient and sample metadata from text :
name, dob, mrn, inerpretation, specimen type, collection date 
"""

# EXTRACTING PATIENT METADATA
def extract_patient_data(text):
    """ Extracts patient MRN, Name, and DOB from text data """

    mrn = dob = name = None

    for i, line in enumerate(text):
        name_match = NAME.search(line)
        dob_match = DOB.search(line)

        if "medical record" in line.lower():
            mrn_match = MRN.search(line)
            if mrn_match:
                mrn = mrn_match.group(1)
            elif i + 1 < len(text):
                next_line = text[i + 1]
                mrn_match = re.search(r"(\d+)", next_line)
                if mrn_match:
                    mrn = mrn_match.group(1)

        if name_match:
            name = re.sub(r"[^a-zA-Z0-9.,\-\s]", "", name_match.group(1)).strip()

        if "DOB" in line and dob_match:
            dob = pd.to_datetime(
                dob_match.group(),
                errors='coerce'
            ).strftime("%m-%d-%Y")

        # Check if values are already found
        if mrn and dob and name:
            break

    return mrn, name, dob

# EXTRACTING SAMPLE COLLECTION DATE
def extract_collection_data(text):
    """ Extracts collection data of sample from text data. """
    collection_date = None

    for line in text:
        date_match = COLLECTION_DATE.search(line)
        if date_match:
            collection_date = pd.to_datetime(
                date_match.group(1),
                errors='coerce'
            ).strftime("%m-%d-%Y")

            # Break out of loop if date is found
            break

    return collection_date

# EXTRACT INTERPRETATION
def extract_interpretation_(text):
    """ Extract interpretation of sample from text data. """
    interpretation = None

    # Extract from Interpretation to (electronic signature)
    start_idx = next(
        (i for i in range(len(text))
        if INTERPRETATION_START.search(text[i])),
        None)

    end_idx = next(
        (i for i in range(len(text))
        if INTERPRETATION_END.search(text[i])),
        None)

    if start_idx is not None and end_idx is not None:
        interpretation = text[start_idx:end_idx]

        # Remove all '#' characters and join into a single string
        interpretation = " ".join(interpretation).replace("#", "")

        # Remove the word interpretation and any extra spaces
        interpretation = re.sub(r"interpretation", "", interpretation, flags=re.IGNORECASE)
        interpretation = interpretation.strip()

    return interpretation

# GENERATING UPID
def generate_upid(name, dob):
    """ Generate UPID.1 for each patient. """
    # Take the first 3 letters for first and last name
    last, first = [part.strip()[:3] for part in name.split(",")]

    # UPID = last,first,dob
    upid = f"{last},{first},{dob}"

    return upid

def extract_metadata(text):
    """ Main driver function for extracting metadata."""

    # Extracting all patient and sample data
    mrn, name, dob = extract_patient_data(text)
    collection_date = extract_collection_data(text)
    interpretation = extract_interpretation_(text)
    upid = generate_upid(name, dob)

    return upid, mrn, name, dob, collection_date, interpretation
