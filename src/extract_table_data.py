# extract_table_data.py

from patterns import *

""" 
Extract all table data (reference and flow cytometry tables).
"""

def extract_specimen_type(table_text):
    """ Extract specimen type from table text. """
    specimen_type = None

    # Iterate through table rows and look for "Specimen Data:"
    for row in table_text:
        specimen_match = SPECIMEN_HEADER.search(row)
        if specimen_match:
            specimen_type = specimen_match.group(1).strip()
            break

    return specimen_type

def extract_reference_table(table_text):
    """ Extract table containing viability and percentages
        ex. (Granulocyte (%), Lymphocyte (%), etc.) """

    # Dictionary to store reference table data
    ref_table = {}

    # Variable for first valid row and end condition
    in_table = False

    for row in table_text:
        # Filter for rows that start with Viability or end in Region
        row_match = REFERENCE_ROW.search(row)

        # End condition (row_match is False and in_table is True)
        if not row_match:
            if in_table:
                break
            continue

        in_table = True

        # Extract region and value %
        region = row_match.group(1).strip()
        raw_value = row_match.group(2).strip()

        # Account for floats and ints for value
        value = float(raw_value) if "." in raw_value else int(raw_value)

        # Add region : value to dictionary
        ref_table[f"{region}(%)"] = value

    return ref_table

def split_gates(table_text):
    """ Separate tables based on gate/region types. """
    # Structure of blocks:
    # ex. blocks["Blast"] = [list of rows associated with Blast region]
    blocks = {}
    current = None

    for row in table_text:
        # Find table header
        if REGION_HEADER.search(row):
            # Excluding marker
            current = re.sub(r"region\s*:?|marker|\s+", " ", row, flags=re.I).strip()

            # Remove duplicate words
            parts = current.split()
            parts = list(dict.fromkeys(parts))
            current = " ".join(parts)

            # Create a new entry if the region is not already in dict.
            if current not in blocks:
                blocks[current] = []
            continue

        # Ignore marker, value, intensity row
        if SKIP_HEADERS.search(row):
            continue

        # Add table rows to corresponding gate
        if current:
            blocks[current].append(row)

    return blocks

def parse_flow_data(rows, gate):
    """ Parse flow cytometry table. """
    table = []

    # Parse data in each row
    for line in rows:
        match = ROW.search(line)

        if match:
            marker = match.group(1).strip()
            value = float(match.group(2))
            intensity = match.group(3).strip() if match.group(3) else None

            table.append({"Marker": marker,
                          "Value(%)": value,
                          "Intensity": intensity,
                          "Gate": gate})

    return table

def extract_flow_data(table_text):
    """ Control the workflow of flow cytometry
        table extraction. """
    blocks = split_gates(table_text)

    # List of dictionaries with the following structure:
    # flow_data = [{"Marker":marker, "Value(%)":value, etc.}]
    flow_data = []

    # Extend flattens into a singular list (no nesting)
    for gate, rows in blocks.items():
        flow_data.extend(parse_flow_data(rows, gate))

    return flow_data
