[![mmds](https://github.com/Carglglz/mmds/actions/workflows/mmds_ci.yml/badge.svg)](https://github.com/Carglglz/mmds/actions/workflows/mmds_ci.yml)
## mmds


Minimal MicroPython Display System using MicroPython - LVGL + OLED monochrome display


Explore GUI development on device with a set of minimal requirements (software and hardware)


<center>

<img src="docs/img/thermometer.png" width="240" height="204">

</center>

Software:
    - MicroPython 
    - LVGL (bindings)
    - mmds:
        - drivers:
            - display 
            - indev
        - set of monochrome styles 
        - set of UI widgets
        - minimal app logic navigation
        - tests

Hardware:
    - Monochrome OLED display (128x64)
    - Potentiometer 
    - Button 
    - Temperature sensor


Demo/Simulator: (micropython unix)
    Demo/App mmds:
        - Top Status bar with widgets:
            - Bluetooth indicator 
            - Wifi signal indicator
            - Battery indicator
            - Clock
        
        - Menu Area: 3 app icons menu 

            - Apps:
                - Thermometer 
                - Temperature Graph App
                - System Info

    Demo/Tests: ui widgets, app logic

Demo/Device: 

Demo/Drivers: Tutorial of how to integrate display/indev drivers with lvgl

Demo/App mmds:
    - Top Status bar with widgets:
        - Bluetooth indicator 
        - Wifi signal indicator
        - Battery indicator
        - Clock
    
    - Menu Area: 3 app icons menu (rotate potentiometer to select)
        and click Button to enter an app, click again to return to menu.

        - Apps:
            - Thermometer 
            - Temperature Graph App
            - System Info

    
Demo/Tests on device: ui widgets, app logic

