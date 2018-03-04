
#include <url_regex.py>
#include <is_pathname_valid.py>

import os, sys, subprocess
class mode_initializators(object):
    def auto(at):
        if (is_pathname_valid(at.command)):
            if not 'local' in mode_lookup: raise Exception("Auto mode found local path, but no handler for it exists!") 
            at.mode = at.mode_lookup['local']
        elif(is_valid_url(at.command)):
            if not 'web' in mode_lookup: raise Exception("Auto mode found web path, but no handler for it exists!") 
            at.mode = at.mode_lookup['web']
        else: raise Exception("Path \"{}\" is neither local nor web".format(at.command))
    
    def install_auto(at):
        raise NotImplementedError()
        pass