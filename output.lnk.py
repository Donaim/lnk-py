import re
import os
import sys
import subprocess
import urllib.request

TARGET_INFO='''

$ -windows  ,  local
~/Desktop/Probf/primitive.py
$git
https://github.com/Donaim/ProblemFlawiusza.git
$[-windows] https://raw.githubusercontent.com/Donaim/ProblemFlawiusza/master/primitive.py

'''

# wyzej miejsce dla adresow. wyszukiwanie jest pryorytetowane z gory do dolu
# second non-emty non-comment line is defined to be the beginning of TARGET_INFO string


        ########
       ## TAGS ##
        ########

DEFAULT_TAG = 'auto'

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
            
            if len(pathname) < 1: return False
            _, pathname = os.path.splitdrive(pathname)
            root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
                if sys.platform == 'win32' else os.path.sep
            assert os.path.isdir(root_dirname)   # ...Murphy and her ironclad Law
            root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep
            for pathname_part in pathname.split(os.path.sep):
                try: os.lstat(root_dirname + pathname_part)
                except OSError as exc:
                    if hasattr(exc, 'winerror'):
                        if exc.winerror == 123: # ERROR_INVALID_NAME = 123
                            return False
                    elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                        return False
        except TypeError as exc: return False
        else: return True
    
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
    
        target_at = tag_funcs._get_first_local(a.args)
        file_name = target_at.command
        file_name = tag_funcs._format_path(file_name)
        di = os.path.dirname(file_name)
        if not os.path.isdir(di): os.mkdir(di)
    
        url = a.command
        u = urllib.request.urlopen(url)
    
        meta = u.info()
        file_size = try_get_file_size(meta)
    
        f = open(file_name, 'wb')
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
    
        tag_funcs.local(target_at)
    
    
    def git(at):
        repository = at.command
        first_local_at = tag_funcs._get_first_local(at.args)
        file = tag_funcs._format_path(first_local_at.command)
    
        try:
            subprocess.check_call(["git", "clone"] + [repository] + [os.path.dirname(file)])
        except Exception as ex:
            print("Couldn't download git repository {}".format(repository), file=sys.stderr)
            raise ex
    
        # after clonning - run
        tag_funcs.local(first_local_at)
        


    pass

# parsing tag_fucs
tag_funcs_static = filter(lambda name: name[0] != '_', dir(tag_funcs))
tag_funcs_di = dict(map(lambda name: (name, getattr(tag_funcs, name)), tag_funcs_static))

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
            if self.func == None: raise ImportError
            self.func(a)
            return True
        except ImportError: return False # ignoring those
        except Exception as ex:
            print(ex, file=sys.stderr)
            return False
    def by_name(name):
        if name in tags_dict: return tags_dict[name]
        elif name[0] == '-': return tag(name, None) # pure tag
        else: raise Exception("tag [{}] doesn't have handler!".format(name)) #  (if you wanted to have tag without handler, name it with like '-mytag')
def parse_args():
    def is_tag(line: str) -> bool: 
        return line.lstrip()[0] == '$'
    def is_group_tag(first: str, second: str) -> bool: 
        return len(second) <= 0 or second.isspace()
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
    
    split = TARGET_INFO.split('\n')
    lines = filter(lambda line: len(line) > 0 and not line.isspace() and line[0] != '#', split)

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

tags_dict = dict(map(lambda p: (p[0], tag(p[0], p[1])), tag_funcs_di.items()))
args = []
parse_args()

for a in args:
    if a.invoke_tags(): break
