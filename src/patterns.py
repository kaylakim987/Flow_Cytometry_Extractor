# patterns.py

import re

""" DEFINING ALL PATTERNS FOR EXTRACTING DATA """

# Patient Metadata
NAME = re.compile(r"Patient\s*:\s*(.*?)(?=\s*(?:Age\b|Medical\b|DOB\b|MRN\b|Location\b|$))", re.IGNORECASE)
MRN = re.compile(r"\s*Medical\s*Record\s*#?\s*:\s*(\d+)", re.IGNORECASE)
DOB = re.compile(r"\d{1,2}/\d{1,2}/\d{2,4}")

# Sample Metadata
COLLECTION_DATE = re.compile(r"Collected:\s*([0-9/]+)", re.IGNORECASE)

# Document Structure Markers
INTERPRETATION_START = re.compile(r"interpretation", re.IGNORECASE)
INTERPRETATION_END = re.compile(r"(electronic signature)", re.IGNORECASE)

# Table Detection Patterns
SPECIMEN_HEADER = re.compile(r"\s*Specimen\s*Data\s*:\s*(.*)", re.IGNORECASE)
END_OF_TABLES = re.compile(r"sample\s*processing\s*information", re.IGNORECASE)
REFERENCE_ROW = re.compile(r"^(Viability|.*Region)\s+(\d+(?:\.\d+)?)\s*$", re.IGNORECASE)

# Flow Table Detection Patterns
SKIP_HEADERS = re.compile(r"\b(marker|value\s*%?|intensity)\b", re.IGNORECASE)
ROW = re.compile(r"^(.*?)\s+(\d+(?:\.\d+)?)(?:\s+(.*))?$", re.IGNORECASE)
REGION_HEADER = re.compile(r"^(Region\s*:?\s*.+|[A-Za-z ]+\s+Region)$", re.IGNORECASE)