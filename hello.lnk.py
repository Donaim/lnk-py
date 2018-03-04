

TARGET_INFO='''
some web path

$local
# README.md

$web
https://github.coN

$install

$install_local

$install_web

$web
# mozna powtarzac sie
https://google.com

'''

# wyzej miejsce dla adresow. wyszukiwanie jest pryorytetowane z gory do dolu
# second non-emty non-comment line is defined to be the beginning of TARGET_INFO string


        #########
       ## MODES ##
        #########

# modes can be added of course
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
        if (at.command == 'some local path'):
            if not 'local' in mode_lookup: raise Exception("Auto mode found local path, but no handler for it exists!") 
            at.mode = mode_lookup['local']
        elif(at.command == 'some web path'):
            if not 'web' in mode_lookup: raise Exception("Auto mode found web path, but no handler for it exists!") 
            at.mode = mode_lookup['web']
        else: raise Exception("Path \"{}\" is neither local nor web".format(at.command))
    
    def install_auto(at, mode_lookup):
        raise NotImplementedError()
        pass

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

import sys # for stderr

class arg_tuple(object):
    def __init__(self, command, mode):
        self.command = command
        self.mode = mode
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
    def invoke_all(self, args):
        for a_tuple in args:
            if a_tuple.mode == self: 
                if a_tuple.invoke(): return True
        return False
    def init(self, args):
        if self.name in mode_inits_di:
            init_func = mode_inits_di[self.name]
            for a_tuple in args:
                if a_tuple.mode == self:
                    init_func(a_tuple, mode_lookup)

mode_lookup = dict(map(lambda p: (p[0], mode(p[0], p[1])), mode_funcs_di.items()))
args_t = []

def parse_args(lines):
    curr = mode_lookup['auto']
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
