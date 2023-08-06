from runfalconbuildtools.command_line_executor import CommandLineExecutor

class AWSCommandParams:
    zone:str
    account:int

    def __init__(self, account:int = None, zone:str = None):
        self.account = account
        self.zone = zone

class AWSClient:

    def __init__(self, params:AWSCommandParams):
        self.params = params

    def push_image_to_ecr(self, source_image:str, repository:str):
        target_image:str = source_image.replace(':', '-')
        executor:CommandLineExecutor = CommandLineExecutor()
        command:str = ''
        command += '#!/bin/bash\n'
        command += 'set -e\n'
        command += 'aws ecr get-login-password --region {zone} | docker login --username AWS --password-stdin {account}.dkr.ecr.{zone}.amazonaws.com\n' \
                        .format(zone = self.params.zone, account = self.params.account)
        command += 'docker tag {source_image} {account}.dkr.ecr.{zone}.amazonaws.com/{repository}:{target_image}\n' \
                        .format(source_image = source_image, account = self.params.account, zone = self.params.zone, repository = repository, target_image = target_image)
        command += 'docker push {account}.dkr.ecr.{zone}.amazonaws.com/{repository}:{target_image}\n' \
                        .format(account = self.params.account, zone = self.params.zone, repository = repository, target_image = target_image)

        executor.execute_script(command)
        if executor.return_code != 0:
            raise Exception('\nCode: {code}.\noutput: {out}\nerror: {error}' \
                .format(code = executor.return_code, out = executor.stdout, error = executor.stderr))