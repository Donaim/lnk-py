TARGET_INFO='''
$[-pylink] ~/Desktop/Probf/primitive.py
$[-symlink] ~/Desktop/Probf/primitive.py
$[-windows] https://raw.githubusercontent.com/Donaim/ProblemFlawiusza/master/primitive.py
$[-linux] https://github.com/Donaim/ProblemFlawiusza.git
# $ -windows  ,  local

# jest tutaj miejsce dla adresow. wyszukiwanie jest pryorytetowane z gory do dolu
# second non-emty non-comment line is defined to be the beginning of TARGET_INFO string

'''

# for stderr
import sys
import re
import os
import urllib.request
import os
import subprocess
import os
import subprocess
import os

DEFAULT_TAG = 'auto'

osname = os.name
def make_self_copy():
    import shutil #pyincluder-ignore
    import random #pyincluder-ignore
    selfpath = sys.argv[0]
    copy_dest = "~/pylnk/{}/{}".format(random.randint(1000, 9999), os.path.basename(selfpath))
    copy_dest = tag_funcs._format_path(copy_dest)
    print("copydest=", copy_dest)
    if not os.path.exists(os.path.dirname(copy_dest)): os.makedirs(os.path.dirname(copy_dest))
    shutil.copy(selfpath, copy_dest)
    return copy_dest
def check_links(target_argument, target_file):
    if target_argument.has_tag('-pylink'):
        selfpath = sys.argv[0]
        copy_dest = make_self_copy()

        template='''
import os
try: 
    if os.path.exists("$target$"): os.system("$target$")
    else: raise Exception()
except: os.system("$fail$")
        '''
        template = template.replace('$target$', target_file.replace('\\', '\\\\'))
        template = template.replace("$fail$", copy_dest.replace('\\', '\\\\'))

        with open(selfpath, 'w+') as selffile:
            selffile.write(template)

        target_argument.command = selfpath
    elif target_argument.has_tag('-symlink'):
        selfpath = sys.argv[0]
        copy_dest = make_self_copy()
        os.remove(selfpath)
        os.symlink(target_file, selfpath)
        target_argument.command = selfpath

class tag_funcs(object):
    
    # #include <tags/basic-auto.py>
    
        # The MIT License (MIT)
    
        # Copyright (c) 2013-2014 Konsta Vesterinen
    
        # Permission is hereby granted, free of charge, to any person obtaining a copy of
        # this software and associated documentation files (the "Software"), to deal in
        # the Software without restriction, including without limitation the rights to
        # use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
        # the Software, and to permit persons to whom the Software is furnished to do so,
        # subject to the following conditions:
    
        # The above copyright notice and this permission notice shall be included in all
        # copies or substantial portions of the Software.
    
        # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
        # FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
        # COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
        # IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
        # CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    
        # SOURCE REPOSITORY: https://github.com/kvesteri/validators
    
    ip_middle_octet = u"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5]))"
    ip_last_octet = u"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    
    url_regex = re.compile(
        u"^"
        # protocol identifier
        u"(?:(?:https?|ftp)://)"
        # user:pass authentication
        u"(?:[-a-z\u00a1-\uffff0-9._~%!$&'()*+,;=:]+"
        u"(?::[-a-z0-9._~%!$&'()*+,;=:]*)?@)?"
        u"(?:"
        u"(?P<private_ip>"
        # IP address exclusion
        # private & local networks
        u"(?:(?:10|127)" + ip_middle_octet + u"{2}" + ip_last_octet + u")|"
        u"(?:(?:169\.254|192\.168)" + ip_middle_octet + ip_last_octet + u")|"
        u"(?:172\.(?:1[6-9]|2\d|3[0-1])" + ip_middle_octet + ip_last_octet + u"))"
        u"|"
        # private & local hosts
        u"(?P<private_host>"
        u"(?:localhost))"
        u"|"
        # IP address dotted notation octets
        # excludes loopback network 0.0.0.0
        # excludes reserved space >= 224.0.0.0
        # excludes network & broadcast addresses
        # (first & last IP address of each class)
        u"(?P<public_ip>"
        u"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
        u"" + ip_middle_octet + u"{2}"
        u"" + ip_last_octet + u")"
        u"|"
        # host name
        u"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
        # domain name
        u"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
        # TLD identifier
        u"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
        u")"
        # port number
        u"(?::\d{2,5})?"
        # resource path
        u"(?:/[-a-z\u00a1-\uffff0-9._~%!$&'()*+,;=:@/]*)?"
        # query string
        u"(?:\?\S*)?"
        # fragment
        u"(?:#\S*)?"
        u"$",
        re.UNICODE | re.IGNORECASE
    )
    
    url_pattern = re.compile(url_regex)
    
    def _is_valid_url(value, public = False):
        result = tag_funcs.url_pattern.match(value)
        if not public:
            return result
    
        return result and not any((result.groupdict().get(key) for key in ('private_ip', 'private_host')))
    

    
    def _is_pathname_valid(pathname: str) -> bool: # https://stackoverflow.com/a/34102855/7038168
        try:
            full = os.path.expanduser(pathname)
            if osname == 'posix':
                return full[0] == os.path.sep # the only condition
            elif osname == 'nt': # thats windows
                return full[1] == ':' and full[2] == os.path.sep
        except:
            return False

    
    def _is_valid_git(url: str):
        return url.endswith(".git")
    def auto(a):
        if (tag_funcs._is_pathname_valid(a.command)):
            # print('adding local')
            try: a.tags.append(tag.by_name('local'))        
            except: raise Exception("Auto mode found local path, but no handler for it exists!") 
        elif(tag_funcs._is_valid_url(a.command)):
            if(tag_funcs._is_valid_git(a.command)):
                try: a.tags.append(tag.by_name('git'))
                except: raise Exception("Auto mode found git repository, but no handler for it exists!") 
            else:
                try: a.tags.append(tag.by_name('web'))
                except: raise Exception("Auto mode found web path, but no handler for it exists!") 
        else: raise Exception("Path \"{}\" is neither local nor web".format(a.command))
        raise ImportError

    
    
    
    def _format_path(path):
        path = path.replace('/', os.path.sep).replace('\\', os.path.sep)
        if (path[0] == '~' and path[1] == os.path.sep): path = os.path.expanduser('~') + path[1:]
        return path
    
    def local(a):
        path = tag_funcs._format_path(a.command)
        
        isdir = True if path[-1] == os.path.sep else False
        if isdir: path += 'lnkpy-run.py'
        
        if not os.path.exists(path): raise Exception("local path \"{}\" does not exist!".format(path))
        
        try:
            subprocess.call([path] + sys.argv[1:], shell=True)
        except Exception as ex:
            print("Couldn't open file {}".format(path), file=sys.stderr)
            raise ex
    
    def _get_first_local(args):
        for a in args:
            if 'local' in map(lambda t: t.name, a.tags): return a
        raise Exception("TARGET_INFO contains not local args!!")
    def web(a):
        def try_get_file_size(meta):
            re = 0.0
            try:
                re = int(meta.get("Content-Length"))
            except: pass
            return re
    
        target_argument = tag_funcs._get_first_local(args_list)
        target_file = target_argument.command
        target_file = tag_funcs._format_path(target_file)
        di = os.path.dirname(target_file)
        if not os.path.isdir(di): os.mkdir(di)
    
        url = a.command
        u = urllib.request.urlopen(url)
    
        meta = u.info()
        file_size = try_get_file_size(meta)
    
        f = open(target_file, 'wb')
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer: break
    
            file_size_dl += len(buffer)
            f.write(buffer)
       
            status = "downloading.. {:10d}b".format(file_size_dl)
            if file_size > 0: status += " ({:3.2f} %)".format(file_size_dl * 100. / file_size)
            print(status)
    
        f.close()
    
        
        
        check_links(target_argument, target_file)
        
        tag_funcs.local(target_argument)
            
        # #include <after-download.basic.py>

    
    
    def git(a):
        repository = a.command
        target_argument = tag_funcs._get_first_local(args_list)
        target_file = tag_funcs._format_path(target_argument.command)
    
        try:
            subprocess.check_call(["git", "clone"] + [repository] + [os.path.dirname(target_file)])
        except Exception as ex:
            print("Couldn't download git repository {}".format(repository), file=sys.stderr)
            raise ex
    
        
        
        check_links(target_argument, target_file)
        
        tag_funcs.local(target_argument)
            
        # #include <after-download.basic.py>


    pass
