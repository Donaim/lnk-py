
#moveat imports 1
import os

#moveat global 1
osname = os.name

def _is_pathname_valid(pathname: str) -> bool: # https://stackoverflow.com/a/34102855/7038168
    try:
        full = os.path.expanduser(pathname)
        if osname == 'posix':
            return full[0] == os.path.sep # the only condition
        elif osname == 'nt': # thats windows
            return full[1] == ':' and full[2] == os.path.sep
    except:
        return False
