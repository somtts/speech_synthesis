import soundfile as sf
import numpy as np
import utility
import sys
from scipy import signal
import matplotlib.pyplot as plt


# takes a list of diphones and outputs a wav file with the wavs of each
# diphone (taken from the diphones_path) concatenated
def synthesize(diphones_wavs_lib,diphones):
    try:
        diphone_wavs=map(lambda diphone: diphones_wavs_lib[diphone],diphones)
    except KeyError, e:
        sys.exit("Diphone %s was not found" % str(e))
    return concat_wav(diphone_wavs)

# concatenate multiple wavs into a single one
# by repeatedly concatenating two wavs
def concat_wav(wavs): #fold over wavs with concat2_wav
    output_wav=concat2_wav(wavs[0],wavs[1])
    for i in xrange(2,len(wavs)):
        output_wav=concat2_wav(np.copy(output_wav),wavs[i])
    return output_wav


# concatenates two sound signals wav1 and wav2
# and smoothes interval around the union
def concat2_wav(wav1,wav2):

    output_wav=np.hstack([wav1,wav2])
    sigma=2
    desired_radius=10
    position=len(wav1)
    output_wav_smoothed=smooth_wav(output_wav,position,sigma,desired_radius)

    # f, axarr = plt.subplots(2,sharex=True,sharey=True)
    # axarr[0].plot(output_wav)
    # axarr[0].set_title('original' )
    #
    # axarr[1].plot(output_wav_smoothed)
    # axarr[1].set_title('smoothed at %d' % position)
    # plt.show()

    return output_wav_smoothed


def smooth_wav(wav,position,sigma,desired_radius):
    smoothed_wav=np.copy(wav)
    window=gaussian_window(sigma)
    radius=smoothing_radius(desired_radius,position,wav,len(window))
    smoothed_wav[position]=smooth_position(wav,position,window)
    for i in xrange(radius+1):
        smoothed_wav[position+i]=smooth_position(wav,position+i,window)
        smoothed_wav[position-i]=smooth_position(wav,position-i,window)
    return  smoothed_wav

# creates a gaussian window with sigma standard deviation
def gaussian_window(sigma):
    truncate_at_sd=4
    window_size= 2*int(truncate_at_sd * sigma + 0.5)+1
    window = signal.gaussian(window_size, std=sigma)
    window=window/np.sum(window)
    #print np.sum(window)
    return window

# calculates the filtering radius for a desired radius,
# which can result in a smaller radius depending on the position-radius
# and length of the wav
def smoothing_radius(desired_radius,position,wav,window_size):
    n=len(wav)

    #possibly make radius smaller based on position and n
    min_length=min(position-1,n-position)
    radius=min(min_length,desired_radius)

    #possibly make radius smaller based on window size and n
    #window_half_size=(window_size-1)/2
    #excess_at_beginning= abs( min((position-radius)-window_half_size,0))
    #excess_at_end= abs( min((position-radius)-window_half_size,0))
    #radius=min( max(excess_at_beginning,excess_at_end),radius)
    return radius


# size of window must be odd
def smooth_position(signal,position,window):
    radius=(len(window)-1)/2
    return np.dot(window,signal[(position-radius):(position+radius+1)])
