#!/usr/bin/python
# -*-coding:utf-8 -*

""" 

Fonctions permettant le calcul d'une liste d'ensembles de Julia
à l'aide multiprocessing

"""

from libjulia import cree_julia
from multiprocessing import *
import time

dossier_sav = 'Images/broceliande'

nprocs = 4
taille = 100

# Worker qui dessine et sauve des Julias
def worker(julia_dict, nb_digits, no = None):
	""" Dessine une liste d'ensembles de Julia et les sauve dans un dossier.
	Reçoit en argument un dictionnaire dont les clés sont les ids des Julias et 
	les valeurs sont des complexes correspondant aux Julias à dessiner
	La variable no sert seulement à afficher des informations à l'utilisateur"""
	for julia_id, c in julia_dict.items():
		image = cree_julia(taille = taille, c = c, verbose = False)
		image.save(dossier_sav + '/img_{}.png'.format(str(julia_id+1).zfill(nb_digits)))
	print('Terminé  {}'.format(no))


# Gestion des différents processus
def launch_client(julia_dict, nb_digits = None):
	""" Lance les processus calculant les Julias indiqués par le dictionnaire.
	nb_digits est le nombre de digits à mettre dans les noms de fichiers.
	Attention : Il faut que le nombre d'entrées de julia_dict soit divisble par nprocs sinon
	le résultat ne sera pas le résultat attendu """

	t_init = time.time()
	nb_ids = len(julia_dict)
	print('number of ids : {}'.format(nb_ids))
	jobs = []
	# Si nb_digits est mal ou non spécifié, on le déduit de nb_ids
	if type(nb_digits) != type(0):
		nb_digits = len(str(nb_ids))

	for k in range(nprocs):
		chunck = {cle: nb for cle, nb in julia_dict.items() if k*nb_ids/nprocs <= cle < (k+1)*nb_ids/nprocs}
		p = Process(target = worker, args = (chunck, nb_digits, k))
		jobs.append(p)
		p.start()

	for p in jobs:
		p.join()
		print('Joined {}'.format(p))

	t_exec = time.time() - t_init
	print("Temps d'execution : {}".format(t_exec))


