#!/usr/bin/python
# -*-coding:utf-8 -*

from PIL import Image, ImageDraw, ImageFont
from cmath import *
from colorsys import *
from libfractales import *

def cree_mandelbrot(taille = 600, n_max = 200, centre = -0.7, largeur = 2.8, alpha = 5):
	"""Trace un ensemble de Mandelbrot
	taille 	: l'image est au format taille*taille
	n_max 	: entier jusqu'auquel on calcul la sortie du cercle
	largeur	: largeur que représente taille dans le plan complexe
	centre 	: centre de l'image dans le plan complexe
	alpha	: exposant d'écrasement pour le dégradé de couleur"""
	# Déclaration de l'image
	image = Image.new('RGB', (taille, taille), (255, 255, 255))
	# Outil de dessin
	draw = ImageDraw.Draw(image)
	for k in range(taille):
		chargement(k, taille)
		for l in range(taille/2+1):
			u = complex(0,0)
			c = ch_coord(k, l, taille, largeur, centre)
			n = 0
			# Si on est dans la cardioïde, on ne fait pas les tests
			if 2*abs(c-0.25) < (1 - cos(phase(c-0.25))).real:
				col = (0,0,0)
			else:
				while abs(u) <= 2 and n < n_max:
					u = u*u + c
					n = n + 1
				col = couleur_pix(n, n_max, alpha = alpha)
			draw.point((k, l), fill=col)
			draw.point((k, taille-l), fill=col) # On utilise l'invariance par conjugaison
	print("  Image Générée") # Retour à la ligne
	return(image)

def cree_mandelbrot_couleur_moche(taille = 600, n_max = 200, centre = -0.7, largeur = 2.8, alpha = 5):
	"""Trace ensemble de mandelbrot avec tout plein de couleur
	C'est moche"""
	# Déclaration de l'image
	image = Image.new('RGB', git(taille, taille), (255, 255, 255))
	# Outil de dessin
	draw = ImageDraw.Draw(image)
	for k in range(taille):
		chargement(k, taille)
		for l in range(taille/2+1):
			u = complex(0,0)
			c = ch_coord(k, l, taille, largeur, centre)
			n = 0
			# Si on est dans la cardioïde, on ne fait pas les tests
			if 2*abs(c-0.25) < (1 - cos(phase(c-0.25))).real:
				while n < n_max:
					u = u*u + c
					n = n + 1
				col = couleur_complexe(u, largeur = largeur)
			else:
				while abs(u) <= 2 and n < n_max:
					u = u*u + c
					n = n + 1
				col = couleur_complexe(u)
			draw.point((k, l), fill=col)
			draw.point((k, taille-l), fill=col) # On utilise l'invariance par conjugaison
	print("  Image Générée") # Retour à la ligne
	return(image)

def cree_mandelbrot_zoli(taille = 600, n_max = 200, centre = -0.7, largeur = 2.8, alpha = 5, couleur_fond = (27, 45, 66), couleur_bord = (163, 183, 205), couleur_mandel = (0,0,0)):
	"""Trace un ensemble de Mandelbrot avec un dégradé
	C'est zoli :)"""
	# Déclaration de l'image
	image = Image.new('RGB', (taille, taille), (255, 255, 255))
	# Outil de dessin
	draw = ImageDraw.Draw(image)
	for k in range(taille):
		chargement(k, taille)
		for l in range(taille/2+1):
			u = complex(0,0)
			c = ch_coord(k, l, taille, largeur, centre)
			n = 0
			# Si on est dans la cardioïde, on ne fait pas les tests
			if 2*abs(c-0.25) < (1 - cos(phase(c-0.25))).real:
				col = couleur_mandel
			else:
				while abs(u) <= 2 and n < n_max:
					u = u*u + c
					n = n + 1
				if n == n_max:
					col = couleur_mandel
				else:
					col = coloration_zoli(n, n_max, couleur_bord, couleur_fond)
			draw.point((k, l), fill=col)
			draw.point((k, taille-l), fill=col) # On utilise l'invariance par conjugaison
	print("  Image Générée") # Retour à la ligne
	return(image)

