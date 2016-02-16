#!/usr/bin/python
import sys
import os
import utility
import soundfile as sf
import numpy as np

# prints without a newline
def print2(a):
    sys.stdout.write(a)

# checks the argument count and the syntax of the input string to synthesize
def validate_arguments():
    argument_count=len(sys.argv)
    if ( argument_count != 3 ):
        sys.exit('Invalid number of arguments (%d)' % argument_count)
    input_string=sys.argv[1]
    output_filepath=sys.argv[2]

    if not validate_syntax(input_string):
        sys.exit('Invalid input string syntax.')
    return input_string,output_filepath

# validates the syntax of the input string to check it only contains
# Consonant-Vowel syllables
def validate_syntax(input_string):
    vowels=['a','A']
    consonants=['k','l','m','s','p']
    n=len(input_string)
    if n == 0:
        return False
    if n % 2 != 0:
        return False
    pairs= n / 2
    for i in xrange(pairs):
        consonant=input_string[2*i]
        vowel=input_string[2*i+1]
        if not (vowel in vowels) or  not(consonant in consonants):
            return False
    return True

# receives an input string with valid syntax
# returns the list of diphones the string represents
# as a list of strings
def tokenize(input_string):
    n=len(input_string)
    pairs= n / 2
    diphone_tuples=zip(input_string,input_string[1:])
    f = lambda (consonant,vowel): consonant+vowel
    diphones=map(f,diphone_tuples)
    diphones.insert(0,'-'+input_string[0])
    diphones.append(input_string[-1]+'-')
    return diphones

# concatenates two sound signals
def concat2_wav(wav1,wav2):
    output_wav=np.hstack([wav1,wav2])
    # TODO smooth the signal!
    return output_wav

# concatenate multiple wavs into a single one
# by repeatedly concatenating two wavs
def concat_wav(wavs): #fold over wavs with concat2_wav
    output_wav=concat2_wav(wavs[0],wavs[1])
    for i in xrange(2,len(wavs)):
        output_wav=concat2_wav(output_wav,wavs[i])
    return output_wav

# takes a list of diphones and outputs a wav file with the wavs of each
# diphone (taken from the diphones_path) concatenated
def synthesize(diphones_wavs_lib,diphones):
    diphone_wavs=map(lambda diphone: diphones_wavs_lib[diphone] ,diphones)
    return concat_wav(diphone_wavs)

# reads a library of diphones from diphones_path
# returns a dict where the key is the name of the diphone and the value is the
# audio signal float32 encoded in a numpy array
def read_diphones(diphones_path):
    diphones_wavs_lib={}
    for file in os.listdir(diphones_path):
        if file.endswith(".wav"):
            wav = utility.read_wav(os.path.join(diphones_path,file))
            name=os.path.splitext(file)[0]
            diphones_wavs_lib[name]=wav
    return diphones_wavs_lib

# synthesizes a string to speech. the string is received in sys.argv
def main():
    diphones_path="diphones_ger"
    print2("1) Loading diphones from folder %s... " % diphones_path)
    diphones_wavs_lib=read_diphones(diphones_path)
    print "done, %d diphones loaded." % len(diphones_wavs_lib)

    print2("2) Checking syntax... ")
    input_string,output_filepath=validate_arguments()
    print "done, syntax ok."

    print2("3) Obtaining diphones from: \"%s\"... " % input_string)
    diphones=tokenize(input_string)
    print "done, diphones to synthesize: %s." % str(diphones)

    print2("4) Synthesizing... ")
    output_wav=synthesize(diphones_wavs_lib,diphones)
    print "done."

    print2("5) Saving file %s..." % output_filepath)
    utility.write_wav(output_wav,output_filepath)
    print "done."



if __name__ == "__main__":
    main()



# -k, -l, -m, -s, -p
# k-, l-, m-, s-, p-
# ka, la, ma, sa, pa
# ak, al, am, as, ap
# kA, lA, mA, sA, pA
# Ak, Al, Am, As, Ap
# a-, A-, -a,-A
