"""Helper functions for working with audio files in NumPy."""

import numpy as np
import soundfile as sf


def pcm2float(sig, dtype='float64'):
    """Convert PCM signal to floating point with a range from -1 to 1.

    Use dtype='float32' for single precision.

    Parameters
    ----------
    sig : array_like
        Input array, must have integral type.
    dtype : data type, optional
        Desired (floating point) data type.

    Returns
    -------
    numpy.ndarray
        Normalized floating point data.

    See Also
    --------
    float2pcm, dtype

    """
    sig = np.asarray(sig)
    if sig.dtype.kind not in 'iu':
        raise TypeError("'sig' must be an array of integers")
    dtype = np.dtype(dtype)
    if dtype.kind != 'f':
        raise TypeError("'dtype' must be a floating point type")

    i = np.iinfo(sig.dtype)
    abs_max = 2 ** (i.bits - 1)
    offset = i.min + abs_max
    return (sig.astype(dtype) - offset) / abs_max


def float2pcm(sig, dtype='int16'):
    """Convert floating point signal with a range from -1 to 1 to PCM.

    Any signal values outside the interval [-1.0, 1.0) are clipped.
    No dithering is used.

    Note that there are different possibilities for scaling floating
    point numbers to PCM numbers, this function implements just one of
    them.  For an overview of alternatives see
    http://blog.bjornroche.com/2009/12/int-float-int-its-jungle-out-there.html

    Parameters
    ----------
    sig : array_like
        Input array, must have floating point type.
    dtype : data type, optional
        Desired (integer) data type.

    Returns
    -------
    numpy.ndarray
        Integer data, scaled and clipped to the range of the given
        `dtype`.

    See Also
    --------
    pcm2float, dtype

    """
    sig = np.asarray(sig)
    if sig.dtype.kind != 'f':
        raise TypeError("'sig' must be a float array")
    dtype = np.dtype(dtype)
    if dtype.kind not in 'iu':
        raise TypeError("'dtype' must be an integer type")

    i = np.iinfo(dtype)
    abs_max = 2 ** (i.bits - 1)
    offset = i.min + abs_max
    return (sig * abs_max + offset).clip(i.min, i.max).astype(dtype)


def read_wav(filepath):
    f = sf.SoundFile(filepath)
    wav= f.read(filepath)
    assert f.samplerate == 16000
    assert f.channels == 1
    assert f.subtype == 'PCM_16'
    return wav

def write_wav(wav,filepath):
    sf.write(filepath, wav, 16000)

def read_wav2(filepath):
    w=wave.open(filepath)
    framerate = w.getframerate()
    frames = w.getnframes()
    channels = w.getnchannels()
    width = w.getsampwidth()
    assert channels == 1 #mono
    assert width == 2 #16bits
    assert framerate == 16000 #16khz

    #print("sampling rate:", framerate, "Hz, length:", frames, "samples,",
    #      "channels:", channels, "sample width:", width, "bytes")

    data = w.readframes(frames) # read all frames
    data = np.frombuffer(data, dtype='<i2').reshape(-1) # convert from string to int16
    w.close()
    return data

    #wav = utility.pcm2float(wav, 'float32') # convert from int16 to float32
    #print wav
    #wav = utility.float2pcm(wav, 'int16') # convert from float32 to int16
    #print wav


def to_bytes(n, length, endianess='big'):
    print n
    h = '%x' % n
    s = ('0'*(len(h) % 2) + h).zfill(length*2).decode('hex')
    return s if endianess == 'big' else s[::-1]

def write_wav2(wav,filepath):
    wav=list(wav)
    frames=len(wav)
    w = wave.open(filepath, 'w')
    w.setparams((1, 2, 16000, frames, 'NONE', 'not compressed')) #nchannels,width,sampling rate,  nframes, comptype, compname
    int16tobytes=lambda i: to_bytes(i,2)
    wav=map(int16tobytes,wav) # convert each amplitude to a tuple of bytes
    wav=list(itertools.chain(*wav)) # remove the tuples so that we are left with a list of bytes
    wav_str = ''.join(wav) # encode as chars and join in a single string (needed for wave.writeframes)
    w.writeframes(wav_str)
    w.close()
