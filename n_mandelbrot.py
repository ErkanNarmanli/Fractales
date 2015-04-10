#!/usr/bin/python
# -*-coding:utf-8 -*

"""
Dessine une généralisation de l'ensemble de Mandelbrot
"""

from libfractales import *
from PIL import Image, ImageDraw, ImageFont
import sys
from cmath import *


# Constantes
centre = 0 	# -0.7
try:
	taille = int(sys.argv[1])
except:
	taille = 600 	# 700
try:
	puis_r = float(sys.argv[2])
except:
	puis_r = 3 
try:
	puis_i = float(sys.argv[3])
except:
	puis_i = 0

puis = complex(puis_r,puis_i)
largeur = 4	# 2.8
n_max = 50	# 200
alpha = 5	# 5
# Image
image = Image.new('RGB', (taille, taille), (255, 255, 255))
# Outil de dessin
draw = ImageDraw.Draw(image)


# Parcours
for k in range(taille):
	chargement(k, taille)
	for l in range(taille):
		u = complex(0,0)
		c = ch_coord(k, l, taille, largeur, 0)
		n = 0
		while abs(u) <= 2 and n < n_max:
			if u != 0:
				u = u**puis + c
			else:
				u = c
			n = n + 1
		col = couleur_pix(n, n_max, alpha)
		draw.point((k, l), fill=col)
sys.stdout.write("\n")

# Affichage et sauvegarde de l'image
image.show()
image.save('Images/mandelbrot_{}_{}px.png'.format(puis,taille))

