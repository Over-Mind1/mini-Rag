from fastapi import APIRouter, Depends, File, UploadFile,status
from fastapi.responses import JSONResponse
from src.utils.config import get_settings,Settings
from src.controllers import DataController,ProjectController
from src.schemas.enums.ResponseEnums import ResponseStatus
import aiofiles
import os
import logging

logger = logging.getLogger("uvicorn.error") #get the uvicorn logger to log errors in the same format as uvicorn logs
router = APIRouter(
    prefix="/api/v1/data",
    tags=["data"]
)

@router.post("/upload/{file_id}", summary="Upload a file")
async def upload_file(file_id: str, file: UploadFile = File(...), 
                      settings: Settings = Depends(get_settings)):
    # Validate the uploaded file 
    is_valid,message = await DataController(settings).validate_file(file)
    
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={"status": ResponseStatus.Failed, "message": message}
                            ) 
    # Process the file (e.g., save to disk, database, etc.)
    file_path_dir,file_path=ProjectController().get_file_path(
        file_id=file_id,
        file_name=file.filename or "unknown"
        )
    #create the directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    #check if file already exists
    if os.path.exists(file_path):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, 
            content={"status": ResponseStatus.Failed, 
                     "message": ResponseStatus.FILE_ALREADY_EXISTS}
                            )
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            chunk_size = settings.file_default_chunk_size * 1024 # Convert kB to bytes
            while content := await file.read(chunk_size):
                await out_file.write(content)

    except Exception as e:
        logger.error(f"Error occurred while uploading file: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content={"status": ResponseStatus.ERROR, 
                     "message": f"{ResponseStatus.FILE_UPLOADED_FAILED} - {str(e)}"}
                            )

    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={"status": ResponseStatus.SUCCESS, 
                 "message": ResponseStatus.FILE_UPLOADED_SUCCESSFULLY,
                 "file_id": file_id,
                 "filename": file.filename,
                 "file_dir_path": file_path_dir,
                 "file_path": file_path}
                        )        