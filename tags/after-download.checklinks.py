if a.has_tag('-pylink'):
    template='''
    #include <helpers/pythoniklink.py>
    '''
    template = template.replace('$target$', "output.lnk.py")
    template = template.replace("$fail$", "echo what????")