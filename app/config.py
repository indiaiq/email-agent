# Gmail search query for initial inbox cleanup
# This finds unread emails older than 90 days
# and excludes anything already labeled ai, fiber, or farm.
CLEANUP_QUERY = 'is:unread older_than:90d -label:AI -label:Fiber -label:Farm'

# Safety settings
DRY_RUN = False
BATCH_LIMIT = 50

# Important senders you do NOT want archived automatically
SENDER_WHITELIST = [
    "deeplearning.ai",
    "anthropic.com",
    "tldrnewsletter.com",
]