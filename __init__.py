from . import server, base, sthpw, vfx
from .vfx import sobjects as _vfx_sobjects
from .sthpw import sobjects as _sthpw_sobjects

import sys
import imp


reload_order = [server, base, _sthpw_sobjects, sthpw, _vfx_sobjects, vfx]


def reload_package():
    for module in reload_order[-2::-1]:
        del module
    imp.reload(sys.modules[__name__])
