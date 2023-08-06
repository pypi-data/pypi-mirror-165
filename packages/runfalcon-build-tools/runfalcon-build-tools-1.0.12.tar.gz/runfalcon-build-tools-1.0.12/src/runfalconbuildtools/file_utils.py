import os
import stat
import shutil

def file_exists(file_path:str) -> bool:
    return os.path.exists(file_path)

def get_current_path():
    return os.path.dirname(os.path.abspath(__file__))

def delete_directory(dir_path:str):
    if file_exists(dir_path):
        shutil.rmtree(dir_path)

def create_file(file_path:str, content:str):
    f = open(file_path, 'w')
    f.write(content)
    f.close()

def add_execution_permission_to_file(file_path:str):
    st = os.stat(file_path)
    os.chmod(file_path, st.st_mode | stat.S_IEXEC)

def create_dir_if_not_exists(dir_path:str):
    if not file_exists(dir_path):
        os.makedirs(dir_path)

def delete_file(file:str):
    if os.path.exists(file):
        os.remove(file)
