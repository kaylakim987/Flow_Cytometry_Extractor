# convert_to_text.py

import argparse
import json
from pathlib import Path
from docling.document_converter import DocumentConverter
from multiprocessing import Pool

"""
Takes a directory, finds PDFs within that directory 
then converts to json and markdown formats.
"""

# EXAMPLE COMMAND TO RUN: python3 convert_to_text.py -d /mnt/storage/kayla/flow_cyto/pdfs -np 20
# FOR DESKTOP (PYCHARM) : python3 convert_to_text.py -d C:\Users\kkim\Desktop\samples\FlowReports_JTCC -np 2

# Initialize global converter
converter = None

def init_worker():
    """ Initialize Docling converter once per process
    """
    global converter
    converter = DocumentConverter()

def list_pdfs(root_dir):
    """ Return a list of PDFs in the output folder.
    """
    return list(root_dir.rglob("*.pdf"))

def convert_pdf(pdf_path):
    global converter

    try:
        result = converter.convert(pdf_path)

        # Convert to json
        data = result.document.export_to_dict()
        print(data) # Remove print later on
        json_path = pdf_path.with_suffix(".json")
        json_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

        # Generate markdown output (fallback to text if markdown not available)
        if hasattr(result.document, "export_to_markdown"):
            content = result.document.export_to_markdown()
        else:
            content = result.document.export_to_text()

        output_path = pdf_path.with_suffix(".md")

        output_path.write_text(content, encoding="utf-8")

        return f"CONVERTED: {pdf_path}"

    except Exception as e:
        return f"ERROR CONVERTING: {pdf_path} -> {e}"


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-d',
                        '--directory',
                        help="Path to directory containing PDFs and converted txt files.")

    parser.add_argument('-np',
                        '--num_processes',
                        help="Number of processes to use.")

    return parser.parse_args()

def main():
    args = get_args()

    root_dir = Path(args.directory)
    pdfs = list_pdfs(root_dir)

    workers = int(args.num_processes)

    # Concurrently convert all documents
    with Pool(processes=workers, initializer=init_worker) as pool:
        for msg in pool.imap_unordered(convert_pdf, pdfs):
            print(msg)

if __name__ == "__main__":
    main()