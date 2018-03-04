
import subprocess

def auto(at): raise Exception("Not supposed to be here")
def local(at):
    path = at.command
    path = path.replace('/', os.path.sep).replace('\\', os.path.sep)
    
    isdir = False
    if path[-1] == os.path.sep: isdir = True
    
    if isdir: path += 'lnkpy-run.py'
    
    try:
        subprocess.check_call([path] + sys.argv, shell=True)
        # subprocess.Popen([path] + sys.argv[1:], shell=True, stdin=None, stdout=None, stderr=None, close_fds=False)
    except Exception as ex:
        print("Couldn't open file {}".format(path), file=sys.stderr)
        raise ex
