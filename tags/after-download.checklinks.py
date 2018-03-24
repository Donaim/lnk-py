#moveat global
def make_self_copy():
    import shutil #pyincluder-ignore
    import random #pyincluder-ignore
    selfpath = sys.argv[0]
    copy_dest = "~/pylnk/{}/{}".format(random.randint(1000, 9999), os.path.basename(selfpath))
    copy_dest = tag_funcs._format_path(copy_dest)
    print("copydest=", copy_dest)
    if not os.path.exists(os.path.dirname(copy_dest)): os.makedirs(os.path.dirname(copy_dest))
    shutil.copy(selfpath, copy_dest)
    return copy_dest
def check_links(target_argument, target_file):
    if target_argument.has_tag('-pylink'):
        selfpath = sys.argv[0]
        copy_dest = make_self_copy()

        template='''
#include <helpers/pythoniclink.py>
        '''
        template = template.replace('$target$', target_file.replace('\\', '\\\\'))
        template = template.replace("$fail$", copy_dest.replace('\\', '\\\\'))

        with open(selfpath, 'w+') as selffile:
            selffile.write(template)

        target_argument.command = selfpath
    elif target_argument.has_tag('-symlink'):
        selfpath = sys.argv[0]
        copy_dest = make_self_copy()
        os.remove(selfpath)
        os.symlink(target_file, selfpath)
        target_argument.command = selfpath
#endmove

check_links(target_argument, target_file)
#include <after-download.basic.py>
    