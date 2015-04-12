#!/usr/bin/python
# -*-coding:utf-8 -*

"""
Fonctions dessinant des ensembles de Julia
"""

from libfractales import *
from PIL import Image, ImageDraw
from math import sqrt
from multiprocessing import Pool
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
	for k in xrange(taille):
		if verbose:
			chargement(k, taille)
		for l in xrange(taille/2):
			u = ch_coord(k, l, taille, largeur, 0)
			n = 0
			while abs(u) <= 2 and n < n_max:
				u = u*u + c
				n = n + 1
			col = couleur_pix(n, n_max, alpha)
			draw.point((k, l), fill = col)		
			draw.point((taille - 1 - k, taille - 1 - l), fill = col)
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
			draw.point((taille-k-1,taille-l-1), fill=col)
	if verbose:
		print("  Image générée")
		print("Temps d'exécution : {} s".format(time.time() - t))
	return(image)



# Ne fonctionne pas encore, et pas sûr que ce soit mieux ...
def cree_julia_mieux(taille = 600, c = 0, n_max = 200, alpha = 5, largeur= 4.2):
	""" Fonction améliorée pour calculer plus rapidement les Julia """
	t = time.time()
	
	# Matrice contenant dans chaque case le nombre d'itérations nécessaires
	# pour que la suite partant du complexe correspondant à [k, l] dépasse 2 en module
	matrice = np.ones((taille, taille)) # +1 car lorsqu'on utilise la symétrie, on est obligés de dépasser
	matrice = -matrice
	# Déclaration de l'image
	image = Image.new('RGB', (taille, taille), (255, 255, 255))
	# Outil de dessin
	draw = ImageDraw.Draw(image)
	
	for k in range(taille):
		chargement(k, taille)
		for l in range(taille/2 + 1):
			# On regarde si le pixel a déjà été traité
			if matrice[k, l] == -1:
				# Initialisations
				u = ch_coord(k, l, taille, largeur, 0)
				chemin = np.array(n_max)
				n = 0
				continuer = True
				# On calcule les termes de la suite, on sort de la boucle si :
				# - on tombe sur un terme déjà calculé
				# - n atteint n_max
				# - u dépasse 2 en module
				while continuer:
					u = u*u + c
					n = n + 1
					queue.append(u)
					i, j = inv_ch_coord(u, taille, largeur, 0)
					# Si on sort de la fenêtre, il faut poser n_mat = -1
					if (i < taille) and (j < taille) and (i >= 0) and (j >= 0):
						n_mat = matrice[i, j]
					else:
						n_mat = -1
					# On retombe sur un terme déjà calculé
					if n_mat >= 0:
						continuer = False
						for m in xrange(n):
							a, b = inv_ch_coord(queue[m], taille, largeur, 0)
							matrice[a, b] = min(n_max, n + n_mat - m)
							col = couleur_pix(min(n_max, n + n_mat - m), n_max, alpha)
							draw.point((a, b), fill = col)
							# On utilise l'invariance par rotation d'angle pi
							matrice[taille - 1 - a, taille - 1 - b] = min(n_max, n + n_mat - m)
							draw.point((taille - 1 - a, taille - 1 - b), fill = col)
					# On atteint n_max
					elif n == n_max:
						continuer = False
						matrice[k, l] = n_max
						col = couleur_pix(n_max, n_max, alpha)
						draw.point((k, l), fill = col)
						# On utilise l'invariance par rotation d'angle pi
						matrice[taille - 1 - k, taille - 1 - l] = n_max
						draw.point((taille - 1 - k, taille - 1 - l), fill = col)
					# le module de u dépasse 2
					elif abs(u) > 2:
						continuer = False
						for m in xrange(n):
							a, b = inv_ch_coord(queue[m], taille, largeur, 0)
							matrice[a, b] = n - m
							col = couleur_pix(n-m, n_max, alpha)
							draw.point((a, b), fill = col)
							# On utilise l'invariance par rotation d'angle pi
							matrice[taille - 1 - a, taille - 1 - b] = n - m
							draw.point((taille - 1 - a, taille - 1 - b), fill = col)
					# Si on ne remplit aucune des conditions précédentes,
					# on refait un tour de boucle
	print("    Image générée")
	print("Temps d'exécution : {} s".format(time.time() - t))
	return(image)






