#!/bin/bash

# Device path
DEV_PATH='/dev/ttyACM0'

# Submodule paths
LCD_DRIVER_SRCDIR='submodules/micropython-i2c-lcd/lib'
RE_DRIVER_SRCDIR='submodules/micropython-rotary'
MODULE_DIR='src/lib'

# Connect to target machine
mpremote connect "${DEV_PATH}"

# Deploy LCD drivers
mpremote fs cp -f "${LCD_DRIVER_SRCDIR}/i2c_lcd_backlight.py" :lib/
mpremote fs cp -f "${LCD_DRIVER_SRCDIR}/i2c_lcd_screen.py" :lib/
mpremote fs cp -f "${LCD_DRIVER_SRCDIR}/i2c_lcd.py" :lib/

# Deploy rotary-encoder drivers
mpremote fs cp -f "${RE_DRIVER_SRCDIR}/rotary.py" :/lib
mpremote fs cp -f "${RE_DRIVER_SRCDIR}/rotary_irq_rp2.py" :/lib

# Deploy Danielle's modules
# mpremote fs cp -f "${MODULE_DIR}/*.py" :/lib
mpremote fs cp -f "${MODULE_DIR}/models.py" :/lib
mpremote fs cp -f "${MODULE_DIR}/utils.py" :/lib

# Deploy main
mpremote fs cp -f src/main.py :main.py
