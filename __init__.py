from . import server, base, sthpw, vfx
from .vfx import sobjects as _vfx_sobjects
from .sthpw import sobjects as _sthpw_sobjects


import sys


from .server import get_server


reload_order = [server, base, _sthpw_sobjects, sthpw, _vfx_sobjects, vfx]


def delete_package():
    for name in sys.modules.copy():
        if name.startswith(__name__):
            del sys.modules[name]
