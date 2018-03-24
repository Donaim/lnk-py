
#moveat imports 1
import platform

osname = platform.system()

if arg.has_tag('-linux'):
    if osname != 'Linux': args_list.remove(arg)
elif arg.has_tag('-windows'):
    if osname != 'Windows': args_list.remove(arg)

