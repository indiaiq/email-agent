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


def archive_thread(service, thread_id: str):
    """
    Archive an entire Gmail thread and mark all messages read.
    """
    service.users().threads().modify(
        userId="me",
        id=thread_id,
        body={
            "removeLabelIds": ["INBOX", "UNREAD"]
        }
    ).execute()

    def count_messages(service, query: str) -> int:
    """
    Count all messages matching a Gmail query by paging through results.
    """
    total = 0
    next_page_token = None

    while True:
        results = service.users().messages().list(
            userId="me",
            q=query,
            maxResults=500,
            pageToken=next_page_token
        ).execute()

        messages = results.get("messages", [])
        total += len(messages)

        next_page_token = results.get("nextPageToken")
        if not next_page_token:
            break

    return total