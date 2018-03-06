
import os
import subprocess

def git(at):
    repository = at.command
    target_argument = tag_funcs._get_first_local(args_list)
    target_file = tag_funcs._format_path(target_argument.command)

    try:
        subprocess.check_call(["git", "clone"] + [repository] + [os.path.dirname(target_file)])
    except Exception as ex:
        print("Couldn't download git repository {}".format(repository), file=sys.stderr)
        raise ex

    #include <after-download.py>
