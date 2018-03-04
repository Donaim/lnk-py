
import os

def git(at):
    repository = at.command
    first_local_at = mode_funcs._get_first_local(at.args_t)
    file = mode_funcs._format_path(first_local_at.command)

    try:
        subprocess.call(["git", "clone"] + [repository] + [os.path.dirname(file)])
        # subprocess.Popen([path] + sys.argv[1:], shell=True, stdin=None, stdout=None, stderr=None, close_fds=False)
    except Exception as ex:
        print("Couldn't download git repository {}".format(repository), file=sys.stderr)
        raise ex

    # after clonning - run
    first_local_at.invoke()
    
