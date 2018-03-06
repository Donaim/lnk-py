def make_self_copy():
    selfpath = sys.argv[0]
    copy_dest = "~/Documents/pylnk/{}/{}".format(random.randint(1000, 9999), os.path.basename(selfpath))
    copy_dest = tag_funcs._format_path(copy_dest)
    print("copydest=", copy_dest)
    if not os.path.exists(os.path.dirname(copy_dest)): os.makedirs(os.path.dirname(copy_dest))
    shutil.copy(selfpath, copy_dest)
    return copy_dest

if target_argument.has_tag('-pylink'):
    import sys
    import subprocess
    import os
    import shutil
    import random

    selfpath = sys.argv[0]
    copy_dest = make_self_copy()

    template='''import os
    #include <helpers/pythoniclink.py>
    '''
    template = template.replace('$target$', target_file.replace('\\', '\\\\'))
    template = template.replace("$fail$", copy_dest.replace('\\', '\\\\'))
    
    with open(selfpath, 'w+') as selffile:
        lines = map(lambda l: l.lstrip() + '\n', template.split('\n'))
        selffile.writelines(lines)

    target_argument.command = selfpath
elif target_argument.has_tag('-symlink'):
    selfpath = sys.argv[0]
    copy_dest = make_self_copy()
    os.remove(selfpath)
    os.symlink(target_file, selfpath)
    target_argument.command = selfpath

#include <after-download.basic.py>
    