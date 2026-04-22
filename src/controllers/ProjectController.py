import os 
import hashlib
import uuid


class ProjectController:
    def __init__(self):
        #go steps back to the root directory and then to the assets/files directory
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.files_path = os.path.join(self.base_path, "assets", "files")
    
    def generate_file_name(self, original_filename: str) -> tuple:
        name, ext = os.path.splitext(original_filename)
        unique_id = uuid.uuid4().hex
        shasum = hashlib.sha256(f"{name}{unique_id}".encode()).hexdigest()
        return f"{shasum}{ext}", ext

    def get_file_path(self,file_id: str , file_name: str ) -> tuple:
        """Construct the full file path for the given filename."""
        file_path_dir = os.path.join(self.files_path, file_id)
        file_name, file_ext = self.generate_file_name(file_name)
        file_path = os.path.join(file_path_dir, file_name)
        return file_path_dir,file_path, file_name, file_ext
    