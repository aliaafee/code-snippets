import math
from PIL import Image, ImageDraw
from random import random

class Twig:
	def __init__(self, start, end, angle, childCount, color, depth):
		self.start = start
		self.end = end
		self.angle = angle
		self.childCount = childCount
		self.color = color
		self.depth = int(depth) - 1
		self.children = []
		if self.depth > 0:
			self.addChildren()

	def rotate(self, vec, a):
		x, y = vec
		x1 = x * math.cos(a) - y * math.sin(a)
		y1 = x * math.sin(a) + y * math.cos(a)
		return (x1 , y1)

	def sub(self, vec1, vec2):
		return (vec1[0] - vec2[0], vec1[1] - vec2[1])

	def add(self, vec1, vec2):
		return (vec1[0] + vec2[0], vec1[1] + vec2[1])

	def mul(sel, vec, fact):
		return (vec[0] * fact, vec[1] * fact)

	def draw(self, imageDraw):
		length = self.sub(self.end, self.start)
		length = math.sqrt(length[0]*length[0] + length[1] * length[1])
		width = int(length/100.0 * 20.0)
		draw.line((self.start[0], self.start[1], self.end[0], self.end[1]), fill=self.color, width=width)
		for child in self.children:
			child.draw(imageDraw)

	def addChildren(self):
		lengthDecayRange = (0.7, 0.8)
		angleDecayRange = (1.0, 1.1)

		angleFuzz = 0.3
		childCountFuzz = 1.0

		lengthDecay = lengthDecayRange[0] + (lengthDecayRange[1] - lengthDecayRange[0]) * random()
		angleDecay = angleDecayRange[0] + (angleDecayRange[1] - angleDecayRange[0]) * random()

		dir = self.sub(self.end, self.start)
		dir = self.mul(dir, lengthDecay)
		astart = -1 * (self.angle / 2.0)
		aend = self.angle / 2.0
		for i in range(0, self.childCount):
			ang = astart + ((aend - astart) * float(i)/float(self.childCount-1))
			ang += (1.0 - (random() * 2.0)) * self.angle * angleFuzz
			ndir = self.rotate(dir, ang)
			end = self.add(self.end, ndir)
			self.children.append(
				Twig(
					start = self.end, 
					end = end, 
					angle = self.angle * angleDecay, 
					childCount = self.childCount, 
					color = self.color,
					depth = self.depth
				)
			)


im = Image.new('RGBA', (1280, 800), (255, 255, 255, 0))
draw = ImageDraw.Draw(im)

for d in range(0,255,5):
	color = 255 - d
	pos = 1280.0 * random()
	height = 200.0 - (140.0 * random())
	tree = Twig(
		start=(pos,800.0), 
		end=(pos,800.0-height), 
		angle=0.7, 
		childCount=2,
		color=(color,color,color),
		depth=10
	)

	tree.draw(draw)

im.show()
