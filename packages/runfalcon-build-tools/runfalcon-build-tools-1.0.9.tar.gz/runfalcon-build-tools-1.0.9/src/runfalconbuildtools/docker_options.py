from enum import Enum
from typing import Dict

class DockerOptions:
    project_name:str
    docker_file_path:str
    image_tag:str
    image_params:Dict
    source_image:str
    target_image:str

class OptionName(Enum):
    project_name:str = 'project_name'
    docker_file_path:str = 'docker_file_path'
    image_tag:str = 'image_tag'
    image_params:str = 'image_params'
    source_image:str = 'source_image'
    target_image:str = 'target_image'
