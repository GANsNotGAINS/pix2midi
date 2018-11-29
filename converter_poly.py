import music21
import argparse
import numpy as np
import matplotlib.pyplot as plt

class PIX2MIDIConverter():
    def __init__(self, input_file, resolution=5):
        self.image = plt.imread(input_file)
        self.image = self.image * 255
        self.image = self.image.astype(int)
        self.minNote = 60
        self.lengths = [1 / (2**i) for i in range(resolution)]


    def buildMidi(self, output_filename):
        mainStream = music21.stream.Stream()
        for i in range(1, 25):
            s = music21.stream.Stream()

            # get all the indices of nonzero pixels
            # transpose is a lil easier to work with
            # indices = np.argwhere(self.image.sum(axis=2).T)
            j = 0
            while j < self.image.shape[1]:
                pixel = self.image[i][j]
                if pixel[0] == 255:
                    duration = .25
                    start = j
                    while pixel[0] == 255 and pixel[1] == 255:
                        duration += .25
                        j += 1
                        pixel = self.image[i][j]
                        print('hi', j)
                    note_val = i + self.minNote
                    n = music21.note.Note(note_val)
                    n.duration = music21.duration.Duration(duration)
                    s.insert(start*.25,n)
                    j += 1
                else:
                    j += 1
                
            print(i)
            mainStream.insert(0, s)
        mainStream.show('text')
        mainStream.write("midi", output_filename)
        
        
        

    def getNoteLength(self, val):
        deltas = [abs(val/255 - length) for length in self.lengths]
        length = self.lengths[np.argmin(deltas)]
        return length * 4

if __name__ == "__main__":
    converter = PIX2MIDIConverter("song.png")
    converter.buildMidi("song.mid")