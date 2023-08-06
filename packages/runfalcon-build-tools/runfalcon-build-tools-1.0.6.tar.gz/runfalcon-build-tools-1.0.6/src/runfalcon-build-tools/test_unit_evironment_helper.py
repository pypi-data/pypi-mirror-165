
from os import environ
from environment_helper import EnvironmetHelper

def test_missing_vars_all_not_found():
    er = None
    environment_helper:EnvironmetHelper = EnvironmetHelper()
    try:
        environment_helper.validate_vars(['NOT_EXISTING_VAR_1', 'NOT_EXISTING_VAR_2'])
    except Exception as e:
        er = e
        print(er)
    assert er != None

def test_missing_vars_some_not_found():
    er = None
    environment_helper:EnvironmetHelper = EnvironmetHelper()
    try:
        environment_helper.validate_vars(['HOME', 'NOT_EXISTING_VAR_1'])
    except Exception as e:
        er = e
        print(er)
    assert er != None

def test_missing_vars_found():
    er = None
    environment_helper:EnvironmetHelper = EnvironmetHelper()
    try:
        environment_helper.validate_vars(['HOME', 'PATH'])
    except Exception as e:
        er = e
        print(er)
    assert er == None
