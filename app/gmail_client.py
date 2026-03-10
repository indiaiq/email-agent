from googleapiclient.discovery import build
from app.gmail_auth import get_gmail_credentials


def get_gmail_service():
    """
    Create and return an authenticated Gmail API service object.
    """
    creds = get_gmail_credentials()
    service = build("gmail", "v1", credentials=creds)
    return service


def search_messages(service, query: str, max_results: int = 100):
    """
    Search Gmail messages using a Gmail search query.
    Returns a list of message dicts with message IDs.
    """
    results = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=max_results
    ).execute()

    return results.get("messages", [])


def get_message_metadata(service, message_id: str):
    """
    Get only basic metadata for a message.
    """
    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format="metadata",
        metadataHeaders=["From", "Subject", "Date"]
    ).execute()

    return message


def archive_message(service, message_id: str):
    """
    Archive a message by removing the INBOX label and remove the UNREAD label.
    This does NOT delete the email.
    """
    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={
            "removeLabelIds": ["INBOX", "UNREAD"]
        }
    ).execute()