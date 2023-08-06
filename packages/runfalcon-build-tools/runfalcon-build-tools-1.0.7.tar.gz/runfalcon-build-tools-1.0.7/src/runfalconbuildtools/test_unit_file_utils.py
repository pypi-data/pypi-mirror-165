from distutils import file_util
from file_utils import file_exists, get_current_path

def test_file_exist_true_directory():
    assert file_exists('.')

def test_file_exist_true_file():
    assert file_exists(get_current_path() + '/__init__.py')

def test_file_exist_false():
    assert not file_exists('./not-existing-directory-name')
