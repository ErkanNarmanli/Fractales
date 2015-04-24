#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
sys.path.append('../')


import pickle
import sys
import os
from filmserver import *


def ajoute_ligne(start_pt, end_pt, img_freq, img_dict, index):
	""" Ajoute les images d'un segment au dictionnaire """
	i_max = int(img_freq*abs(start_pt - end_pt))
	for i in xrange(i_max):
		index += 1
		img_dict[index] = start_pt + i*(end_pt-start_pt)/float(i_max)
	return  index

def mp_make_film(file_path, save_dir = 'imgs', taille = 600):
	""" Lance un serveur manageant la génération de la liste d'image contenue
	dans le fichier file_path. On génère ensuite un film à partir de ces images """
	images_dict = {}
	nb_images = 0
	# Lecture du fichier contenant la liste des Julias à dessiner
	try:
		with open(file_path, 'rb') as fichier:
			unpickler = pickle.Unpickler(fichier)
			while True:
				try:
					start_pt, end_pt, img_freq = unpickler.load()
					nb_images = ajoute_ligne(start_pt, end_pt, \
							img_freq, images_dict, nb_images)
				except EOFError:
					break
	except IOError: # Erreur à l'ouverture du fichier 
		print("Le fichier spécifié n'existe pas")
		exit(1)

	# Lancement du serveur
	runserver(images_dict, save_dir, taille)
	print('Terminé')
