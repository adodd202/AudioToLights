from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
import time
import threading
import soundRecorder
import pyaudio
import wave
import math
import threading
from hue_api import PhilipsHue
import os

globalNewBPM = 0
globalOldBPM = 0
globTimeOff = 2

def getBPM():
	while (1):
		print "LISTENING~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~SHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"
		soundRecorder.soundRecord5Sec()
		[Fs, x] = audioBasicIO.readAudioFile("file.wav");
		x = x[:,0] # sometimes necessary due to different wav files...
		winSize = .1   # size of the window to extract data from
		winStep = winSize/2 # 50% overlap steps
		F = audioFeatureExtraction.stFeatureExtraction(x, Fs, winSize*Fs, winStep*Fs);
		soundRecorder.soundRecord5Sec()
		#plt.subplot(2,1,1); plt.plot(F[0,:]); plt.xlabel('Frame no'); plt.ylabel('ZCR'); 
		#plt.subplot(2,1,2); plt.plot(F[1,:]); plt.xlabel('Frame no'); plt.ylabel('Energy'); plt.show()

		[BPM,RATIO] = audioFeatureExtraction.beatExtraction(F, winSize, PLOT=False)	

		#BPM is lower by a factor of 2 from the actual bpm. So we will multiply by 2.
		BPM = BPM * 2
		global globalNewBPM
		globalNewBPM = BPM
		print "I heard this BPM, master!", 

def get_bridge_config_data(filename):
	try:
		f = open(filename, "r")
		data = f.read()
		data = data.split("\n")
	finally:
		f.close()
	return data

def newBPMVerify():
	global globalOldBPM
	global globTimeOff

	i = 0
	while (1):
		BPM_is_similar = 1
		i += 1
		print "timer", i
		if (abs(globalNewBPM-globalOldBPM)>1):
			print "CHANGING LIGHT BPM TO", globalNewBPM
			print "CHANGING LIGHT BPM FROM", globalOldBPM
			globalOldBPM = globalNewBPM #BPM changes if it is different by more than 1 bpm.

			BPS = globalOldBPM/60.0
			globTimeOff = (1.0/BPS-.15)
			if (globTimeOff < .1):
				print ("WARNING: The computed BPM may exceed the physical light beat rate capability.")
		time.sleep(1)

def lowLevelControl():
	while (1):
		print ("On")
		Hue.set_light("1",True,254,1)   #light number, turn on, max brightness is 254, transition time (1 * 100 ms)
		time.sleep(.15)
		print ("Off")
		Hue.set_light("1",True,1,1)
		time.sleep(globTimeOff)

def mainSongListener():
	getBPMThread = threading.Thread(target = getBPM)
	lowLevelControlThread = threading.Thread(target = lowLevelControl)
	newBPMVerifyThread = threading.Thread(target = newBPMVerify)
	cfgfilepath = "hue_api\config.txt"
	if os.path.isfile(cfgfilepath):
		data = get_bridge_config_data(cfgfilepath)
		global Hue
		Hue = PhilipsHue.Bridge(data[0], data[1], True)
	else:
		print("config file does not exist\n")
		global Hue
		Hue = PhilipsHue.Bridge()

	getBPMThread.start()
	lowLevelControlThread.start()
	newBPMVerifyThread.start()

if __name__ == "__main__":
	mainSongListener()


# Every 10 seconds, let's record 5 seconds and recompute the beat rate.
# If it is different by more than 1% of current beat, change beat rate



# How to find the start of the beat? maximum energy across the beat length?


#Threading with updating global variable with locks.