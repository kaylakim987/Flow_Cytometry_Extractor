# convert_to_text.py

import argparse
import json
from pathlib import Path
from docling.document_converter import DocumentConverter
from multiprocessing import Pool

"""
Takes a directory, finds PDFs within that directory 
then converts to markdown formats.
"""

# EXAMPLE COMMAND TO RUN: python3 convert_to_text.py -d /mnt/storage/kayla/flow_cyto/pdfs -np 20
# FOR DESKTOP (PYCHARM) : python convert_to_text.py -d C:\Users\kkim\Desktop\samples\FlowReports_JTCC -np 2

# Initialize global converter and output directory
converter = None

def init_worker(output_dir):
    """ Initialize Docling converter once per process
    """
    global converter, output_root

    converter = DocumentConverter()
    output_root = Path(output_dir)

def list_pdfs(root_dir):
    """ Return a list of PDFs in the output folder.
    """
    return list(root_dir.rglob("*.pdf"))

def convert_pdf(pdf_path):
    global converter, output_root

    try:
        result = converter.convert(pdf_path)

        # Create a flat output directory
        output_root.mkdir(parents=True, exist_ok=True)

        # Generate markdown output (fallback to text if markdown not available)
        if hasattr(result.document, "export_to_markdown"):
            content = result.document.export_to_markdown()
        else:
            content = result.document.export_to_text()

        output_path = output_root / f"{pdf_path.stem}.md"

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
                        type=int,
                        default=1,
                        help="Number of processes to use.")

    return parser.parse_args()

def main():
    args = get_args()

    root_dir = Path(args.directory)

    # Output directory
    output_dir = root_dir / "Converted"
    output_dir.mkdir(parents=True, exist_ok=True)

    pdfs = list_pdfs(root_dir)

    with Pool(
        processes=args.num_processes,
        initializer=init_worker,
        initargs=(output_dir,)
    ) as pool:
        for msg in pool.imap_unordered(convert_pdf, pdfs):
            print(msg)


if __name__ == "__main__":
    main()