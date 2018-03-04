import os, tempfile, re

DEFAULT_MODE = 'auto'

class mode_funcs(object):
    def auto(at): raise Exception("Not supposed to be here")
    def local(at):
        if at.command == "README.md": raise Exception("Dont like readmes!!!")
        print("Hello from local", at.command)
    def web(at):
        if at.command[-1] == 'N': raise Exception(":(")
        print("Hello from web", at.command)
    def install(at): raise Exception("Not supposed to be here")
    def install_local(at):
        print("Hello from install_local", at.command)
    def install_web(at):
        print("Hello from install_web", at.command)
class mode_initializators(object):
    valid_url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def auto(at, mode_lookup):
        def is_pathname_valid(pathname: str) -> bool: # https://stackoverflow.com/a/34102855/7038168
            try:
                if len(pathname) < 1: return False
                _, pathname = os.path.splitdrive(pathname)
                root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
                    if sys.platform == 'win32' else os.path.sep
                assert os.path.isdir(root_dirname)   # ...Murphy and her ironclad Law
                root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep
                for pathname_part in pathname.split(os.path.sep):
                    try: os.lstat(root_dirname + pathname_part)
                    except OSError as exc:
                        if hasattr(exc, 'winerror'):
                            if exc.winerror == 123: # ERROR_INVALID_NAME = 123
                                return False
                        elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                            return False
            except TypeError as exc: return False
            else: return True
        if (is_pathname_valid(at.command)):
            if not 'local' in mode_lookup: raise Exception("Auto mode found local path, but no handler for it exists!") 
            at.mode = mode_lookup['local']
        elif(at.command == 'some web path'):
            if not 'web' in mode_lookup: raise Exception("Auto mode found web path, but no handler for it exists!") 
            at.mode = mode_lookup['web']
        else: raise Exception("Path \"{}\" is neither local nor web".format(at.command))
    
    def install_auto(at, mode_lookup):
        raise NotImplementedError()
        pass