import os

class FileTools:
    """Safe local file access tools"""
    @staticmethod
    def search_file(filename: str, search_path: str = "/storage/emulated/0/Download") -> list:
        results = []
        if not os.path.exists(search_path):
            return results
            
        for root, _, files in os.walk(search_path):
            for file in files:
                if filename.lower() in file.lower():
                    results.append(os.path.join(root, file))
        return results
