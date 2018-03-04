

TARGET_INFO='''
ahdahdjah sd
$local
README.md
$web

$install

$install_local

$install_web

$web
# - można powtarzać się

'''

# wyżej miejsce dla adresów. wyszukiwanie jest pryorytetowane z góry do dołu
# first non-emty non-comment line is defined to be the beginning of TARGET_INFO string


        #########
       ## MODES ##
        #########

# modes can be added of course
class mode_funcs(object):
    def auto(me, arg):
        print("Hello from auto", arg)
    def local(me, arg):
        print("Hello from local", arg)
    def web(me, arg):
        print("Hello from web", arg)
    def install(me, arg):
        print("Hello from install", arg)
    def install_local(me, arg):
        print("Hello from install_local", arg)
    def install_web(me, arg):
        print("Hello from install_web", arg)
class mode_initializators(object):
    def auto(me, modes, arg):
        print("HELLO FORM INIT AUTO!")
        if (arg == 'some local path'):
            me.args.remove(arg)
            modes['local'].args.append(arg)
        elif(arg == 'some web path'):
            me.args.remove(arg)
            modes['web'].args.append(arg)
        else: raise Exception("Path \"{}\" is neither local nor web".format(arg))
    
    def install_auto(me, modes, arg):
        raise NotImplementedError()
        pass

mode_funcs_static = filter(lambda name: name[0] != '_', dir(mode_funcs))
mode_funcs_di = dict(map(lambda name: (name, getattr(mode_funcs, name)), mode_funcs_static))
mode_names = list(mode_funcs_di.keys())

mode_inits_static = filter(lambda name: name[0] != '_', dir(mode_initializators))
mode_inits_di = dict(map(lambda name: (name, getattr(mode_initializators, name)), mode_inits_static))
mode_inits_names = list(mode_inits_di.keys())

        ###########
       ## PARSING ##
        ###########

split = TARGET_INFO.split('\n')

def filter_target(line): return len(line) > 0 and line[0] != '#'
filtered  = filter(filter_target, split)

# filtered contains non-empty non-comment lines from TARGET_INFO

class mode(object):
    def __init__(self, name, func):
        self.name = name
        self.func = func
        self.args = []
    def invoke(self):
        for a in self.args:
            self.func(self, a)
    def init(self, init_func, modes):
        for a in self.args:
            init_func(self, modes, a)
   

mode_lookup = dict(map(lambda p: (p[0], mode(p[0], p[1])), mode_funcs_di.items()))
# modes = mode_lookup.values()
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
# print(list(map(lambda m: (m.name, m.args), modes))) # ok
for m in modes:
    if m.name in mode_inits_di:
        print(m.name)
        m.init(mode_inits_di[m.name], modes)
for m in modes:
    m.invoke()
