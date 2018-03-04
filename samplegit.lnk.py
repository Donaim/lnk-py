import subprocess
import os
import os, sys, subprocess
import sys # for stderr

TARGET_INFO='''
C:\\Users\\d0naim\\Desktop\\Probf\\rec.py
https://github.com/Donaim/ProblemFlawiusza.git
'''

# wyzej miejsce dla adresow. wyszukiwanie jest pryorytetowane z gory do dolu
# second non-emty non-comment line is defined to be the beginning of TARGET_INFO string


        #########
       ## MODES ##
        #########

DEFAULT_MODE = 'auto'

class mode_funcs(object):
    
    
    def auto(at): raise Exception("Not supposed to be here")
    def local(at):
        path = at.command
        path = path.replace('/', os.path.sep).replace('\\', os.path.sep)
        
        isdir = False
        if path[-1] == os.path.sep: isdir = True
        
        if isdir: path += 'lnkpy-run.py'
        
        try:
            subprocess.check_call([path] + sys.argv, shell=True)
            # subprocess.Popen([path] + sys.argv[1:], shell=True, stdin=None, stdout=None, stderr=None, close_fds=False)
        except Exception as ex:
            print("Couldn't open file {}".format(path), file=sys.stderr)
            raise ex

    
    
    def git(at):
        def get_first_local_dir_at():
            for a in at.args_t:
                if a.mode.name == 'local': return a 
    
        repository = at.command
        first_local_at = get_first_local_dir_at()
    
        try:
            subprocess.call(["git", "clone"] + [repository] + [os.path.dirname(first_local_at.command)])
            # subprocess.Popen([path] + sys.argv[1:], shell=True, stdin=None, stdout=None, stderr=None, close_fds=False)
        except Exception as ex:
            print("Couldn't download git repository {}".format(repository), file=sys.stderr)
            raise ex
    
        # after clonning - run
        first_local_at.invoke()
        


class mode_initializators(object):
    
    def _is_pathname_valid(pathname: str) -> bool: # https://stackoverflow.com/a/34102855/7038168
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


########## parsing classes
mode_funcs_static = filter(lambda name: name[0] != '_', dir(mode_funcs))
mode_funcs_di = dict(map(lambda name: (name, getattr(mode_funcs, name)), mode_funcs_static))

mode_inits_static = filter(lambda name: name[0] != '_', dir(mode_initializators))
mode_inits_di = dict(map(lambda name: (name, getattr(mode_initializators, name)), mode_inits_static))

        ###########
       ## PARSING ##
        ###########

split = TARGET_INFO.split('\n')
filtered  = filter(lambda line: len(line) > 0 and not line.isspace() and line[0] != '#', split)

# filtered contains non-empty non-comment lines from TARGET_INFO


class arg_tuple(object):
    def __init__(self, command, mode):
        self.command = command
        self.mode = mode
        self.mode_lookup = mode_lookup
        self.args_t = args_t
    def invoke(self):
        try:
            self.mode.func(self)
            return True
        except Exception as ex:
            print(ex, file=sys.stderr)
            return False
class mode(object):
    def __init__(self, name, func):
        self.name = name
        self.func = func
    def invoke_all(self):
        for a_tuple in args_t:
            if a_tuple.mode == self: 
                if a_tuple.invoke(): return True
        return False
    def init(self, args):
        if self.name in mode_inits_di:
            init_func = mode_inits_di[self.name]
            for a_tuple in args:
                if a_tuple.mode == self:
                    init_func(a_tuple)

mode_lookup = dict(map(lambda p: (p[0], mode(p[0], p[1])), mode_funcs_di.items()))
args_t = []

def parse_args(lines):
    curr = mode_lookup[DEFAULT_MODE]
    for line in lines:
        if line[0] == '$':
            mname = line[1:].strip()
            if mname in mode_lookup:
                curr = mode_lookup[mname]
                continue
            else: raise Exception("unknown mode name: {}".format(mname))
        args_t.append( arg_tuple(line, curr) )
parse_args(filtered)

for (name, m) in mode_lookup.items():
    m.init(args_t)
for t in args_t:
    if t.invoke(): break
