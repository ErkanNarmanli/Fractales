#!/usr/bin/python
# -*-coding:utf-8 -*

""" 

Fonctions permettant le calcul d'une liste d'ensembles de Julia
à l'aide multiprocessing

"""

from libjulia import cree_julia
from multiprocessing import *
import time

DEFAULT_SAVE_DIR = 'Images/broceliande'

# Worker qui dessine et sauve des Julias
def worker(index, c, result_queue, taille):
	"""
	Dessine une liste d'ensembles de Julia et les place dans result_queue.
	"""
	image = cree_julia(taille = taille, c = c, verbose = False)
	result_queue.put((list(image.getdata()), index))


# Gestion des différents processus
def launch_client(julia_dict, result_queue, taille = 600):
	"""
	Lance les processus calculant les Julias indiqués par le dictionnaire.
	"""

	t_init = time.time()
	nb_images = len(julia_dict)
	print('number of images : {}'.format(nb_images))
	jobs = []
	
	# Distribution des tâches
	for index, c in julia_dict.items():
		p = Process(target = worker, args = (index, c, result_queue, taille))
		jobs.append(p)
		p.start()
	
	# On attend que tous les processus se terminent
	for p in jobs:
		p.join()

	t_exec = time.time() - t_init
	print("Temps d'exécution : {}".format(t_exec))


