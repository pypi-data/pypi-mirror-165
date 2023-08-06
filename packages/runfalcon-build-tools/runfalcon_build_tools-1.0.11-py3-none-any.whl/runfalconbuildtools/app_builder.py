from runfalconbuildtools.logger import Logger
from runfalconbuildtools.file_utils import delete_directory
from abc import ABC, abstractmethod
from runfalconbuildtools.base_builder import BaseBuilder
from pathlib import Path

class AppBuilder(BaseBuilder, ABC):

    logger:Logger = Logger(Path(__file__).stem)

    def __init__(self, project_name:str, repo_url:str, branch:str):
        self.repo_url = repo_url
        self.branch = branch
        self.project_name = project_name

    def clean_output_directories(self):
        delete_directory(self.get_app_directory())
        delete_directory(self.get_build_file_dir())

    def get_source_artifacts(self):
        self.logger.info('Getting repository {repo}/{branch} to {output_dir} ...'
                                .format(
                                    repo = self.repo_url, 
                                    branch = self.branch, 
                                    output_dir = self.get_app_directory()
                                ))
        
        self.executor.execute('git', [
                                    'clone',
                                    '-b', self.branch,
                                    self.repo_url,
                                    self.get_app_directory()
                                    ]
                            )
        
        if self.executor.return_code != 0:
            self.logger.info('---> {error}'.format(error = self.executor.stderr))
            raise Exception('Can\'t clone repository {url}. {cause}'.format(url = self.repo_url, cause = self.executor.stderr))

    def get_app_name(self) -> str:
        return self.project_name
