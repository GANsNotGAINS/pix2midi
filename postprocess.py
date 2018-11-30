import numpy as np 
import matplotlib.pyplot as plt 

class Processer():
	def __init__(self, input_file, output_dir, output_prefix, resolution=5):
		self.image = plt.imread(input_file)
		# ignore g channel
		self.image[:, :, 1] = 0

		self.output_dir = output_dir
		if not self.output_dir.endswith("/"):
			self.output_dir += "/"

		self.output_prefix = output_prefix
		self.minNote = 60
		self.lengths = [1 / (2 ** i) for i in range(resolution)]
		self.defaultHeight = 24
		self.defaultWidth = 24

	def buildImages(self):
		rows, cols, z = self.image.shape 

		# assume image is in tiles
		for i in range(rows // self.defaultHeight):
			for j in range(cols // self.defaultWidth):
				start_r = i * self.defaultHeight
				start_c = j * self.defaultWidth

				processed = np.zeros((self.defaultHeight, self.defaultWidth, 3))

				chunk = self.image[start_r: start_r + self.defaultHeight, start_c: start_c + self.defaultWidth]
				summed = np.sum(chunk, axis=2)

				for col in range(self.defaultWidth):
					column = chunk[:, col]
					idx = np.argmax(summed[:, col]) # get the "brightest" pixel in the column, idk if this is great lol
					pixel = column[idx]
					
					new_pixel = [0, 0, 0]
					new_pixel[np.argmax(pixel[:3])] = np.max(pixel[:3]) * pixel[3] # pick between red or blue and multiply by alpha

					processed[idx, col] = new_pixel 

				fname = "{0}{1}{2}-{3}.png".format(self.output_dir, self.output_prefix, i, j)
				plt.imsave(fname, processed) 


if __name__ == "__main__":
	p = Processer("img.png", "output/", "output")
	p.buildImages()



