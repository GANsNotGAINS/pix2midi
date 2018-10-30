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
        s = music21.stream.Stream()

        # get all the indices of nonzero pixels
        # transpose is a lil easier to work with
        indices = np.argwhere(self.image.sum(axis=2).T)
        
        for col, row in indices:
            pixel = self.image[row][col]

            if pixel[2] > 0:
                scaled = pixel[2]
                note_val = row + self.minNote
                n = music21.note.Note(note_val)
            else:
                scaled = pixel[0]
                n = music21.note.Rest()
            
            duration = music21.duration.Duration(self.getNoteLength(scaled))
            n.duration = duration
            s.append(n)

        s.write("midi", output_filename)

    def getNoteLength(self, val):
        deltas = [abs(val/255 - length) for length in self.lengths]
        length = self.lengths[np.argmin(deltas)]
        return length * 4

if __name__ == "__main__":
    converter = PIX2MIDIConverter("song.png")
    converter.buildMidi("song.mid")