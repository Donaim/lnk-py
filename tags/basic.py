
import urllib.request
import os
import subprocess

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