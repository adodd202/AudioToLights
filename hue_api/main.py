import PhilipsHue
import os

cfg_file = "config.txt"

def main():
    if os.path.isfile(cfg_file):
        data = get_bridge_config_data(cfg_file)
        Hue = PhilipsHue.Bridge(data[0], data[1], True)
    else:
        print("config file does not exist\n")
        Hue = PhilipsHue.Bridge()

def get_bridge_config_data(filename):
    try:
        f = open(filename, "r")
        data = f.read()
        data = data.split("\n")
    finally:
        f.close()
    return data

main()