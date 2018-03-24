#include <helpers/url_regex.py>
#include <helpers/is_pathname_valid.py>

def auto(a):
    if (tag_funcs._is_pathname_valid(a.command)):
        # print('adding local')
        try: a.tags.append(tag.by_name('local'))        
        except: raise Exception("Auto mode found local path, but no handler for it exists!") 
    elif(tag_funcs._is_valid_url(a.command)):
        try: a.tags.append(tag.by_name('web'))
        except: raise Exception("Auto mode found web path, but no handler for it exists!") 
    else: raise Exception("Path \"{}\" is neither local nor web".format(a.command))
    raise ImportError
