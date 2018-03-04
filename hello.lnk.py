

TARGET_INFO='''

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

class mode_funcs(object):
    def auto(me, arg):
        print("Hello from auto")
    def local(me, arg):
        print("Hello from local")
    def web(me, arg):
        print("Hello from web")
    def install(me, arg):
        print("Hello from install")
    def install_local(me, arg):
        print("Hello from install_local")
    def install_web(me, arg):
        print("Hello from install_web")

mode_funcs_static = filter(lambda name: name[0] != '_', dir(mode_funcs))
mode_funcs_di = dict(map(lambda name: (name, getattr(mode_funcs, name)), mode_funcs_static))
mode_names = list(mode_funcs_di.keys())

class mode_parsers(object):
    pass

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

# modes can be added of course

mode_lookup = dict(map(lambda p: (p[0], mode(p[0], p[1])), mode_funcs_di.items()))
# modes = mode_lookup.values()
modes = [mode_lookup['auto']]

def parse_args(lines):
    curr = modes[0]
    for line in lines:
        if line[0] == '$':
            mname = line[1:].strip()
            if mname in mode_names:
                curr = mode_lookup[mname]
                modes.append(curr)
                continue
            else: raise Exception("unknown mode name: {}".format(mname))
        curr.args.append(line)

parse_args(filtered)
print(dict(map(lambda m: (m.name, m.args), modes))) # ok
for m in modes:
    m.invoke()
