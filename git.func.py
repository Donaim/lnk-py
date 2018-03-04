
def git(at):
    path = at.command
    
    try:
        subprocess.call([path] + sys.argv)
        # subprocess.Popen([path] + sys.argv[1:], shell=True, stdin=None, stdout=None, stderr=None, close_fds=False)
    except Exception as ex:
        print("Couldn't open file {}".format(path), file=sys.stderr)
        raise ex

    at.mode
