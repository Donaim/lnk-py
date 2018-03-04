
#include <is_pathname_valid.py>

def auto(at):
    def is_valid_git(string):
        return (string.startswith("https://") or string.startswith("http://")) and string.endswith(".git")
    if (mode_initializators._is_pathname_valid(at.command)):
        if not 'local' in mode_lookup: raise Exception("Auto mode found local path, but no handler for it exists!") 
        at.mode = at.mode_lookup['local']
    elif(is_valid_git(at.command)):
        if not 'git' in mode_lookup: raise Exception("Auto mode found web path, but no handler for it exists!") 
        at.mode = at.mode_lookup['git']
    else: raise Exception("Path \"{}\" is neither local nor git".format(at.command))