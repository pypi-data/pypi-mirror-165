from abc import ABC, abstractmethod
from array import array
from base_builder import BaseBuilder
from docker_options import DockerOptions
from file_utils import delete_directory
from docker_options import OptionName

class DockerBase(BaseBuilder, ABC):

    base_required_options = [
        OptionName.project_name.value
    ]

    def __init__(self, options:DockerOptions):
        self.options = options

    def _validate_required_options(self):
        is_subset = set(list(self.base_required_options)).issubset(set(self.options.keys()))
        if not is_subset:
            raise Exception('Requiered docker base options not setted: {op}'.format(op = set(self.base_required_options) - set(self.options.keys())))

        is_subset = set(list(self.get_required_options())).issubset(set(self.options.keys()))
        if not is_subset:
            raise Exception('Requiered options not setted: {op}'.format(op = set(self.get_required_options()) - set(self.options.keys())))
    
    def validate(self) -> str:
        self._validate_required_options()

    def clean_output_directories(self):
        delete_directory(self.get_app_directory())
        delete_directory(self.get_build_file_dir())

    def get_option(self, option:str) -> str:
        return self.options.get(option.value)

    def get_app_name(self):
        return self.get_option(OptionName.project_name)

    @abstractmethod
    def get_required_options(self) -> array:
        pass
