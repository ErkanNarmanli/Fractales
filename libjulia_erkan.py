#!/usr/bin/python
# -*-coding:utf-8 -*

from libfractales import *
from PIL import Image, ImageDraw
from math import sqrt
import time
import sys
import numpy as np

def cree_julia_erkan(taille = 600, n_max = 200, alpha = 5, largeur = 4.2):
	# On regarde le temps initial
	t = time.time()
	# On déclare l'image
	image = Image.new('RGB', (taille, taille), (255,255,255))
	# Outil de dessin
	draw = ImageDraw.Draw(image)
	# On déclare notre matrice
	matrice = np.ones((taille, taille))
	matrice = (-1)*matrice
	# Et puis c'est parti ! :)
	for k in range(taille):
		for l in range(taille/2+1):
			if (matrice[k,l] != -1):
				continue
			u = ch_chord(k,l,taille,largeur,0)
			n = 0
			chemin = np.ones(
			# On initialise le booléen de sortie
			sortie = 0
			while sortie == 0:
				
