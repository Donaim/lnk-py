
import os
import subprocess

def git(at):
    repository = at.command
    first_local_at = tag_funcs._get_first_local(args_list)
    file = tag_funcs._format_path(first_local_at.command)

    try:
        subprocess.check_call(["git", "clone"] + [repository] + [os.path.dirname(file)])
    except Exception as ex:
        print("Couldn't download git repository {}".format(repository), file=sys.stderr)
        raise ex

    # after clonning - run
    tag_funcs.local(first_local_at)
    
