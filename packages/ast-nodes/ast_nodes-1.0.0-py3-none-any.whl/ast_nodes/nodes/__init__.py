from sys import version_info
ver = version_info[:2]    

if ver == (3,6):
    from .nodes36 import *
elif ver == (3,7):
    from .nodes37 import *
elif ver == (3,8):
    from .nodes38 import *
elif ver == (3,9):
    from .nodes39 import *
elif ver == (3,10):
    from .nodes310 import *
elif ver == (3,11):
    from .nodes311 import *
else: raise NotImplementedError(f'python version not supported: {ver}')
