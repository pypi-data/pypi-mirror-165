from runfalconbuildtools.logger import Logger
from runfalconbuildtools.base_builder import BaseBuilder
from runfalconbuildtools.file_utils import delete_directory
from pathlib import Path
from runfalconbuildtools.docker_options import DockerOptions, OptionName

class DockerImageTagger(BaseBuilder):

    logger:Logger = Logger(Path(__file__).stem)

    required_options = [
        'project_name',
        'docker_file_path',
        'image_tag'
    ]

    options = DockerOptions()

    def __init__(self, options:DockerOptions):
        self.options = options

    def validate_required_options(self):
        is_subset = set(list(self.required_options)).issubset(set(self.options.keys()))
        if not is_subset:
            raise Exception('Requiered options not setted: {op}'.format(op = set(self.required_options) - set(self.options.keys())))
    
    def get_build_script(self):
        script:str = '#!/bin/bash\n'
        script += 'docker_file="{file}"\n'.format(file = self.get_option(OptionName.docker_file_path))
        script += 'image_tag="{image_tag}"\n'.format(image_tag = self.get_option(OptionName.image_tag))
        script += 'docker build -f ${docker_file} \\\n'
        script += '   -t ${image_tag} \\\n'

        if self.get_option(OptionName.image_params) != None:
            image_params_obj = self.get_option(OptionName.image_params)
            for key in image_params_obj:
                script += '   --build-arg {arg_name}="{arg_value}" \\\n'.format(arg_name = key, arg_value = image_params_obj.get(key))

        script += '   .\n'

        return script

    def get_app_name(self):
        return self.get_option(OptionName.project_name)

    def get_option(self, option:str) -> str:
        return self.options.get(option.value)

    def validate(self) -> str:
        self.validate_required_options()

    def get_script_file_name(self) -> str:
        return 'docker_image_build_script.sh'

    def clean_output_directories(self):
        delete_directory(self.get_app_directory())
        delete_directory(self.get_build_file_dir())

    def get_source_artifacts(self):
        self.get_option(OptionName.docker_file_path)

    def get_loger(self):
        return self.logger