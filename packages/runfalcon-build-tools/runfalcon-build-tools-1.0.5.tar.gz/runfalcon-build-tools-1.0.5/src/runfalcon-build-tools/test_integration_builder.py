from nodejs_typescript_builder import NodeJSTypeScriptBuilder

def test_build_NodeJS():
    project_name:str = 'runfalcon-load-agent-web-api'
    builder:NodeJSTypeScriptBuilder = NodeJSTypeScriptBuilder(
                            project_name,
                            'ssh://git-codecommit.us-east-1.amazonaws.com/v1/repos/' + project_name,
                            'master'
                        )
    builder.build()
