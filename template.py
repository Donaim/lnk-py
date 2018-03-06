TARGET_INFO='''
#include <target_info.txt>
'''

DEFAULT_TAG = 'auto'

class tag_funcs(object):
    #include <tag_funcs.py>
    pass

# parsing tag_fucs
tag_funcs_static = filter(lambda name: name[0] != '_', dir(tag_funcs))
tag_funcs_di = dict(map(lambda name: (name, getattr(tag_funcs, name)), tag_funcs_static))

# for stderr
import sys

class arg(object):
    def __init__(self):
        self.command = None
        self.tags = []
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
        elif name[0] == '-': return tag(name, None) # pure tag
        else: raise Exception("tag [{}] doesn't have handler!".format(name)) 
def parse_args():
    def is_tag(line: str) -> bool: 
        return line.lstrip()[0] == '$'
    def is_group_tag(first: str, second: str) -> bool: 
        return len(second) == 0 or second.isspace()
    def split_tags(line):
        return filter(lambda s: len(s) > 0, (line.replace(' ', ',').replace('\t', ',')).split(','))
    def parse_tags(first: str) -> list:
        if len(first) == 0: return []
        return list(map(lambda tname: tag.by_name(tname), split_tags(first)))
    def find_tag_close(line: str) -> int:
        for (i, c) in enumerate(line):
            if c == ']': return i
        return len(line)
    def split_by_tag(line: str) -> (str, str):
        if is_tag(line):
            line = line.lstrip()[1:] # skip first '$' char
            close_index = find_tag_close(line)
            first = line[:close_index].strip(' \t,[]')
            second = line[close_index + 1:].lstrip()
            return (first, second)
        else:
            return ('', line)
    
    #lines
    split = TARGET_INFO.split('\n')
    lines = filter(lambda line: len(line) > 0 and not line.isspace() and line[0] != '#', split)

    #parsing
    group_tags = [tags_dict[DEFAULT_TAG]]
    for line in lines:
        (first, second) = split_by_tag(line)
        if is_group_tag(first, second):
            group_tags = parse_tags(first)
        else:
            a = arg()
            a.tags = group_tags + parse_tags(first)
            a.command = second
            args_list.append(a)
    
    #invoking tags
    for a in args_list:
        for t in a.tags:
            if t.func == None: continue # pure tag, do not invoke
            if t.invoke(a): break       # if some tag succeded with args, end the program

tags_dict = dict(map(lambda p: (p[0], tag(p[0], p[1])), tag_funcs_di.items()))
args_list = []
parse_args()

