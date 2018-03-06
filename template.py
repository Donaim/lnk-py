

TARGET_INFO='''
~/Desktop/Probf/primitive.py
https://github.com/Donaim/ProblemFlawiusza.git
https://raw.githubusercontent.com/Donaim/ProblemFlawiusza/master/primitive.py
'''

# wyzej miejsce dla adresow. wyszukiwanie jest pryorytetowane z gory do dolu
# second non-emty non-comment line is defined to be the beginning of TARGET_INFO string


        ########
       ## TAGS ##
        ########

DEFAULT_TAG = 'auto'

class tag_funcs(object):
    #include <tag_funcs.py>

# parsing tag_fucs
tag_funcs_static = filter(lambda name: name[0] != '_', dir(tag_funcs))
tag_funcs_di = dict(map(lambda name: (name, getattr(tag_funcs, name)), tag_funcs_static))

        ###########
       ## PARSING ##
        ###########

split = TARGET_INFO.split('\n')
filtered  = filter(lambda line: len(line) > 0 and not line.isspace() and line[0] != '#', split)

# filtered contains non-empty non-comment lines from TARGET_INFO

import sys
# for stderr

class arg(object):
    def __init__(self, group_tag):
        self.command = None
        self.tags = [group_tag]
        self.tags_dict = tags_dict
        self.args = args
    def invoke_tags(self):
        for t in self.tags:
            if t.invoke(self): return True
        return False
class tag(object):
    def __init__(self, name, func):
        self.name = name
        self.func = func
    def invoke(self, a):
        try:
            self.func(a)
            return True
        except ImportError: return False
        except Exception as ex:
            print(ex, file=sys.stderr)
            return False
    def by_name(name):
        if name in tags_dict: return tags_dict[name]
        else: raise Exception("unknown tag: {}".format(name))
        # else: return curr

tags_dict = dict(map(lambda p: (p[0], tag(p[0], p[1])), tag_funcs_di.items()))
args = []

def is_tag(line): return line[0] == '$'
def is_group_tag(line): is_tag(line) and line[-1] == '$'
def next_group_tag(line):
    tname = line[1:-1]
    return tag.by_name(tname)

def parse_tags(a: arg, line, curr):
    sp = line[1:].split('$')
    a.command = "$".join(sp[1:])
    for tname in sp[0].split():
        a.tags.append(tag.by_name(tname))

def parse_args(lines):
    curr = tags_dict[DEFAULT_TAG]
    for line in lines:
        if is_group_tag(line):
            curr = next_group_tag(line)
        else:
            a = arg(curr)
            if is_tag(line): parse_tags(a, line, curr)
            else: a.command = line
            args.append(a)

parse_args(filtered)

for a in args:
    if a.invoke_tags(): break
