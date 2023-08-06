import os

def check_type(variable, variableName, dtype, child=None):
    if type(variable) != dtype:
        raise Exception(f"Expect {variableName} type {dtype} but got {type(variable)}")
    if child is not None:
        for elm in variable:
            if type(elm) != child:
                raise Exception(f"{variableName} expect [{child}, {child}, ... {child}] but has {elm}({type(elm)})")

def check_env():
    DSM_EMAIL_APIKEY = os.environ.get('DSM_EMAIL_APIKEY', None)
    EMAIL_SERVICES_URI = os.environ.get('DSM_EMAIL_URI', None)  
    if DSM_EMAIL_APIKEY is None:
        raise Exception("Please set env `DSM_EMAIL_APIKEY`='<APIKEY>'")
    if EMAIL_SERVICES_URI is None:
        raise Exception("Please set env `EMAIL_SERVICES_URI`='<URI>'")