import os

class FileManager:
    def __init__(self) -> None:
        self.directory = f"{os.getcwd()}/data"
        self.files = self.get_sorted_files()
        self.latest_file = self.get_latest_file()

    def get_sorted_files(self):
        files = [(file, os.path.getctime(os.path.join(self.directory, file))) for file in os.listdir(self.directory)]
        sorted_files = sorted(files, key=lambda x: x[1], reverse=True)
        return sorted_files
    
    def get_latest_file(self):
        return self.get_sorted_files()[0][0]
