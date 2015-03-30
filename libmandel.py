#!/usr/bin/python
# -*-coding:utf-8 -*

from PIL import Image, ImageDraw, ImageFont
from cmath import *
from colorsys import *
from libfractales import *

# Fonction qui trace un ensemble de mandelbrot
def cree_mandelbrot(taille = 600, n_max = 200, centre = -0.7, largeur = 2.8, alpha = 5):
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
	print("\nImage Générée") # Retour à la ligne
	return(image)

# Fonction qui trace un ensemble de mandelbrot en couleur ! Et c'est moche :)
def cree_mandelbrot_couleur_moche(taille = 600, n_max = 200, centre = -0.7, largeur = 2.8, alpha = 5):
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
	print("\nImage Générée") # Retour à la ligne
	return(image)

# Fonction qui trace un ensemble de mandelbrot zoli
def cree_mandelbrot_zoli(taille = 600, n_max = 200, centre = -0.7, largeur = 2.8, alpha = 5):
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
				if n == n_max:
					col = (0,0,0)
				else:
					col = coloration_zoli(n, n_max, (163, 183, 205), (27, 45, 66))
			draw.point((k, l), fill=col)
			draw.point((k, taille-l), fill=col) # On utilise l'invariance par conjugaison
	print("\nImage Générée") # Retour à la ligne
	return(image)