def init_func(arg):
    
    
    osname = os.name
    
    if arg.has_tag('-linux'):
        if osname != 'posix': args_list.remove(arg)
    elif arg.has_tag('-windows'):
        if osname != 'nt': args_list.remove(arg)
    

    

    pass

# parsing tag_fucs
tag_funcs_static = filter(lambda name: name[0] != '_', dir(tag_funcs))

class arg(object):
    def __init__(self):
        self.command = None
        self.tags = []
    def has_tag(self, tname): return any(map(lambda t: t.name == tname, self.tags))
    def __repr__(self): return '(command:"{}"  tags:[{}])'.format(self.command, ','.join(map(lambda t: t.name, self.tags)))
class tag(object):
    def __init__(self, name, func):
        self.name = name
        self.func = func
    def invoke(self, a):
        try:
            if self.func == None: return False # pure tag, do not invoke
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
    def is_group_tag(aleft: str, aright: str) -> bool: 
        return len(aright) == 0 or aright.isspace()
    def split_tags(line):
        return filter(lambda s: len(s) > 0, (line.replace(' ', ',').replace('\t', ',')).split(','))
    def parse_tags(aleft: str) -> list:
        if len(aleft) == 0: return []
        return list(map(lambda tname: tag.by_name(tname), split_tags(aleft)))
    def find_tag_close(line: str) -> int:
        for (i, c) in enumerate(line):
            if c == ']': return i
        return len(line)
    def split_by_tag(line: str) -> (str, str):
        if is_tag(line):
            line = line.lstrip()[1:] # skip aleft '$' char
            close_index = find_tag_close(line)
            aleft = line[:close_index].strip(' \t,[]')
            aright = line[close_index + 1:].lstrip()
            return (aleft, aright)
        else:
            return ('', line)
    
    #lines
    split = TARGET_INFO.split('\n')
    lines = filter(lambda line: len(line) > 0 and not line.isspace() and line[0] != '#', split)

    #parsing
    group_tags = [tags_dict[DEFAULT_TAG]]
    for line in lines:
        (aleft, aright) = split_by_tag(line)
        if is_group_tag(aleft, aright):
            group_tags = parse_tags(aleft)
        else:
            a = arg()
            a.tags = parse_tags(aleft) + group_tags
            a.command = aright
            args_list.append(a)
def init_args():
    for a in args_list.copy():
        init_func(a)
def invoke_tags():
    for a in args_list:
        for t in a.tags:
            if t.invoke(a): return      # if some tag succeded with args, end the program
tags_dict = dict(map(lambda name: (name, tag(name, getattr(tag_funcs, name))), tag_funcs_static))
args_list = []

def main():
    parse_args()
    init_args()
    invoke_tags()
if __name__ == "__main__":
    main()