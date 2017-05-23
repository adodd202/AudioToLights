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

def getBPM():
	soundRecorder.soundRecord5Sec()
	[Fs, x] = audioBasicIO.readAudioFile("file.wav");
	x = x[:,0] #sometimes necessary due to different wav files...
	winSize = .1   # size of the window to extract data from
	winStep = winSize/2 #    50% overlap steps
	F = audioFeatureExtraction.stFeatureExtraction(x, Fs, winSize*Fs, winStep*Fs);
	soundRecorder.soundRecord5Sec()
	#plt.subplot(2,1,1); plt.plot(F[0,:]); plt.xlabel('Frame no'); plt.ylabel('ZCR'); 
	#plt.subplot(2,1,2); plt.plot(F[1,:]); plt.xlabel('Frame no'); plt.ylabel('Energy'); plt.show()

	[BPM,RATIO] = audioFeatureExtraction.beatExtraction(F, winSize, PLOT=True)	

	#BPM is lower by a factor of 2 from the actual bpm. So we will multiply by 2.
	BPM = BPM * 2
	return BPM

	#BPM_Matrix = np.zeros(1000)

def mainSongListener():
	oldBPM = 0
	while (1):
		print ("newCheck")
		newBPM = getBPM()
		print ("BPM", newBPM)
		#If the difference in the BPMs is greater than 1%, change beat
		x =oldBPM-newBPM
		control(newBPM)
		# x = abs(2)
		# if (abs(x)/newBPM > .01):
		# 	control(newBPM)




def control(BPM):
	#60 bpm is 60 times a minute (On every second, off after .2 seconds)
	BPS = BPM/60.0
	timeOff = (1.0/BPS-.1)
	if (timeOff < .1):
		print ("WARNING: The computed BPM may exceed the physical light beat rate capability.")
	while (1):
		print ("On")
		time.sleep(.1)
		print ("Off")
		time.sleep(timeOff)
	# 120 bpm 
	# 2 BPS
	# should be .5 seconds per cycle
	# on, then wait .1 seconds. off for .4
	# timeoff = 
 
 

# threads = []
# for i in range(5):
#     t = threading.Thread(target=worker, args=(i,))
#     threads.append(t)
#     t.start()




if __name__ == "__main__":
	mainSongListener()


# Every 10 seconds, let's record 5 seconds and recompute the beat rate.
# If it is different by more than 1% of current beat, change beat rate



# How to find the start of the beat? maximum energy across the beat length?


#Threading with updating global variable with locks.