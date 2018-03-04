

TARGET_INFO='''
C:\\Users\\d0naim\\Desktop\\Probf\\primitive.py
https://raw.githubusercontent.com/Donaim/ProblemFlawiusza/master/primitive.py
# https://github.com/Donaim/ProblemFlawiusza.git
'''

# wyzej miejsce dla adresow. wyszukiwanie jest pryorytetowane z gory do dolu
# second non-emty non-comment line is defined to be the beginning of TARGET_INFO string


        #########
       ## MODES ##
        #########

DEFAULT_MODE = 'auto'

class mode_funcs(object):
    #include <mode_funcs.py>
class mode_initializators(object):
    #include <mode_initializators.py>

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
