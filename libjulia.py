#!/usr/bin/python
# -*-coding:utf-8 -*

from libfractales import *
from PIL import Image, ImageDraw
from math import sqrt
import numpy as np
import time
import sys


def cree_julia(taille=600, c = 0, n_max = 200, alpha = 5, largeur = 4.2, verbose = True):
	""" Dessine et renvoit un ensemble de Julia de taille x taille pixels
	L'option verbose sert à indiquer si on veut afficher les informations et la barre
	de chargement lors de l'exécution """
	t = time.time()
	# Déclaration de l'image
	image = Image.new('RGB', (taille, taille), (255, 255, 255))
	# Outil de dessin
	draw = ImageDraw.Draw(image)
	for k in range(taille):
		if verbose:
			chargement(k, taille)
		for l in range(taille/2+1):
			u = ch_coord(k,l,taille, largeur, 0)
			n = 0
			while abs(u) <= 2 and n < n_max:
				u = u*u + c
				n = n + 1
			col = couleur_pix(n, n_max, alpha)
			draw.point((k, l), fill=col)
			draw.point((taille-k-1,taille-l), fill=col)
	if verbose:
		print("  Image générée")
		print("Temps d'exécution : {} s".format(time.time() - t))
	return(image)

def cree_julia_zoli(taille=600, c = 0, n_max = 200, largeur = 4.2, couleur_fond = (27, 45, 66), couleur_bord = (163, 183, 205), couleur_julia = (0, 0, 0), verbose = True):
	""" Fait la même chose que cree_julia avec plus de coloration
	C'est zoli quoi """
	t = time.time()
	# Déclaration de l'image
	image = Image.new('RGB', (taille, taille), (255, 255, 255))
	# Outil de dessin
	draw = ImageDraw.Draw(image)
	for k in range(taille):
		if verbose:
			chargement(k, taille)
		for l in range(taille/2+1):
			u = ch_coord(k,l,taille, largeur, 0)
			n = 0
			while abs(u) <= 2 and n < n_max:
				u = u*u + c
				n = n + 1
			if n == n_max:
				col = couleur_julia
			else:
				col = coloration_zoli(n, n_max, couleur_bord, couleur_fond)
			draw.point((k, l), fill=col)
			draw.point((taille-k-1,taille-l), fill=col)
	if verbose:
		print("  Image générée")
		print("Temps d'exécution : {} s".format(time.time() - t))
	return(image)



# Ne fonctionne pas encore, et pas sûr que ce soit mieux ...
def cree_julia_mieux(taille = 600, c = 0, n_max = 200, lg_queue = 10, alpha = 5, largeur= 4.2):
	""" Fonction améliorée pour calculer plus rapidement les Julia """
	t = time.time()
	# Matrice contenant dans chaque case le nombre d'itérations nécessaires
	# pour que la suite partant du complexe correspondant à [k, l] dépasse 2 en module
	matrice = np.ones((taille, taille))
	matrice = (-1)*matrice
	for k in range(taille):
		chargement(k, taille)
		for l in range(taille):
			# On regarde si le pixel a déjà été traité
			if matrice[k, l] == -1:
				# Initialisation
				v = ch_coord(k, l, taille, largeur, 0)
				u = v
				n = 0
				continuer = True
				# On calcule les termes de la suite, on sort de la boucle si :
				# - on tombe sur un terme déjà calculé
				# - n attient n_max
				# - u dépasse 2 en module
				while continuer:
					u = u*u + c
					n = n + 1
					# On retombe sur un terme déjà calculé
					i, j = inv_ch_coord(u, taille, largeur, 0)
					# Si on sort de la fenêtre, il faut poser k = 0
					if (i < taille) and (j < taille) and (i >= 0) and (j >= 0):
						k = matrice[i, j]
					else:
						k = 0
					if k != -1:
						continuer = False
						for m in range(n):
							a, b = inv_ch_coord(v, taille, largeur, 0)
							matrice[a, b] = min(n_max, n + k - m)
							v = v*v + c
					# On atteint n_max
					elif n == n_max:
						continuer = False
						matrice[k, l] = n_max
					# le module de u dépasse 2
					elif abs(u) > 2:
						continuer = False
						for m in range(n):
							a, b = inv_ch_coord(v, taille, largeur, 0)
							matrice[a, b] = n - m
							v = v*v + c
					# Si on ne remplit aucune des conditions précédentes,
					# on refait un tour de boucle
	# On a rempli la matrice, il ne reste qu'à colorier l'image
	print("\nGénération de l'image")
	print(matrice)
	# Déclaration de l'image
	image = Image.new('RGB', (taille, taille), (255, 255, 255))
	# Outil de dessin
	draw = ImageDraw.Draw(image)
	for k in range(taille):
		for l in range(taille):
			col = couleur_pix(matrice[k, l], n_max, alpha)
			draw.point((k, l), fill = col)
			# On utilise l'invariance par rotation d'angle pi
			draw.point((taille - k, taille - l), fill = col)
	print("Image générée")
	print("Temps d'exécution : {} s".format(time.time() - t))
	return(image)



