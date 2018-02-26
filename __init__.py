from . import server, base, sthpw, vfx, config
from .vfx import sobjects as _vfx_sobjects
from .sthpw import sobjects as _sthpw_sobjects
from .config import sobjects as _config_sobject


import sys


from .server import get_server, logout, login


reload_order = [server, base, _sthpw_sobjects, sthpw, _vfx_sobjects, vfx,
                _config_sobject, config]


def delete_sub_packages():
    for name in sys.modules.copy():
        if name.startswith(__name__ + '.'):
            del sys.modules[name]


def delete_package():
    for name in sys.modules.copy():
        if name.startswith(__name__):
            del sys.modules[name]


def reload_package():
    delete_sub_packages()
    reload(sys.modules[__name__])
