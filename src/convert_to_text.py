# convert_to_text.py

import argparse
import tempfile
from pathlib import Path
from multiprocessing import Pool
from pypdf import PdfReader, PdfWriter
from docling.document_converter import DocumentConverter

"""
Takes a directory, finds PDFs within that directory 
then converts to markdown formats.
"""

# EXAMPLE COMMAND TO RUN: python3 convert_to_text.py -d /mnt/storage/kayla/flow_cyto/pdfs -np 20
# FOR DESKTOP (PYCHARM) : python convert_to_text.py -d C:\Users\kkim\Desktop\samples\FlowReports_JTCC -np 1

# python3 convert_to_text.py -d /mnt/storage/kayla/Normal_Flow/FlowReports_JTCCC/Normal -np 10

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

def split_pdf(pdf_path, pages_per_chunk=2):
    """ Split large PDFs into smaller temporary PDFs.
        Returns a list of PDF paths.
    """
    reader = PdfReader(pdf_path)
    chunks = []

    temp_dir = Path(tempfile.mkdtemp())

    for start in range(0, len(reader.pages), pages_per_chunk):
        writer = PdfWriter()

        for page in range(start, min(start + pages_per_chunk, len(reader.pages))):
            writer.add_page(reader.pages[page])

        chunk_path = temp_dir / f"{pdf_path.stem}_part_{start//pages_per_chunk + 1}.pdf"

        with open(chunk_path, "wb") as f:
            writer.write(f)

        chunks.append(chunk_path)

    return chunks


def convert_single_pdf(pdf_path):
    """ Convert a single PDF to Markdown."""
    result = converter.convert(pdf_path)

    if hasattr(result.document, "export_to_markdown"):
        return result.document.export_to_markdown()
    else:
        return result.document.export_to_text()


def convert_pdf(pdf_path):
    global converter, output_root

    temp_files = []

    try:
        # Create a flat output directory
        output_root.mkdir(parents=True, exist_ok=True)

        reader = PdfReader(pdf_path)

        if len(reader.pages) > 2:
            pdf_parts = split_pdf(pdf_path)
            temp_files = pdf_parts
        else:
            pdf_parts = [pdf_path]

        markdown_parts = []

        for i, part in enumerate(pdf_parts):
            print(f"Processing chunk {i} of {len(pdf_parts)}")
            markdown_parts.append(
                convert_single_pdf(part))

        # Combine all components into a single markdown file
        content = "\n\n".join(markdown_parts)

        output_path = output_root / f"{pdf_path.stem}.md"

        output_path.write_text(content, encoding="utf-8")

        return f"CONVERTED: {pdf_path}"

    except Exception as e:
        return f"ERROR CONVERTING: {pdf_path} -> {e}"

    finally:
        # Remove temp files
        for temp in temp_files:
            temp.unlink(missing_ok=True)

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