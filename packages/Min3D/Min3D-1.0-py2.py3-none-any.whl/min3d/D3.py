from shutil import get_terminal_size as gtz

class graph():
	def __init__(self, gradient='@$8W9H4Z1l(r/:. ', console_size=None, lenght=16):
		if(console_size == None):
			w, h = gtz()
			self.width = w
			self.height = h
			self.lenght = lenght
		self.gradient = gradient
		self.gradientSize = len(self.gradient)
		self.MAP = {}
		for x in range(w):
			for y in range(h):
				self.MAP[(x, y)] = [0 for _ in range(lenght)]
		self.screen = [' ' for _ in range(w*h)]
	def remap(self, x, in_min, in_max, out_min, out_max):
		return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
	def __str__(self):
		for x in range(self.width):
			for y in range(self.height):
				if(self.MAP[(x, y)] == [0 for _ in range(self.lenght)]):
					pixel = self.gradient[-1]
				else:
					i = 0
					for p in self.MAP[(x, y)]:
						if(p != 0):
							pixel = self.gradient[int(self.remap(p, 0, self.lenght, 0, self.gradientSize))]
							break
						i += 1
				self.screen[x+y*self.width] = pixel
		return ''.join(x for x in self.screen)
	def putsquere(self, cordfrom, cordto, range_):
		if(range_ > self.lenght) or (range_ < 0):
			raise TypeError('RANGE NOT > LENGHT AND RANGE NOT < 0')
		if(not cordfrom in self.MAP) or (not cordto in self.MAP):
			raise TypeError('PIXEL NOT FOUND')
		for x in range(cordfrom[0], cordto[0]):
			for y in range(cordfrom[1], cordto[1]):
				lst = []
				for i in range(self.lenght):
					if(i+1 == range_):
						lst.append(range_)
					else:
						lst.append(0)
				self.MAP[(x, y)] = lst
	def clear(self):
		for x in range(w):
			for y in range(h):
				self.MAP[(x, y)] = [0 for _ in range(lenght)]
	def putpixel(self, xy, range_):
		if(range_ > self.lenght) or (range_ < 0):
			raise TypeError('RANGE NOT > LENGHT AND RANGE NOT < 0')
		if(not xy in self.MAP):
			raise TypeError('PIXEL NOT FOUND')
		lst = []
		for i in range(self.lenght):
			if(i+1 == range_):
				lst.append(range_)
			else:
				lst.append(0)
		self.MAP[(xy[0], xy[0])] = lst
