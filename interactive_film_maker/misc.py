#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Fonctions/Variables utiles un peu partout
"""

# Pour dire à python d'importer aussi depuis le répertoire parent
import sys
sys.path.append('../')

from libfractales import ch_coord, inv_ch_coord

##### Variables globales
taille_image = 750			# Taille du mandelbrot
taille_miniature = 180			# Taille des ensembles de Julia
mandel_largeur = 2.8			# Correspond aux options par défaut de cree_mandel
mandel_centre = complex(-0.7, 0)	# idem, normalement on ne touche pas
fichier_image = 'fond_film_maker_{}px.png'.format(taille_image)

##### Fonctions utiles
# Changements de coordonnées
def get_coord(k, l):
	""" Récupère les coordonnées dans le plan complexe d'un événement sur l'image """
	c = ch_coord(k, l, taille_image, mandel_largeur, mandel_centre)
	x = c.real
	y = -c.imag	# tkinter oriente l'axe des ordonnées à l'envers
	return(x, y)

def inv_get_coord(x, y):
	""" Fonction inverse : rend le pixel correspondant aux coordonnées (x, y) """
	k, l = inv_ch_coord(complex(x, -y), taille_image, mandel_largeur, mandel_centre)
	return(k, l)

# Formatage d'un complexe pour l'affichage
def complex_format(c):
	""" Formate le complexe c pour l'affichage """
	string = ''
	if c.real >= 0:
		string += ' '
	string += '{0:.4f}'.format(c.real)
	if c.imag < 0:
		string += ' -{0:.4f}i'.format(c.imag)
	else:
		string += ' +{0:.4f}i'.format(c.imag)
	return(string)

# Formatage d'un couple de point pour l'affichage dans SegItem
def seg_format(pt1, pt2):
	""" Formate le couple de points (pt1, pt2) qui représente une segment
	pour l'affichage """
	# 5 digits partout
	string = ''
	string += complex_format(pt1)
	string += '  ;  '
	string += complex_format(pt2)
	return(string)


