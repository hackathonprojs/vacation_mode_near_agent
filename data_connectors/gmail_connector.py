from dotenv import load_dotenv
import os
import json
import base64
from googleapiclient.discovery import build
from google.oauth2 import service_account


load_dotenv()


class GmailConnector:
    def __init__(self, service_account_file: str, delegated_user: str):
        self.service_account_file = service_account_file
        self.delegated_user = delegated_user
        self.service = self._authenticate()

    def _authenticate(self):
        """Authenticate using the service account and return the Gmail API service instance."""
        creds = service_account.Credentials.from_service_account_file(
            self.service_account_file,
            scopes=["https://www.googleapis.com/auth/gmail.readonly"],
        )
        delegated_creds = creds.with_subject(self.delegated_user)
        service = build("gmail", "v1", credentials=delegated_creds)
        return service

    """
    GET ONLY THE FIRST 3 EMAILS FOR DEMO
    """
    def fetch_emails(self, max_results=3):
        """Fetch the most recent emails from the inbox."""
        response = (
            self.service.users()
            .messages()
            .list(
                userId="me",
                maxResults=max_results
            )
            .execute()
        )
        return response.get("messages", []) 


    def get_email_details(self, message_id):
        """Retrieve the full details of an email by its ID."""
        email = (
            self.service.users()
            .messages()
            .get(userId="me", id=message_id, format="full")
            .execute()
        )
        headers = {h["name"]: h["value"] for h in email["payload"]["headers"]}
        body = ""

        if "parts" in email["payload"]:
            for part in email["payload"]["parts"]:
                if part["mimeType"] == "text/plain" and "body" in part:
                    data = part["body"].get("data")
                    if data:
                        body = base64.urlsafe_b64decode(data).decode("utf-8")
                        break

        return {
            "id": email["id"],
            "threadId": email["threadId"],
            "snippet": email["snippet"],
            "subject": headers.get("Subject", ""),
            "from": headers.get("From", ""),
            #"to": headers.get("To", ""),
            "date": headers.get("Date", ""),
            "body": body,
        }

    def fetch_all_emails_with_details(self, limit=None):
        """Fetch all emails and return detailed email information."""
        email_list = []
        messages = self.fetch_emails()

        for idx, msg in enumerate(messages):
            email_details = self.get_email_details(msg["id"])
            email_list.append(email_details)

            if limit and idx + 1 >= limit:
                break

        return email_list

    def save_emails_to_json(self, emails, output_file="gmail_results.json"):
        """Save the extracted emails into a JSON file."""
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(emails, f, indent=4, ensure_ascii=False)
        print(f"Emails saved to {output_file}")


if __name__ == "__main__":
    SERVICE_ACCOUNT_FILE_PATH = os.getenv("SERVICE_ACCOUNT_FILE_PATH")
    DELEGATED_USER_EMAIL = os.getenv("DELEGATED_USER_EMAIL")

    connector = GmailConnector(SERVICE_ACCOUNT_FILE_PATH, DELEGATED_USER_EMAIL)
    # Limit to pulling first 3 emails for demo
    emails = connector.fetch_all_emails_with_details(limit=3)
    connector.save_emails_to_json(emails)

    for email in emails:
        print(f"Subject: {email['subject']}")

    print(f"Processed {len(emails)} emails. Check gmail_results.json for results.")

