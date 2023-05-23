import os

def check_file_exists(file_path: str) -> bool:
    return os.path.exists(file_path)

def create_file_if_not_exists(file_path: str) -> None:
    if not check_file_exists(file_path):
        with open(file_path, "w") as file:
            pass
