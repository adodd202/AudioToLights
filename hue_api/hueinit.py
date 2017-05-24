import PhilipsHue
import os

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
	Hue.set_light("1", False, 254, 1)
else:
	print("importing hueinit")
	cfg_file = "hue_api/config.txt"
