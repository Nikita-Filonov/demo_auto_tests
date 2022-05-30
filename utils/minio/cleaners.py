from utils.minio.storage import get_files_in_folder, remove_files_from_storage


def clear_files_storage():
    """Used to clear all files in storage created by autotests"""
    files = get_files_in_folder()
    remove_files_from_storage(files)


if __name__ == '__main__':
    clear_files_storage()
