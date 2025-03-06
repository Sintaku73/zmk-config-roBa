#!/usr/bin/env bash

west build -p -d build/left -b "seeeduino_xiao_ble" -- -DZMK_CONFIG="/workspaces/zmk-config/config" -DSHIELD="roBa_L" -DZMK_EXTRA_MODULES="/workspaces/zmk-modules/zmk-pmw3610-driver-sayu-hub" && \
west build -p -d build/right -b "seeeduino_xiao_ble" -S "studio-rpc-usb-uart" -- -DZMK_CONFIG="/workspaces/zmk-config/config" -DSHIELD="roBa_R" -DZMK_EXTRA_MODULES="/workspaces/zmk-modules/zmk-pmw3610-driver-sayu-hub" && \
west build -p -d build/reset -b "seeeduino_xiao_ble" -- -DZMK_CONFIG="/workspaces/zmk-config/config" -DSHIELD="settings_reset" -DZMK_EXTRA_MODULES="/workspaces/zmk-modules/zmk-pmw3610-driver-sayu-hub"
