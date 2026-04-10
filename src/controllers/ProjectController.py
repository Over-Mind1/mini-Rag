import os 
import hashlib

class ProjectController:
    def __init__(self):
        #go steps back to the root directory and then to the assets/files directory
        self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.files_path = os.path.join(self.base_path, "assets", "files")
    
    def generate_file_name(self, original_filename: str) -> str:
        """use shasum of the original filename to generate a unique filename.
        split the original filename to get the extension and append it to the shasum"""
        name, ext = os.path.splitext(original_filename)
        shasum = hashlib.sha256(name.encode()).hexdigest()
        return f"{shasum}{ext}"

    def get_file_path(self,file_id: str , file_name: str ) -> tuple:
        """Construct the full file path for the given filename."""
        file_path_dir = os.path.join(self.files_path, file_id)
        file_path = os.path.join(file_path_dir, self.generate_file_name(file_name))
        return file_path_dir,file_path
