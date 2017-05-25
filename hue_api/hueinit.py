import PhilipsHue
import os
import time

def hueinit():
	if os.path.isfile(cfg_file):
		data = get_bridge_config_data(cfg_file)
		Hue = PhilipsHue.Bridge(data[0], data[1], True)
	else:
		print("config file does not exist\n")
		Hue = PhilipsHue.Bridge()
	return Hue

def get_bridge_config_data(filename):
	try:
		f = open(filename, "r")
		data = f.read()
		data = data.split("\n")
	finally:
		f.close()
	return data


cfg_file = str()
if __name__ == "__main__":
	print("calling hueinit")
	cfg_file = "config.txt"
	Hue = hueinit()
	Hue.get_light_names()
	while(1):
		Hue.set_light(1, True, 1, 1)
		time.sleep(0.1)
		Hue.set_light(1, True, 254, 1)
		time.sleep(0.1)
else:
	print("importing hueinit")
	cfg_file = "hue_api/config.txt"
