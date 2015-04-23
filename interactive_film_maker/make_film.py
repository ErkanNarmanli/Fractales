#!/usr/bin/python
# -*- coding:utf-8 -*-

import pickle
import sys
import os
from filmserver import *


try:
	images_list = sys.argv[1]
except IndexError:
	print("Aucun fichier n'est spécifié")
	exit(1)
try:
	save_dir = sys.argv[2]
except IndexError:
	save_dir = 'imgs'

images_dict = {}
nb_images = 0

# Lecture du fichier contenant la liste des Julias à dessiner
try:
	with open(images_list, 'rb') as fichier:
		unpickler = pickle.Unpickler(fichier)
		while True:
			try:
				c = unpickler.load()
				nb_images += 1
				images_dict[nb_images] = c
			except EOFError:
				break
except IOError: # Erreur à l'ouverture du fichier 
	print("Le fichier spécifié n'existe pas")
	exit(1)

# Lancement du serveur
runserver(images_dict, save_dir)
