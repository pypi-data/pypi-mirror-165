from .roll_body import RollBody
from .disk_element import DiskElement

from pyroll.core import RollPass, Roll
from pyroll.ui import Reporter

from . import roll_hookimpls
from . import roll_hookspecs
from . import rollpass_roll_hookimpls
from . import rollpass_roll_hookspecs
from . import reporter_impls

Roll.plugin_manager.add_hookspecs(roll_hookspecs)
RollPass.Roll.plugin_manager.add_hookspecs(rollpass_roll_hookspecs)

Roll.plugin_manager.register(roll_hookimpls)
RollPass.Roll.plugin_manager.register(rollpass_roll_hookimpls)

Reporter.plugin_manager.register(reporter_impls)
