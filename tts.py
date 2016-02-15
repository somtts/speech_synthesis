#!/usr/bin/python
import sys
import os
# input: mamAsalAlapApa
# outpute: -m,ma,am,Ma,As,sa,

vowels=['a','A']
consonants=['k','l','m','s','p',]

diphones_path="diphones"

def validate_arguments():
    argument_count=len(sys.argv)
    if ( argument_count != 3 ):
        sys.exit('Invalid number of arguments (%d)' % argument_count)
    input_string=sys.argv[1]
    output_filepath=sys.argv[2]

    if not validate_syntax(input_string):
        sys.exit('Invalid input string syntax.')
    return input_string,output_filepath

def validate_syntax(input_string):
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

def tokenize(input_string):
    n=len(input_string)
    pairs= n / 2
    diphone_tuples=zip(input_string,input_string[1:])
    f = lambda (consonant,vowel): consonant+vowel
    diphones=map(f,diphone_tuples)
    diphones.insert(0,input_string[0])
    diphones.append(input_string[-1])
    return diphones

def concat2_wav(wav_filepath1,wav_filepath2,output_filepath):
    pid=os.getpid()
    #print 'sox %s -r 44100  /tmp/%d-1.raw' % (wav_filepath1,pid)
    os.system('sox %s -r 44100  /tmp/%d-1.raw' % (wav_filepath1,pid))
    os.system('sox %s -r 44100 /tmp/%d-2.raw' % (wav_filepath2,pid))
    os.system('cat /tmp/%d-1.raw /tmp/%d-2.raw > /tmp/%d.raw' % (pid,pid,pid))
    os.system('sox -r 44100 -e signed-integer -b 16 -c 1 /tmp/%d.raw %s' % (pid,output_filepath))
    os.system('rm /tmp/%d*.raw' % pid)

def concat_wav(diphone_filepaths,output_filepath):
    concat2_wav(diphone_filepaths[0],diphone_filepaths[1],output_filepath)
    for i in xrange(2,len(diphone_filepaths)):
        concat2_wav(output_filepath,diphone_filepaths[i],output_filepath)


def synthesize(diphones,output_filepath):
    diphone_filenames=map(lambda diphone:  diphone+".wav",diphones)
    diphone_filepaths=map(lambda filename: os.path.join(diphones_path,filename),diphone_filenames)
    concat_wav(diphone_filepaths,output_filepath)

def main():
    input_string,output_filepath=validate_arguments()
    print "Synthesizing wav for input: %s" % input_string
    diphones=tokenize(input_string)
    print "Synthesizing diphones: %s" % str(diphones)
    print "..."
    synthesize(diphones,output_filepath)
    print "Synthesis complete."



if __name__ == "__main__":
    main()


# #!/bin/sh
# sox $1 -r 44100 -c 2 -s -w /tmp/$$-1.raw
# sox $2 -r 44100 -c 2 -s -w /tmp/$$-2.raw
# cat /tmp/$$-1.raw /tmp/$$-2.raw > /tmp/$$.raw
# sox -r 44100 -c 2 -s -w /tmp/$$.raw $3
# rm /tmp/$$*.raw
