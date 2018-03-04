DEFAULT_MODE = 'auto'

#include <url_regex.py>
#include <is_pathname_valid.py>

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
    def auto(at, mode_lookup):
        if (is_pathname_valid(at.command)):
            if not 'local' in mode_lookup: raise Exception("Auto mode found local path, but no handler for it exists!") 
            at.mode = mode_lookup['local']
        elif(is_valid_url(at.command)):
            if not 'web' in mode_lookup: raise Exception("Auto mode found web path, but no handler for it exists!") 
            at.mode = mode_lookup['web']
        else: raise Exception("Path \"{}\" is neither local nor web".format(at.command))
    
    def install_auto(at, mode_lookup):
        raise NotImplementedError()
        pass