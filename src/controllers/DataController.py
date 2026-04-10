from src.utils.config import Settings
from fastapi import UploadFile
from src.schemas.enums.ResponseEnums import ResponseStatus
import os

class DataController:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.allowed_extensions = settings.file_allowed_extensions
        self.max_file_size_mb = settings.file_max_size_mb
        self.size_scale = 1024 * 1024

    def validate_file_extension(self, filename: str) -> bool:
        """Check if the file extension is allowed."""
        ext = os.path.splitext(filename)[1].lower()
        return ext in self.allowed_extensions

    async def validate_file_size(self, file: UploadFile) -> bool:
        """Check if the file size is within the allowed limit."""
        contents = await file.read()
        file_size = len(contents)

        await file.seek(0)

        max_size_bytes = self.max_file_size_mb * self.size_scale
        return file_size <= max_size_bytes

    async def validate_file(self, file: UploadFile) -> tuple[bool, str]:
        """
        Validate the uploaded file for both extension and size.
        param file: The uploaded file to validate.
        Returns a tuple of (is_valid, message) where is_valid is a boolean and message is a string.
        """
        if not file.filename:   
            return False, ResponseStatus.NO_FILENAME_PROVIDED
        
        if not self.validate_file_extension(file.filename):
            return False, ResponseStatus.NOT_ALLOWED_FILE_EXTENSION

        if not await self.validate_file_size(file):
            return False, ResponseStatus.FILE_SIZE_EXCEEDS_LIMIT

        return True, ResponseStatus.SUCCESS