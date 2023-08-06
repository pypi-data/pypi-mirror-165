from runfalconbuildtools.app_builder import AppBuilder
from runfalconbuildtools.logger import Logger
from pathlib import Path

class NodeJSTypeScriptBuilder(AppBuilder):

    logger:Logger = Logger(Path(__file__).stem)

    def get_build_script(self) -> str:
        script:str = '#!/bin/bash\n'
        script += 'curr_dir=`pwd`\n'
        script += 'app_dir="{app_src_dir}"\n'.format(app_src_dir = self.get_app_directory())
        script += 'cd "${app_dir}"\n'
        script += 'echo "Building \\"${app_dir}\\"..."\n'
        script += 'npm install\n'
        script += 'npm run build\n'
        script += 'rm -rf dist/__test__\n'
        script += 'cd "${curr_dir}"\n'
        return script

    def get_script_file_name(self) -> str:
        return 'app_build_script.sh'

    def validate(self) -> str:
        pass

    def get_loger(self):
        return self.logger
