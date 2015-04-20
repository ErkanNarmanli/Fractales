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
nprocs = 4

# Worker qui dessine et sauve des Julias
def worker(julia_dict, taille, nb_digits, save_dir, no = None):
	""" Dessine une liste d'ensembles de Julia et les sauve dans un dossier.
	Reçoit en argument un dictionnaire dont les clés sont les ids des Julias et 
	les valeurs sont des complexes correspondant aux Julias à dessiner
	La variable no sert seulement à afficher des informations à l'utilisateur"""
	for index, c in julia_dict.items():
		image = cree_julia(taille = taille, c = c, verbose = False)
		image.save(save_dir + '/img_{}.png'.format(str(index).zfill(nb_digits)))
	print('Terminé  {}'.format(no))


# Gestion des différents processus
def launch_client(julia_dict, taille = 600, nb_digits = None, save_dir = DEFAULT_SAVE_DIR):
	""" Lance les processus calculant les Julias indiqués par le dictionnaire.
	nb_digits est le nombre de digits à mettre dans les noms de fichiers.
	Attention : Il faut que le nombre d'entrées de julia_dict soit divisble par nprocs sinon
	le résultat ne sera pas le résultat attendu """

	t_init = time.time()
	nb_images = len(julia_dict)
	print('number of images : {}'.format(nb_images))
	jobs = []
	
	# Si nb_digits est mal ou non spécifié, on le déduit de nb_images
	if type(nb_digits) != int:
		nb_digits = len(str(nb_images))
	
	# Distribution des tâches
	for k in xrange(nprocs):
		min_index = min(julia_dict.keys())
		dict_size = len(julia_dict)
		little_dict = {index: c for index, c in julia_dict.items() if min_index + k*dict_size/nprocs <= index < min_index + (k+1)*dict_size/nprocs }
		p = Process(target = worker, args = (little_dict , taille, nb_digits, save_dir, k))
		jobs.append(p)
		p.start()
	
	# On attend que tous les processus se terminent
	for p in jobs:
		p.join()

	t_exec = time.time() - t_init
	print("Temps d'exécution : {}".format(t_exec))


