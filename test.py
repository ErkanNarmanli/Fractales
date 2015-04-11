#!/usr/bin/python
# -*-coding:utf-8 -*

from PIL import Image, ImageDraw

image = Image.new('RGB', (600,600), (255,0,0))
draw = ImageDraw.Draw(image)

for k in range(600):
	for l in range(600):
		draw.point((k,l), fill = (0,0,0))

image.show()
