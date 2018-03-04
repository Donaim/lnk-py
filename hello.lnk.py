

TARGET_INFO='''
some local path
$local
README.md
$web

$install

$install_local

$install_web

$web
# - mozna powtarzac sie

'''

# wyzej miejsce dla adresow. wyszukiwanie jest pryorytetowane z gory do dolu
# second non-emty non-comment line is defined to be the beginning of TARGET_INFO string


        #########
       ## MODES ##
        #########

# modes can be added of course
class mode_funcs(object):
    def auto(me, arg): raise Exception("Not supposed to be here")
    def local(me, arg):
        print("Hello from local", arg)
    def web(me, arg):
        print("Hello from web", arg)
    def install(me, arg): raise Exception("Not supposed to be here")
    def install_local(me, arg):
        print("Hello from install_local", arg)
    def install_web(me, arg):
        print("Hello from install_web", arg)
class mode_initializators(object):
    def auto(me, mode_lookup, arg):
        if (arg == 'some local path'):
            if not 'local' in mode_lookup: raise Exception("Auto mode found local path, but no handler for it exists!") 
            me.args.remove(arg)
            mode_lookup['local'].args.append(arg)
        elif(arg == 'some web path'):
            if not 'web' in mode_lookup: raise Exception("Auto mode found web path, but no handler for it exists!") 
            me.args.remove(arg)
            mode_lookup['web'].args.append(arg)
        else: raise Exception("Path \"{}\" is neither local nor web".format(arg))
    
    def install_auto(me, mode_lookup, arg):
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

class mode(object):
    def __init__(self, name, func):
        self.name = name
        self.func = func
        self.args = []
    def invoke(self):
        for a in self.args:
            self.func(self, a)
    def init(self):
        if self.name in mode_inits_di:
            init_func = mode_inits_di[self.name]
            for a in self.args:
                init_func(self, mode_lookup, a)

mode_lookup = dict(map(lambda p: (p[0], mode(p[0], p[1])), mode_funcs_di.items()))
modes = [mode_lookup['auto']]

def parse_args(lines):
    curr = modes[0]
    for line in lines:
        if line[0] == '$':
            mname = line[1:].strip()
            if mname in mode_lookup:
                curr = mode_lookup[mname]
                modes.append(curr)
                continue
            else: raise Exception("unknown mode name: {}".format(mname))
        curr.args.append(line)
parse_args(filtered)

for m in modes:
    m.init()
for m in modes:
    m.invoke()
