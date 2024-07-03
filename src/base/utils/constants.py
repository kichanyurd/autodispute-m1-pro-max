HOST = "host.docker.internal"
DOWNLOADS_BASE_FOLDER = "downloaded_pages"
DB_NAME = "crawls"
COLLECTION_NAME = "crawling_requests"

# keys
STATUS_KEY = "status"
URL_KEY = "url"
NOTIFICATION_TARGETS_KEY = "notification_targets"
CRAWL_ID_KEY = "crawl_id"

#statuses
RUNNING_STATUS = "RUNNING"
COMPLETE_STATUS = "COMPLETE"
ACCEPTED_STATUS = "ACCEPTED"
ERROR_STATUS = "ERROR"


#queues
ORCHESTRATOR_QUEUE = "orchestrator"
LLM_WORKER_1_QUEUE = "llm-1"
LLM_WORKER_2_QUEUE = "llm-2"
LLM_WORKER_3_QUEUE = "llm-3"
OUTPUT_QUEUE = "output"
TEXT_TO_SPEECH_QUEUE = "text-to-speech"
