# This file is executed on every boot (including wake-boot from deepsleep)
import esp
import machine
import sys

machine.freq(240000000)

esp.osdebug(True, esp.LOG_INFO)

sys.path.append("/display")
