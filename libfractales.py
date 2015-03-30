#!/usr/bin/python
# -*-coding:utf-8 -*-

import sys
from colorsys import *
from cmath import *

#Fonction de coloration d'un complexe
def couleur_complexe(z, largeur = 2.8):
	teinte = phase(z)/(2*pi)
	lumino = max(0, (1-abs(z)/largeur))
	col = hls_to_rgb(teinte, 150, lumino)
	c_1 = int(col[0])
	c_2 = int(col[1])
	c_3 = int(col[2])
	return (c_1, c_2, c_3)

# Fonction qui aligne du texte à droite dans un espace de t_max caractères
def ecrire(chaine, t_max):
	l = len(chaine)
	for m in range(t_max - l):
		sys.stdout.write(" ") 
	sys.stdout.write(chaine)

# Affiche une barre de chargement
def chargement(k, taille):
	pourc = 100*k/float(taille)
	pourv = 20*pourc/100. #pourvingt, parce que j'ai envie
	pourc = int(pourc) + 1
	pourv = int(pourv) + 1
	sys.stdout.write('\r')
	ecrire("{}% : ".format(pourc), 7)
	ecrire(str(k+1), len(str(taille)))
	sys.stdout.write('/{} pix'.format(taille))
	sys.stdout.write('   [')
	for m in range(pourv):
		sys.stdout.write(':')
	for m in range(20 - pourv):
		sys.stdout.write(' ')
	sys.stdout.write(']')
	sys.stdout.flush() # Rend l'affichage plus fluide

# Détermine les coordonnées dans le plan complexe
# à partir des coordonnées dans l'image
def ch_coord(k, l, taille, largeur, centre):
	return(complex( \
		(float(k) - taille/2.)*largeur/float(taille) + centre, \
		(float(l) - taille/2.)*largeur/float(taille) \
		))

# Détermine la couleur du pixel sur une echelle de gris en
# fonction du rang à partir duquel on sort du cercle de rayon 2
def couleur_pix(n, n_max, alpha = 5):
	if n == n_max:
		c = 0
	else:
		c = 20 + 235*((n_max - n)/float(n_max))**alpha
		c = int(c)
	return(c, c, c)

# Autre façon de colorier (toujours en noir en echelle de gris)
def couleur_pix_v2(n, n_max, n_min = 0, alpha = 5):
	if n == n_max:
		c = 0
	else:
		c = 20 + 235*((n_max - n)/float(n_max - n_min))**alpha
		c = int(c)
	return(c, c, c)
