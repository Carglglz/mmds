# config / setup

import board_config

# gui
# config which app to run --> app template
if hasattr(board_config, "app"):
    import sys

    sys.path.append("apps")
    app = __import__(board_config.app, [], [], [])

else:
    from gui import mgui as app


# gc.collect()

import sys

# debug path modules, check if running from fs " " or frozen ".frozen"
# fs shows full file path (.py or .mpy), frozen just filepath.py
for name, mod in sorted(sys.modules.items()):
    if hasattr(mod, "__file__"):
        # Is a file
        print(f"- mod: {name} from {mod.__file__}")
    elif hasattr(mod, "__path__"):
        # Is a package
        print(f"- package: {name} from {mod.__path__}")

print(f"APP: {app.__name__} from {app.__file__}")
app.run(**board_config.conf)
