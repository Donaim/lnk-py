
#moveat imports 1
import os
#moveat global 1
osname = os.name

if arg.has_tag('-linux'):
    if osname != 'posix': args_list.remove(arg)
elif arg.has_tag('-windows'):
    if osname != 'nt': args_list.remove(arg)

