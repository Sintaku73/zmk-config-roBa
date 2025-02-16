import os
import shutil

os.chdir(os.path.dirname(os.path.abspath(__file__)))

path_uf2_l = os.path.expanduser("~/zmk/app/build/left/zephyr/zmk.uf2")
path_uf2_r = os.path.expanduser("~/zmk/app/build/right/zephyr/zmk.uf2")
path_uf2_reset = os.path.expanduser("~/zmk/app/build/reset/zephyr/zmk.uf2")

uf2name_l = "roBa_L-seeeduino_xiao_ble-zmk"
uf2name_r = "roBa_R-seeeduino_xiao_ble-zmk"
uf2name_reset = "settings_reset-seeeduino_xiao_ble-zmk"

firmware_dir = "firmware"

os.makedirs(firmware_dir, exist_ok=True)

if os.path.exists(path_uf2_l):
    shutil.copy2(path_uf2_l, f"{firmware_dir}/{uf2name_l}.uf2")
else:
    print("No UF2 file for roBa_L")

if os.path.exists(path_uf2_r):
    shutil.copy2(path_uf2_r, f"{firmware_dir}/{uf2name_r}.uf2")
else:
    print("No UF2 file for roBa_R")

if os.path.exists(path_uf2_reset):
    shutil.copy2(path_uf2_reset, f"{firmware_dir}/{uf2name_reset}.uf2")
else:
    print("No UF2 file for settings_reset")
