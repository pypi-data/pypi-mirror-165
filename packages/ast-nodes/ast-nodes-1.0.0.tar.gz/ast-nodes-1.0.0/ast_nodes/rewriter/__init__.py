from sys import version_info
ver = version_info[:2]    

if ver == (3,6):
    from .rewriter36 import *
elif ver == (3,7):
    from .rewriter37 import *
elif ver == (3,8):
    from .rewriter38 import *
elif ver == (3,9):
    from .rewriter39 import *
elif ver == (3,10):
    from .rewriter310 import *
elif ver == (3,11):
    from .rewriter311 import *
else: raise NotImplementedError(f'python version not supported: {ver}')
