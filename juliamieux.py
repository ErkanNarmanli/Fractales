#!/usr/bin/python
# -*- encoding:utf-8 -*-

from libfractales import *
from PIL import Image, ImageDraw, ImageFont
import time
import sys
import numpy as np

def cree_julia_mieux(taille = 600, c = 0, n_max = 200, lg_queue = 10, alpha = 5, largeur= 4.2):
	""" Fonction améliorée pour calculer plus rapidement les Julia 
	Attention : lg_queue doit être inférieur à n_max """
	# Matrice contenant dans chaque case le nombre d'itérations nécessaires
	# pour que la suite partant du complexe correspondant à [k, l] dépasse 2
	matrice = np.zeros((taille, taille))
	for k in range(taille):
		chargement(k, taille)
		for l in range(taille):
			if matrice[k, l] == 0:
				# On garde en mémoire les lg_queue premiers termes
				queue = np.zeros(lg_queue)
				u = ch_coord(k, l, taille, largeur, 0)
				for i in range(lg_queue):
					queue[i] = u
					u = u*u + c
				# On regarde si on est déjà sorti du cercle de rayon 2
				n = 0
				while (n < lg_queue) and (abs(u) <= 2):
					n = n + 1
				# Si c'est le cas, on enregistre l'information
				if abs(u) > 2:
					for j in range(n):
						k, l = inv_ch_coord(queue[j])
						matrice[k, l] = n - j
				else:
					# On itère jusqu'à sortir du disque
					# de rayon 2 ou dépasser n_max
					while (n < n_max + lg_queue) and (abs(u) <= 2) and :
						u = u*u + c
						n = n + 1
					# On regarde si on est sorti
					if abs(u) > 2:
						matrice






						###### C'est compliqué !!!!!!!!
