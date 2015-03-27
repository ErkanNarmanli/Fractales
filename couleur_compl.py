#!/usr/bin/python
# -*-coding:utf-8 -*

from PIL import Image, ImageDraw, ImageFront
import sys
from cmath import *
from colorsys import *

#Constante
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
	lumino = abs(z)

#Main : on parcours les complexes
for k in range(taille):
	for l in range(taille):
		u = ch_coord(k,l)
		col = couleur_complexe(u)
		draw.point((k,l), fill = col)
#Affichage de l'image
image.show()
