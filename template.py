

TARGET_INFO='''
~/Desktop/Probf/primitive.py
https://github.com/Donaim/ProblemFlawiusza.git
# https://raw.githubusercontent.com/Donaim/ProblemFlawiusza/master/primitive.py
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
    def __init__(self):
        self.command = None
        self.tags = []
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
        except ImportError: return False # ignoring those
        except Exception as ex:
            print(ex, file=sys.stderr)
            return False
    def by_name(name):
        if name in tags_dict: return tags_dict[name]
        else: raise Exception("unknown tag: \"{}\"".format(name))
        # else: return curr

tags_dict = dict(map(lambda p: (p[0], tag(p[0], p[1])), tag_funcs_di.items()))
args = []

def is_tag(line: str) -> bool: return line.lstrip()[0] == '$'
def is_group_tag(first: str, second: str) -> bool: return len(second) == 0
def parse_tags(first: str) -> list:
    if len(first) == 0: return []
    return list(map(lambda tname: tag.by_name(tname), first.split(' \t,')))
def find_tag_close(line: str) -> int:
    for (i, c) in enumerate(line):
        if c == '$': return i
    return 0
def split_by_tag(line: str) -> (str, str):
    if is_tag(line):
        line = line.lstrip()[1:] # skip first '$' char
        close_index = find_tag_close(line)
        first = line[:close_index].strip(' \t,')
        second = line[close_index:].lstrip()
        return (first, second)
    else:
        return ('', line)

def parse_args(lines):
    group_tags = [tags_dict[DEFAULT_TAG]]
    for line in lines:
        (first, second) = split_by_tag(line)
        if is_group_tag(first, second):
            group_tags = parse_tags(first)
        else:
            a = arg()
            a.tags = group_tags + parse_tags(first)
            a.command = second
            args.append(a)

parse_args(filtered)

for a in args: print('arg \"{}\" has tags={}'.format(a.command, list(map(lambda t: t.name, a.tags))))
for a in args:
    if a.invoke_tags(): break
