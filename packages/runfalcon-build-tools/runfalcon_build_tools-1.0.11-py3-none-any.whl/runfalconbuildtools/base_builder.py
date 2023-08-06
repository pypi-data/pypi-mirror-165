from abc import ABC, abstractmethod
from runfalconbuildtools.env_utils import get_env_variable
from runfalconbuildtools.file_utils import create_file, add_execution_permission_to_file, create_dir_if_not_exists
from runfalconbuildtools.command_line_executor import CommandLineExecutor

class BaseBuilder(ABC):

    executor:CommandLineExecutor = CommandLineExecutor()
    working_dir:str = get_env_variable('WORKING_DIR', './working_dir')

    def get_app_directory(self):
        return self.working_dir + '/' + self.get_app_name()

    def get_build_file_dir(self) -> str:
        return self.working_dir + '/scripts'

    def get_build_file_full_name(self) -> str:
        return self.get_build_file_dir() + '/' + self.get_script_file_name()

    def create_build_script(self):
        build_script:str = self.get_build_script()
        script_file:str = self.get_build_file_full_name()
        create_dir_if_not_exists(self.get_build_file_dir())
        create_file(script_file, build_script)
        add_execution_permission_to_file(script_file)

    def _run_build(self):
        self.create_build_script()
        self.executor.execute(self.get_build_file_full_name())
        if self.executor.return_code != 0:
            raise Exception('Error running build script.\nERROR\n{error}\nOUTPUT\n{output}'.format(
                error = self.executor.stderr,
                output = self.executor.stdout
            ))

    def build(self):
        self.validate()
        self.get_loger().info("Build started ...")
        self.clean_output_directories()
        self.get_source_artifacts()
        self._run_build()
        self.get_loger().info("Build ended.")

    @abstractmethod
    def get_app_name(self) -> str:
        pass

    @abstractmethod
    def validate(self) -> str:
        pass

    @abstractmethod
    def get_script_file_name(self) -> str:
        pass

    @abstractmethod
    def get_build_script(self) -> str:
        pass
  
    @abstractmethod
    def clean_output_directories(self):
        pass

    @abstractmethod
    def get_source_artifacts(self):
        pass

    @abstractmethod
    def get_loger(self):
        pass
