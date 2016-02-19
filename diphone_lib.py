import soundfile as sf
import numpy as np
import utility
import os
import matplotlib.pyplot as plt
import ttslib as ttslib

def preprocess_diphone(name,diphone):
    #TODO REMOVE WHEN USING BETTER DIPHONES
    # n=len(diphone)
    # if name[0]=='-':
    #     diphone=diphone[0:n/2]
    # elif name[-1]=='-':
    #     diphone=diphone[n/2:-1]
    # else:
    #     diphone=diphone[n/3-100:(n/3)*2+100]

    #normalize amplitude
    preprocessed_diphone=diphone/max(diphone)

    #TODO remove
    # n=len(diphone)
    #preprocessed_diphone=ttslib.smooth_wav(preprocessed_diphone,position=31,sigma=2,desired_radius=28)
    #preprocessed_diphone=ttslib.smooth_wav(preprocessed_diphone,position=n-31,sigma=2,desired_radius=28)

    # TODO remove
    # f, axarr = plt.subplots(2, sharex=True)
    # axarr[0].plot(diphone)
    # axarr[0].set_title('%s original' % name )
    # diphone[diphone>1]=1
    # axarr[1].plot(diphone)
    # axarr[1].set_title('%s preprocessed' % name )
    # plt.show()

    return diphone

# reads a library of diphones from diphones_path
# returns a dict where the key is the name of the diphone and the value is the
# audio signal float32 encoded in a numpy array
def read_diphones(diphones_path):
    diphones_wavs_lib={}
    for file in os.listdir(diphones_path):
        if file.endswith(".wav"):
            wav = utility.read_wav(os.path.join(diphones_path,file))
            name=os.path.splitext(file)[0]
            wav=preprocess_diphone(name,wav)
            diphones_wavs_lib[name]=wav
    return diphones_wavs_lib
