# config / setup
import board_config

# gui / app
from gui import mgui

import sys

# debug path modules, check if running from fs " " or frozen ".frozen"
# fs shows full file path (.py or .mpy), frozen just filepath.py
for name, mod in sys.modules.items():
    if hasattr(mod, "__file__"):
        # Is a file
        print(f"- mod: {name} from {mod.__file__}")
    elif hasattr(mod, "__path__"):
        # Is a package
        print(f"- package: {name} from {mod.__path__}")

mgui.run(**board_config.conf)
