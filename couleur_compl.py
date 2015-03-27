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


#Determine les cooerdonées dans le plan complexe
#à partir des coordonnées dans l'image
def ch_coord(k, l):
	return(complex( \
		(float(k) - taille/2.)*largeur/float(taille) + centre, \
		(float(l) - taille/2.)*largeur/float(taille) \
		))

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
		u = ch_coord(k,l)
		col = couleur_complexe(u)
		draw.point((k,l), fill = col)
print("\n")

#Affichage de l'image
image.show()
