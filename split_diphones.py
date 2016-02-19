import wave
import numpy as np
import utility
import soundfile as sf
import os



def split_wav(input_filepath,diphones,output_folderpath):
    wav=utility.read_wav(input_filepath)
    for (name,start_ms,end_ms) in diphones:
        start=start_ms*16 # 16000
        end=end_ms*16
        diphone=wav[start:end]
        output_filename='%s.wav' % name
        output_filepath=os.path.join(output_folderpath,output_filename)
        utility.write_wav(diphone,output_filepath)

class DiphoneSource:
        def __init__(self,filepath,splits):
            self.splits=splits # tuples of the form (diphone_name,start_ms,end_ms)
            self.filepath=filepath


input_folderpath='diphone_words/'

sources={}

make_ds=lambda name,splits: DiphoneSource(os.path.join(input_folderpath,name+'.wav'),splits)
make_ds_and_add=lambda name,splits: sources.__setitem__(name,make_ds(name,splits))

# Source wav files from which to extract diphones
make_ds_and_add('mamA',  [('A-',1202,1704)])
make_ds_and_add('kamAla',[('a-',616,774)])
make_ds_and_add('kamAla',[('-k',0,126),('ka',120,258),('am',258,369),('mA',369,461),('Al',461,616)])
make_ds_and_add('malApa',[('-m',30,125),('ma',125,250),('al',250,370),('lA',370,515),('Ap',515,800)])
make_ds_and_add('lapAsa',[('-l',122,287),('la',231,334),('ap',343,470),('pA',470,627),('As',627,761)])
make_ds_and_add('pasAka',[('-p',30,110),('pa',110,250),('as',250,392),('sA',392,535),('Ak',535,683)])
make_ds_and_add('sakAma',[('-s',177,368),('sa',365,450),('ak',450,580),('kA',580,770),('Am',770,900)])


def main():
    output_folderpath='diphones'
    print "Generating diphones in folder \"%s\"..." % output_folderpath
    for source in sources.values():
        split_wav(source.filepath,source.splits,output_folderpath)
    print "Done"


if __name__ == "__main__":
    main()
