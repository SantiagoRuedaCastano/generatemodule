import os
import shutil

class DirectoryHelper:

    def create(self, path:str):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

    def delete(self, path):
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)