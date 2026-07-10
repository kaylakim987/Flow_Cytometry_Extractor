# rename_files.py

from pathlib import Path

def abbreviate_type(specimen_type):
    """ Abbreviate specimen type to the correct format
        EX. Bone Marrow -> BM """
    if "peripheral" in specimen_type.lower():
        return "PB"

    if "csf" in specimen_type.lower():
        return "CSF"

    return "BM"


def rename(file_path, root_dir, upid, collection_date, specimen_type):
    # Fix formatting for specimen type
    specimen_type = abbreviate_type(specimen_type)

    # Path to Markdown
    md_path = Path(file_path)

    # Find corresponding PDF path
    pdf_matches = list(root_dir.rglob(f"{md_path.stem}.pdf"))

    if pdf_matches:
        pdf_path = pdf_matches[0]

        # Defining the desired format
        new_base = f"{upid}_FlowColD {collection_date}_{specimen_type}"

        # Defining new name
        new_md = md_path.with_name(new_base + ".md")
        new_pdf = pdf_path.with_name(new_base + ".pdf")

        # Rename PDFs
        md_path.rename(new_md)
        pdf_path.rename(new_pdf)
