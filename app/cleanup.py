import time

from app.gmail_client import (
    get_gmail_service,
    search_messages,
    get_message_metadata,
    archive_thread,
    count_messages,
)
from app.config import CLEANUP_QUERY, DRY_RUN, BATCH_LIMIT, SENDER_WHITELIST


def extract_header(headers, header_name: str) -> str:
    """
    Pull a specific header value from Gmail message headers.
    """
    for header in headers:
        if header.get("name", "").lower() == header_name.lower():
            return header.get("value", "")
    return ""


def sender_is_whitelisted(sender_value: str, whitelist: list[str]) -> bool:
    """
    Check whether the sender matches any protected sender/domain.
    """
    sender_lower = sender_value.lower()
    return any(item.lower() in sender_lower for item in whitelist)


def run_cleanup():
    """
    Find old unread emails, skip protected ones, and archive safely.
    """

    service = get_gmail_service()

    # remaining = count_messages(service, CLEANUP_QUERY)
    # print(f"\nRemaining emails matching query before batch: {remaining}\n")

    print("\n=== CLEANUP START ===")
    print(f"Query: {CLEANUP_QUERY}")
    print(f"Dry run: {DRY_RUN}")
    print(f"Batch limit: {BATCH_LIMIT}\n")

    messages = search_messages(service, CLEANUP_QUERY, max_results=BATCH_LIMIT)

    # process messages here (archive logic)

    # remaining_after = count_messages(service, CLEANUP_QUERY)
    # print(f"\nRemaining emails matching query after batch: {remaining_after}")

    if not messages:
        print("No matching messages found.")
        return

    print(f"Found {len(messages)} matching messages.\n")

    archived_count = 0
    skipped_whitelist_count = 0

    for index, msg in enumerate(messages, start=1):
        message_id = msg["id"]
        metadata = get_message_metadata(service, message_id)
        headers = metadata.get("payload", {}).get("headers", [])

        sender = extract_header(headers, "From")
        subject = extract_header(headers, "Subject")
        date = extract_header(headers, "Date")

        print("=" * 80)
        print(f"Message {index}")
        print(f"ID: {message_id}")
        print(f"From: {sender}")
        print(f"Subject: {subject}")
        print(f"Date: {date}")

        if sender_is_whitelisted(sender, SENDER_WHITELIST):
            print("Action: SKIPPED (whitelisted sender)")
            skipped_whitelist_count += 1
            continue

        if DRY_RUN:
            print("Action: WOULD ARCHIVE (dry-run)")
        else:
            thread_id = msg["threadId"]
            archive_thread(service, thread_id)
            print("Action: ARCHIVED")
            archived_count += 1
            time.sleep(0.3)

    print("\n=== CLEANUP SUMMARY ===")
    print(f"Matched messages: {len(messages)}")
    print(f"Skipped by whitelist: {skipped_whitelist_count}")
    print(f"Archived: {archived_count}")

    if DRY_RUN:
        print("Dry-run mode is ON, so no emails were changed.")