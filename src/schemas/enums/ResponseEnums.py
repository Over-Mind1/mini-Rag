from enum import Enum

class ResponseStatus(str, Enum):
    SUCCESS = "success"
    Failed = "failed"
    ERROR = "error"
    FILE_UPLOADED_FAILED = "file_upload_failed"
    FILE_UPLOADED_SUCCESSFULLY = "file_upload_success"
    FILE_ALREADY_EXISTS = "file_already_exists"
    NO_FILENAME_PROVIDED = "no_filename_provided"
    NOT_ALLOWED_FILE_EXTENSION = "not_allowed_file_extension"
    FILE_SIZE_EXCEEDS_LIMIT = "file_size_exceeds_limit"