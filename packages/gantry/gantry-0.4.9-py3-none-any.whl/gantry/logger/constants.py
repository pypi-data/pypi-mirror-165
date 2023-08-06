from enum import Enum


class BatchType(str, Enum):
    RECORD = "RECORD"
    FEEDBACK = "FEEDBACK"
    PREDICTION = "PREDICTION"


class UploadFileType(str, Enum):
    CSV_WITH_HEADERS = "CSV_WITH_HEADERS"
    EVENTS_BYTES = "EVENTS_BYTES"


class Delimiter(Enum):
    COMMA = ","


CHUNK_SIZE = 10 * 1024 * 1024  # File upload chunk size 10 MB
