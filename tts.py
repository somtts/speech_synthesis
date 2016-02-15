#!/usr/bin/python
import sys
import os







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
    diphones.insert(0,input_string[0])
    diphones.append(input_string[-1])
    return diphones

# concatenates two wav files into another
def concat2_wav(wav_filepath1,wav_filepath2,output_filepath):
    pid=os.getpid()
    #print 'sox %s -r 44100  /tmp/%d-1.raw' % (wav_filepath1,pid)
    options = "-r 16000 -b 16 -c 1 -e signed"
    options_input=options
    temp1="/tmp/%d-1.raw" % pid
    temp2="/tmp/%d-2.raw" % pid
    temp_output="/tmp/%d_.raw" % pid
    os.system('sox %s %s %s' % (wav_filepath1,options_input,temp1))
    os.system('sox %s %s %s' % (wav_filepath2,options_input,temp2))
    os.system('cat %s %s > %s' % (temp1,temp2,temp_output))
    os.system('sox %s %s %s %s' % (options,temp_output,options,output_filepath))
    os.system('rm %s' % temp_output)

# concatenate multiple wavs into a single one
# by repeatedly concatenating two wavs
# list of wavs must contain at least two files
def concat_wav(wav_filepaths,output_filepath):
    concat2_wav(wav_filepaths[0],wav_filepaths[1],output_filepath)
    for i in xrange(2,len(wav_filepaths)):
        concat2_wav(output_filepath,wav_filepaths[i],output_filepath)

# takes a list of diphones and outputs a wav file with the wavs of each
# diphone (taken from the diphones_path) concatenated
def synthesize(diphones_path,diphones,output_filepath):
    diphone_filenames=map(lambda diphone:  diphone+".wav",diphones)
    diphone_filepaths=map(lambda filename: os.path.join(diphones_path,filename),diphone_filenames)
    concat_wav(diphone_filepaths,output_filepath)

# synthesizes a string to speech. the string is received in sys.argv
def main():
    diphones_path="diphones"

    input_string,output_filepath=validate_arguments()
    print "Synthesizing wav for input: %s" % input_string
    diphones=tokenize(input_string)
    print "Synthesizing diphones: %s" % str(diphones)
    print "..."
    synthesize(diphones_path,diphones,output_filepath)
    print "Synthesis complete."



if __name__ == "__main__":
    main()



# -k, -l, -m, -s, -p
# ka, la, ma, sa, pa
# ak, al, am, as, ap
# kA, lA, mA, sA, pA
# Ak, Al, Am, As, Ap
# a-, A-
