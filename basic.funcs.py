

def auto(at): raise Exception("Not supposed to be here")
def local(at):
    path = at.command
    path = path.replace('/', os.path.sep).replace('\\', os.path.sep)
    
    isdir = False
    if path[-1] == os.path.sep: isdir = True
    
    if isdir: path += 'lnkpy-run.py'
    
    try:
        subprocess.call([path] + sys.argv)
        # subprocess.Popen([path] + sys.argv[1:], shell=True, stdin=None, stdout=None, stderr=None, close_fds=False)
    except Exception as ex:
        print("Couldn't open file {}".format(path), file=sys.stderr)
        raise ex

def web(at):
    if at.command[-1] == 'N': raise Exception(":(")
    print("Hello from web", at.command)
def install(at): raise Exception("Not supposed to be here")
def install_local(at):
    print("Hello from install_local", at.command)
def install_web(at):
    print("Hello from install_web", at.command)