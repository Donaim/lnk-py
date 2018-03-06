if target_argument.has_tag('-pylink'):
    import sys
    import subprocess
    import os
    import shutil
    import random

    selfpath = sys.argv[0]
    copy_dest = "~/Documents/pylnk/{}/{}".format(random.randint(1000, 9999), os.path.basename(selfpath))
    copy_dest = tag_funcs._format_path(copy_dest)
    print("copydest=", copy_dest)
    if not os.path.exists(os.path.dirname(copy_dest)): os.makedirs(os.path.dirname(copy_dest))
    shutil.copy(selfpath, copy_dest)

    template='''import os
    #include <helpers/pythoniclink.py>
    '''
    template = template.replace('$target$', target_file)
    template = template.replace("$fail$", copy_dest)
    template = template.replace('\\', '\\\\')
    
    with open(selfpath, 'w+') as selffile:
        lines = map(lambda l: l.lstrip() + '\n', template.split('\n'))
        selffile.writelines(lines)

    p = subprocess.Popen(selfpath, shell=True)
    p.wait()
    exit(0)