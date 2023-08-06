import array
from runfalconbuildtools.logger import Logger
from runfalconbuildtools.docker_base import DockerBase
from pathlib import Path
from runfalconbuildtools.docker_options import DockerOptions, OptionName

class DockerTagger(DockerBase):

    logger:Logger = Logger(Path(__file__).stem)

    def __init__(self, options:DockerOptions):
        super().__init__(options)

    def get_build_script(self):
        script:str = '#!/bin/bash\n'
        script += 'source_image="{source}"\n'.format(file = self.get_option(OptionName.source_image))
        script += 'target_image="{target}"\n'.format(image_tag = self.get_option(OptionName.target_image))
        script += 'docker tag ${source_image} ${target_image} \n'
        return script

    def get_script_file_name(self) -> str:
        return 'docker_image_tag_script.sh'

    def get_source_artifacts(self):
        self.get_option(OptionName.docker_file_path)

    def get_loger(self):
        return self.logger

    def get_required_options(self) -> array:
        return [
            OptionName.source_image.value,
            OptionName.target_image.value
        ]
