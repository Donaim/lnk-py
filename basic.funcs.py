
import urllib.request
import os
import subprocess

def auto(at): raise Exception("Not supposed to be here")
def _format_path(path):
    path = path.replace('/', os.path.sep).replace('\\', os.path.sep)
    if (path[0] == '~'): return os.path.expanduser('~') + path[1:]
    else: return path

def local(at):
    path = mode_funcs._format_path(at.command)
    
    isdir = True if path[-1] == os.path.sep else False
    if isdir: path += 'lnkpy-run.py'
    
    if not os.path.exists(path): raise Exception("local path \"{}\" does not exist!".format(path))
    
    try:
        subprocess.call([path] + sys.argv[1:], shell=True)
    except Exception as ex:
        print("Couldn't open file {}".format(path), file=sys.stderr)
        raise ex

def _get_first_local(args_t):
    for a in args_t:
        if a.mode.name == 'local': return a 
def web(at):
    def try_get_file_size(meta):
        re = 0.0
        try:
            re = int(meta.get("Content-Length"))
        except: pass
        return re

    target_at = mode_funcs._get_first_local(at.args_t)
    file_name = target_at.command
    file_name = mode_funcs._format_path(file_name)
    di = os.path.dirname(file_name)
    if not os.path.isdir(di): os.mkdir(di)

    url = at.command
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

    mode_funcs.local(target_at)