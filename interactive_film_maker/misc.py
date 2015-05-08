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
# Taille du mandelbrot
taille_image = 750
# Taille des ensembles de Julia
taille_miniature = 180
# Mettre cette contante à False pour masquer les barres de chargement lors de
# la génération des images
verbose = False
# Constantes utilisées pour la génération des images
# Ne pas toucher
mandel_largeur = 2.8
mandel_centre = complex(-0.7, 0)	
# Fichier contenant l'image du Mandelbrot
fichier_image = 'fond_film_maker_{}px.png'.format(taille_image)
# Couleur des frames contenant les infos sur les segments
DEFAULT_SEG_COLOR = '#f0f0f0'
# Couleur desdits frames lorsqu'ils sont séléctionnés
EMPH_SEG_COLOR = '#ffd0d0'

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


