import array
from runfalconbuildtools.logger import Logger
from runfalconbuildtools.docker_base import DockerBase
from pathlib import Path
from runfalconbuildtools.docker_options import DockerOptions, OptionName

class DockerImageBuilder(DockerBase):

    logger:Logger = Logger(Path(__file__).stem)

    def __init__(self, options:DockerOptions):
        super().__init__(options)

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

    def get_script_file_name(self) -> str:
        return 'docker_image_build_script.sh'

    def get_source_artifacts(self):
        self.get_option(OptionName.docker_file_path)

    def get_loger(self):
        return self.logger

    def get_required_options(self) -> array:
        return [
            OptionName.project_name.value,
            OptionName.docker_file_path.value,
            OptionName.image_tag.value
        ]
