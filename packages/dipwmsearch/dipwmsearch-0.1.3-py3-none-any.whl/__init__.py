# SOL https://py-pkgs.org/04-package-structure.html
# read version from installed package
from importlib.metadata import version
__version__ = version("dipwmsearch")

# ##################################################
print ( __version__ )
# ##################################################

from .AhoCorasick import *
# from .BestWords import *
from .Block import *
from .diPwm import *
from .Enumerate import *
from .SemiNaive import *
# from .Super import *

#
