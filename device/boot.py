# boot.py -- run on boot to configure USB and filesystem
# Put app code in main.py

import pyb
import sys
import os

# pyb.main('main.py') # main script to run after this one
pyb.usb_mode("VCP")  # act as a serial and a storage device
# pyb.usb_mode('VCP+HID') # act as a serial device and a mouse
# import network
# network.country('US') # ISO 3166-1 Alpha-2 code, eg US, GB, DE, AU or XX for worldwide
# network.hostname('...') # DHCP/mDNS hostname


# sys.path.append(f"{os.getcwd()}/gui")
sys.path.append(f"{os.getcwd()}/display")
