#!/usr/bin/python
# -*-coding:utf-8 -*

"""

Fonctions permettant le calcul de tout plein d'image zoomant sur
le Mandelbrot pour faire une video super zolie ! :)

"""

from libfractales import *
from libmandel import cree_mandelbrot
from multiprocessing import *
import time
import sys
import os


# Worker qui dessine et sauve les images
def workers(mandel_dict, taille, nb_digits, save_dir, no = None):
	"""
	Dessine une liste de Mandel et les sauve dans un dossier.
	Reçoit en argument un dictionnaire dont les clefs sont les ids des Mandel
	et les valeurs sont des p-uplet avec les arguments pour creer_mandelbrot
	La variable no sert seulement à afficher des informations à l'utilisateur
	"""
	
	for mandel_id, infos in mandel_dict.items():
		image = cree_mandelbrot(taille = taille,\
				centre = infos["centre"],\
				n_max = infos["n_max"],\
				largeur = infos["largeur"],\
				verbose = False)
		image.save(save_dir + '/img_{}.png'\
				.format(str(mandel_id+1).zfill(nb_digits)))

	#print('Terminé {}'.format(no))


# Gestion des différents processus
def launch_client(mandel_dict, nb_images, nprocs, taille = 600, nb_digits = None, save_dir = "Images/framboisine", verbose = True):
	"""
	Lance les processus calculant les mandels indiqués par le dictionnaire
	nb_digits est le nombre de chiffres à mettre dans le noms de fichiers.
	Attention : il faut que le nombre d'entrées de mandel_dict soit 
	divisible par nprocs sinon le résultat ne sera pas celui attendu
	"""

	t_init = time.time()
	nb_ids = len(mandel_dict)
	if verbose:
		print('Quantité de processus à traiter : {}'.format(nb_ids))
		print('Quantité de pétites entre lequels on les réparti : {}'.format(nprocs))
	jobs = []
	
	# Si nb_digits est mal ou non specifié, on le déduit de nb_ids
	if type(nb_digits) != int:
		nb_digits = len(str(nb_ids))
	
	#Distribution des tâches
	if verbose: print("Repartition des processus :")
	for k in xrange(nprocs):
		min_index = min(mandel_dict.keys())
		dict_size = len(mandel_dict)
		chunck 	  = {index: c for index, c in mandel_dict.items() if min_index + k*dict_size/nprocs <= index < min_index + (k+1)*dict_size/nprocs}		
		p	  = Process(target = workers, args = (chunck, taille, nb_digits, save_dir, k))
		jobs.append(p)
		p.start()
		if verbose: chargement(len(jobs) - 1, nprocs)
	if verbose: print(" ")

	# On attend que tous les processus se terminent
	if verbose: print("Récolte des pépites...")
	if verbose: cpt = 0
	for p in jobs:
		p.join()
		
		# print('Joined {}'.format(p))
		if verbose: chargement(cpt, nprocs)
		if verbose: cpt += 1

	if verbose: print(" ")	
	t_exec = time.time() - t_init
	if verbose: ecrire_temps(t_exec)

def creer_dico(nb_images, pt_zoom = complex(0,0), pt_init = complex(-0.7,0), taille_min = 0.005):
	"""
	Fonction qui génère les images pour la vidéo
	En zoomant en changeant de centre de telle sorte que :
		le centre initial soit pt_init
		le centre final soit pt_zoom
	"""
	dictionnaire = {}
	for k in range(nb_images):
		t = sqrt(float(k)/nb_images)
		dictionnaire[k]	= dict()
		dictionnaire[k]	= {}
		dictionnaire[k]["centre"]	= pt_init + t*(pt_zoom - pt_init)
		dictionnaire[k]["n_max"]	= 200
		dictionnaire[k]["largeur"]	= taille_min + (2.8 - taille_min)*(1 - t)
	return dictionnaire


def faire_film(taille = 100, pt_zoom = complex(-1.250666667,0.345333333), nb_images = 300, nprocs = None, verbose = True, nb_digits = None, dossier_sav = 'Images/framboisine'):
	# ET HOP ! On commence à travailler !
	t_init_gen = time.time()

	# On regarde si nb_digit est spécifié
	if type(nb_digits) != int:
		nb_digits = len(str(nb_images)) - 1

	# On regarde si nprocs est spécifié
	if type(nprocs) != int:
		nprocs = nb_images

	# On vide le dossier, hein on est pas des cochons	
	if verbose: print("Suppression du contenu du dossier " + dossier_sav)
	os.system("cd " + dossier_sav + " ; rm *")
		
	
	# On calcule nos images :)
	if verbose: print("Génération du dictionnaire des images")
	dictionnaire = creer_dico(pt_zoom = pt_zoom, nb_images = nb_images)
	
	# On lance le client
	if verbose: print("Calcul des images")
	launch_client(mandel_dict = dictionnaire, taille = taille, nb_digits = nb_digits, save_dir = dossier_sav, nb_images = nb_images, nprocs = nprocs, verbose = verbose)
	
	# On lance la création du film
	if verbose: print("Montage des images en film")
	os.system("cd " + dossier_sav + " ; ffmpeg -v quiet -f image2 -r 10 -i img_%0{}d.png -vcodec mpeg4 -y movie.mp4".format(nb_digits))
	t_exec = time.time() - t_init_gen
	if verbose: ecrire_temps(t_exec)

	return t_exec
