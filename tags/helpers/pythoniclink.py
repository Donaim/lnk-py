import os #pyincluder-ignore
try: 
    if os.path.exists("$target$"): os.system("$target$")
    else: raise Exception()
except: os.system("$fail$")