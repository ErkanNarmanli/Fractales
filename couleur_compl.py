#!/usr/bin/python
# -*-coding:utf-8 -*

from PIL import Image, ImageDraw, ImageFont
from cmath import *
from colorsys import *
from libfractales import *

#Constantes
taille = 800
largeur = 2.8
centre = 0


#Image
image = Image.new('RGB', (taille, taille), (255, 255, 255))
#Outil de dessin
draw = ImageDraw.Draw(image)

#Fonction de coloration d'un complexe
def couleur_complexe(z):
	teinte = phase(z)/(2*pi)
	lumino = max(0, (1-abs(z)/largeur))
	col = hls_to_rgb(teinte, 150, lumino)
	c_1 = int(col[0])
	c_2 = int(col[1])
	c_3 = int(col[2])
	return (c_1, c_2, c_3)


#Main : on parcours les complexes
for k in range(taille):
	chargement(k,taille)
	for l in range(taille):
		u = ch_coord(k,l, taille, largeur, centre)
		col = couleur_complexe(u)
		draw.point((k,l), fill = col)
print("")

#Affichage de l'image
image.show()
