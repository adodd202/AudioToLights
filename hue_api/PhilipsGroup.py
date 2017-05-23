import sys
import json
import requests as r
import time

class PhilipsGroup:
    def __init(self, name_, all_on_, any_on_, lights_):
        self.name = name_
        self.all_on = all_on_
        self.any_on = any_on_
        self.lights = lights_