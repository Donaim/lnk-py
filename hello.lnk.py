

TARGET_INFO='''

$local
README.md
$web

$install

$install-local

$install-web

$web
# - można powtarzać się

'''


# wyżej miejsce dla adresów. wyszukiwanie jest pryorytetowane z góry do dołu
# first non-emty non-comment line is defined to be the beginning of TARGET_INFO string

split = TARGET_INFO.split('\n')

def filter_target(line): return len(line) > 0 and line[0] != '#'
filtered  = filter(filter_target, split)

# filtered contains non-empty non-comment lines from TARGET_INFO

class mode(object):
    def __init__(self, name):
        self.name = name
        self.func = mode_funcs_di[name]
        self.args = []
    def invoke(self): self.func(self)

    def p_auto(me):
        print("in auto!!")
    def p_local(me):
        pass
    def p_web(me):
        pass
    def p_install_auto(me):
        pass
    def p_install_local(me):
        pass
    def p_install_web(me):
        pass

mode_funcs_di = { "auto": mode.p_auto, "local": mode.p_local, "web": mode.p_web, 
                  "install": mode.p_install_auto, "install-local": mode.p_install_local, "install-web": mode.p_install_web }
mode_names = mode_funcs_di.keys()

# modes can be added of course

mode_lookup = dict(map(lambda key: (key, mode(key)), mode_funcs_di))
modes = mode_lookup.values()

def parse_args(lines):
    curr = mode_lookup["auto"]
    for line in lines:
        if line[0] == '$':
            mname = line[1:].strip()
            if mname in mode_names:
                curr = mode_lookup[mname]
                continue
            # else: raise Exception("unknown mode name: {}".format(mname))
        curr.args.append(line)

parse_args(filtered)
print(dict(map(lambda m: (m.name, m.args), modes))) # ok
# for m in modes:
#     m.invoke()
