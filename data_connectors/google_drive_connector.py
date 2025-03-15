from dotenv import load_dotenv
import os
import json
import tempfile
from googleapiclient.discovery import build
from google.oauth2 import service_account
from pypdf import PdfReader

# Load environment variables from .env
load_dotenv()


class GoogleDriveConnector:
    def __init__(self, service_account_file: str, user_email: str):
        self.service_account_file = service_account_file
        self.user_email = user_email
        self.service = self._authenticate()

    def _authenticate(self):
        """Authenticate using the service account and impersonate the specified user."""
        creds = service_account.Credentials.from_service_account_file(
            self.service_account_file,
            scopes=["https://www.googleapis.com/auth/drive.readonly"],
        )
        delegated_creds = creds.with_subject(self.user_email)
        service = build("drive", "v3", credentials=delegated_creds)
        return service

    """
    FETCH ONLY 1 GDRIVE DOCUMENT FOR DEMO BY LATEST UPLOADED
    """
    def list_pdf_files(self):
        response = (
            self.service.files()
            .list(
                pageSize=1, 
                q="mimeType='application/pdf'",
                fields="files(id, name, mimeType, createdTime)",
                orderBy="createdTime desc", 
            )
            .execute()
        )

        return response.get("files", [])[:1]

    def download_file(self, file_id, file_path, file_name):
        """Download a file from Google Drive."""
        print(f"Downloading file: {file_name}...")
        request = self.service.files().get_media(fileId=file_id)
        with open(file_path, "wb") as file:
            file.write(request.execute())
        print(f"Download complete: {file_name}")

    def extract_text_from_pdf(self, file_path, file_name):
        """Extract text from a PDF file using PyPDF."""
        print(f"Extracting text from: {file_name}...")
        with open(file_path, "rb") as file:
            reader = PdfReader(file)
            text = "\n".join([page.extract_text() or "" for page in reader.pages])
        print(f"Extraction complete: {file_name}")
        return text

    def process_pdfs(self):
        """Download and extract text from PDFs."""
        pdf_files = self.list_pdf_files()
        extracted_texts = {}

        for file in pdf_files:
            file_id = file["id"]
            file_name = file["name"]

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_path = temp_file.name

            try:
                self.download_file(file_id, temp_path, file_name)
                text = self.extract_text_from_pdf(temp_path, file_name)
                extracted_texts[file_name] = text
            finally:
                os.remove(temp_path)  # Ensure temp file is deleted

        return extracted_texts

    def save_extracted_text(self, extracted_data, output_file="gdrive_results.json"):
        """Save extracted text into a JSON file."""
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(extracted_data, f, indent=4, ensure_ascii=False)
        print(f"Extracted text saved to {output_file}")


if __name__ == "__main__":
    SERVICE_ACCOUNT_FILE_PATH = os.getenv("SERVICE_ACCOUNT_FILE_PATH")
    DELEGATED_USER_EMAIL = os.getenv("DELEGATED_USER_EMAIL")

    connector = GoogleDriveConnector(SERVICE_ACCOUNT_FILE_PATH, DELEGATED_USER_EMAIL)
    extracted_pdfs = connector.process_pdfs()

    # Save the extracted text into a JSON file
    connector.save_extracted_text(extracted_pdfs)

    print(f"Processed {len(extracted_pdfs)} PDFs. Check gdrive_results.json for results.")
