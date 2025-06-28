# Improved MicroPython-LVGL callbacks
# MIT license; Copyright (c) 2025 Carlos Gil

# Use e.g. @callback.clicked(target,...) decorator

import lvgl as lv  # noqa
import sys


def _get_event(event):
    if isinstance(event, str):
        event = getattr(lv.EVENT, event)
    return event


class Callback:
    def __init__(self): ...
    def __call__(self, f):
        def _task(*args, **kwargs):
            try:
                f(*args, **kwargs)

            except Exception as e:
                print(f"CallbackException @ {f.__name__}")
                sys.print_exception(e)

        return _task

    def event(self, *targets, event="CLICKED"):
        # print(target)

        def deco(f):
            # print(f.__name__)
            for target in targets:
                target.add_event_cb(
                    lambda *args, **kwargs: self.__call__(f)(*args, **kwargs),
                    _get_event(event),
                    None,
                )
            return

        return deco

    def clicked(self, *target):
        return self.event(*target, event="CLICKED")

    def pressing(self, *target):
        return self.event(*target, event="PRESSING")

    def pressed(self, *target):
        return self.event(*target, event="PRESSED")

    def value_changed(self, *target):
        return self.event(*target, event="VALUE_CHANGED")

    def released(self, *target):
        return self.event(*target, event="RELEASED")

    def focused(self, *target):
        return self.event(*target, event="FOCUSED")

    def defocused(self, *target):
        return self.event(*target, event="DEFOCUSED")


callback = Callback()
