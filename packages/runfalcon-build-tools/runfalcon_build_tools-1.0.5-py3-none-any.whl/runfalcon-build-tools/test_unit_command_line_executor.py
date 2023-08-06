from sys import stdout
from command_line_executor import CommandLineExecutor

def test_execute_ok_with_args():
    executor:CommandLineExecutor = CommandLineExecutor()
    executor.execute('ls', ['-l'])
    assert executor.return_code == 0

def test_execute_ok_no_args():
    executor:CommandLineExecutor = CommandLineExecutor()
    executor.execute('ls')
    assert executor.return_code == 0

def test_execute_error():
    executor:CommandLineExecutor = CommandLineExecutor()
    executor.execute('lsX', ['-l'])
    assert executor.return_code != 0

def test_execute_script_from_string_ok():
    executor:CommandLineExecutor = CommandLineExecutor()
    script:str = '#!/bin/bash\nset -e\nls -l'
    executor.execute_script(script)
    print(executor.stdout)
    print(executor.stderr)
    assert executor.return_code == 0