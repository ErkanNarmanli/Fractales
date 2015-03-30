#!/usr/bin/python
# -*-coding:utf-8 -*

from libfractales import *
from PIL import Image, ImageDraw, ImageFont
from math import sqrt
import time
import sys


def cree_julia(taille=600, c = 0, n_max = 200, alpha = 5, largeur = 4.2):
	# Déclaration de l'image
	image = Image.new('RGB', (taille, taille), (255, 255, 255))
	# Outil de dessin
	draw = ImageDraw.Draw(image)
	for k in range(taille):
		chargement(k, taille)
		for l in range(taille/2+1):
			u = ch_coord(k,l,taille, largeur, 0)
			n = 0
			while abs(u) <= 2 and n < n_max:
				u = u*u + c
				n = n + 1
			col = couleur_pix(n, n_max, alpha)
			draw.point((k, l), fill=col)
			draw.point((taille-k,taille-l), fill=col)
	print("\nImage générée")
	return(image)


