#!/usr/bin/python
import sys
import os
import utility
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import diphone_lib as diphone_lib
import ttslib as ttslib

import pdb


# prints without a newline
def print2(a):
    sys.stdout.write(a)

# checks the argument count and the syntax of the input string to synthesize
def validate_arguments():
    argument_count=len(sys.argv)
    if ( argument_count != 3 ):
        sys.exit('\n ERROR: Invalid number of arguments (%d).\nUsage: pytts input_string output_file' % argument_count)
    input_string=sys.argv[1]
    output_filepath=sys.argv[2]

    if not validate_syntax(input_string):
        sys.exit('\n ERROR: Invalid input string syntax. Input must be of the form (CV)+ where C is a consonant taken from {m,l,s,p,k} and V a vowel taken from {a,A}.')
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





# synthesizes a string to speech. the string is received in sys.argv
def main():

    print2("1) Checking arguments and syntax... ")
    input_string,output_filepath=validate_arguments()
    print "done, syntax ok."

    diphones_path="diphones"
    print2("2) Loading diphones from folder %s... " % diphones_path)
    diphones_wavs_lib=diphone_lib.read_diphones(diphones_path)
    print "done, %d diphones loaded." % len(diphones_wavs_lib)

    print2("3) Obtaining diphones from: \"%s\"... " % input_string)
    diphones=tokenize(input_string)
    print "done, diphones to synthesize: %s." % str(diphones)

    print2("4) Synthesizing... ")
    output_wav=ttslib.synthesize(diphones_wavs_lib,diphones)
    print "done."

    print2("5) Saving file %s..." % output_filepath)
    utility.write_wav(output_wav,output_filepath)
    print "done."



if __name__ == "__main__":
    main()




#a-, A-,
# -k, -l, -m, -s, -p

# ka, la, ma, sa, pa
# ak, al, am, as, ap
# kA, lA, mA, sA, pA
# Ak, Al, Am, As, Ap

#-a,-A
#k-, l-, m-, s-, p-
