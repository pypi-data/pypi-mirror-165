from docker_image_builder import DockerImageBuilder
from docker_options import DockerOptions

def test_build_image_requiered_para_not_set():
    options:DockerOptions = {
        'docker_file_path': '/path'
    }
    docker_manager:DockerImageBuilder = DockerImageBuilder(options)
    error = None
    try:
        docker_manager.build()
    except Exception as e:
        error = e
        print(' >>>>> Error:\n{e}'.format(e = error))

    assert error != None

def test_build_image_ok():
    options:DockerOptions = {
        'project_name': 'test project name',
        'docker_file_path': './scripts/test/resources/simple_docker_file.dockerfile',
        'image_tag': 'the_tag',
        'image_params': {
            'arg1': 'value 1',
            'arg2': 'value 2'
        }
    }
    docker_manager:DockerImageBuilder = DockerImageBuilder(options)
    error = None
    try:
        docker_manager.build()
    except Exception as e:
        error = e
        print(' >>>>> Error:\n{e}'.format(e = error))

    assert error == None
