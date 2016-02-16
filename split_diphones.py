import wave
import numpy as np
import utility
import soundfile as sf
import os



def split_wav(input_filepath,diphones,output_folderpath):
    wav=utility.read_wav(input_filepath)
    for (name,start,end) in diphones:
        diphone=wav[start:end]
        output_filename='%s.wav' % name
        output_filepath=os.path.join(output_folderpath,output_filename)
        utility.write_wav(diphone,output_filepath)

class DiphoneSource:
        def __init__(self,filepath,splits):
            self.splits=splits
            self.filepath=filepath

# TODO record diphones and annotate them
diphones= [ ('-a',20,2500),
            ('a-',2500,5000)
          ]
main_source=DiphoneSource('diphones_ger/ak.wav',diphones)

def main():
    output_folderpath='diphones'
    sources=[main_source]
    for source in sources:
        split_wav(source.filepath,source.splits,output_folderpath)


if __name__ == "__main__":
    main()
