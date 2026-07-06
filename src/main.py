# main.py

import argparse
from preprocess import extract_all_text, extract_table_text
from extract_metadata import extract_metadata
from extract_table_data import extract_specimen_type, extract_flow_data, extract_reference_table
from pathlib import Path
import pandas as pd

# EXAMPLE COMMAND TO RUN: python3 main.py -d /mnt/storage/kayla/flow_cyto/out

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-d',
                        '--directory',
                        help="Path to directory containing PDFs and converted txt files.")

    return parser.parse_args()

def process_file(file_path):
    """ Process each markdown file and return a list of
        dictionaries for each PDF file.
        ( One marker per row )
    """
    text = extract_all_text(file_path)

    # Extracting sample and patient metadata
    upid, mrn, name, dob, collection_date, interpretation = extract_metadata(text)

    # Extracting table text only
    table_text = extract_table_text(text)

    # Extracting data from tables
    specimen_type = extract_specimen_type(table_text)
    ref_table = extract_reference_table(table_text)
    flow_data = extract_flow_data(table_text)

    # Flow Data Present
    flow_present = 3 if flow_data else 2

    full_data = []

    for row in flow_data:
        base_row = {
                "UPID.1" : upid,
                "PatientName" : name,
                "DOB" : dob,
                "MRN" : mrn,
                "FlowDataPresent" : flow_present,
                "SpecimenTypeFlow" : specimen_type,
                "CollectedDateFlow" : collection_date,
                "Interpretation" : interpretation}

        # Merge all parsed layers
        base_row.update(ref_table)
        base_row.update(row)

        full_data.append(base_row)

    return full_data

def traverse_directory(root_dir):
    """ Iterate through all Markdown files in root
        directory and process.
    """
    root_dir = Path(root_dir)

    # Iterate through folders in root directory
    md_files = root_dir.rglob('*.md')

    final_data = []

    # Process each PDF file
    for file_path in md_files:
        data = process_file(file_path)

        if data:
            final_data.extend(data)

    # Convert to dataframe and remove duplicate rows
    df = pd.DataFrame(final_data)
    df = df.drop_duplicates()

    # Ordering columns
    column_order = [
        "UPID.1",
        "PatientName",
        "DOB",
        "MRN",
        "FlowDataPresent",
        "SpecimenTypeFlow",
        "CollectedDateFlow",
        "Interpretation",
        "Marker",
        "Value(%)",
        "Intensity",
        "Gate"
    ]

    df = df[column_order + [c for c in df.columns if c not in column_order]]

    # Write to CSV file
    output_file = root_dir / "ALL_PATIENTS_FlowCytometry.csv"
    df.to_csv(output_file, index=False)

    print(f"Saved: {output_file}")

def main():
    args = get_args()

    # Iterate through root directory and process files
    traverse_directory(args.directory)


if __name__ == '__main__':
    main()