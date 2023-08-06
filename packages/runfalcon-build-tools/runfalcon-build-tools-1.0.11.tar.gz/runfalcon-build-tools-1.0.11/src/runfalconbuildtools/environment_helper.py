from array import array
import os

class EnvironmetHelper:

    def validate_vars(self, vars:array):
        if len(vars) > 0:

            missing_vars:array = []
            for var in vars:
                if os.getenv(var) == None:
                    missing_vars.append(var)

            if len(missing_vars) > 0:
                raise Exception('Missing environment variables: {vars}'.format(vars = missing_vars))