import os
import json
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# Initialize Presidio
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# Detect all possible PII entities supported by Presidio
entities = [
    "PHONE_NUMBER", "CREDIT_CARD", "SSN", "IP_ADDRESS",
    "NRP", "IBAN_CODE", "US_BANK_NUMBER", "US_DRIVER_LICENSE", "US_PASSPORT",
    "US_SSN",
]

def remove_pii(text):
    """Detect and remove PII from the given text using default Presidio settings."""
    if not isinstance(text, str):  # Ensure text is a string
        return text  

    results = analyzer.analyze(text=text, entities=entities, language="en")
    
    if not results:  # If no PII is detected, return the original text
        return text

    anonymized_text = anonymizer.anonymize(text=text, analyzer_results=results)
    return anonymized_text.text

def sanitize_file(file_path, sanitize_func):
    """Check if the file exists before sanitizing."""
    if not os.path.exists(file_path):
        print(f"Skipping: {file_path} (file not found)")
        return

    sanitize_func(file_path)

def sanitize_gmail_results(file_path):
    """Sanitize PII from values in gmail_results.json while keeping keys (filenames) unchanged."""
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, dict):  # If JSON is a dictionary (expected format)
        sanitized_data = {key: remove_pii(value) if isinstance(value, str) else value for key, value in data.items()}

    elif isinstance(data, list):  # If JSON is a list (unexpected format)
        sanitized_data = [
            {key: remove_pii(value) if isinstance(value, str) else value for key, value in item.items()}
            for item in data
        ]

    else:
        raise ValueError(f"Unexpected JSON format in {file_path}")

    # Overwrite the original file with sanitized data
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(sanitized_data, file, indent=4)

    print(f"Sanitized and updated: {file_path}")
    
def sanitize_slack_messages(file_path):
    """Sanitize PII from values in slack_messages.json."""
    with open(file_path, "r", encoding="utf-8") as file:
        messages = json.load(file)

    # Iterate through each message and remove PII from values only
    sanitized_messages = [
        {key: remove_pii(value) if isinstance(value, str) else value for key, value in message.items()}
        for message in messages
    ]

    # Overwrite the original file with sanitized data
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(sanitized_messages, file, indent=4)

    print(f"Sanitized and updated: {file_path}")
    
def sanitize_gdrive_results(file_path):
    """Sanitize PII from values in gdrive_results.json while keeping keys (filenames) unchanged."""
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):  # Ensure it is a dictionary
        raise ValueError(f"Unexpected JSON format in {file_path}")

    sanitized_data = {key: remove_pii(value) if isinstance(value, str) else value for key, value in data.items()}

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(sanitized_data, file, indent=4)

    print(f"Sanitized and updated: {file_path}")

# Run the sanitization process only if files exist
sanitize_file("gmail_results.json", sanitize_gmail_results)
sanitize_file("slack_messages.json", sanitize_slack_messages)
sanitize_file("gdrive_results.json", sanitize_gdrive_results)

print("Sanitization process completed.")
