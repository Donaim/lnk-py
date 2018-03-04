
import os

def git(at):
    def get_first_local_dir_at():
        for a in at.args_t:
            if a.mode.name == 'local' and a.command[-1] == os.path.sep: return a 

    repository = at.command
    first_local_at = get_first_local_dir_at()

    try:
        subprocess.call(["git", "clone"] + [repository] + [first_local_at.command])
        # subprocess.Popen([path] + sys.argv[1:], shell=True, stdin=None, stdout=None, stderr=None, close_fds=False)
    except Exception as ex:
        print("Couldn't download git repository {}".format(repository), file=sys.stderr)
        raise ex

    # after clonning - run
    first_local_at.invoke()
    
