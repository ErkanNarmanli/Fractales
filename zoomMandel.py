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
import os


dossier_sav = 'Images/framboisine'

taille 	   = 800
nb_images  = 1000
nprocs	   = 4		#supprimer cet variable à terme
verbose    = False

nb_digits = len(str(nb_images)) - 1


# Worker qui dessine et sauve les images
def workers(mandel_dict, nb_digits, no = None):
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
		image.save(dossier_sav + '/img_{}.png'\
				.format(str(mandel_id+1).zfill(nb_digits)))

	#print('Terminé {}'.format(no))


# Gestion des différents processus
def launch_client(mandel_dict, nb_digits = None):
	"""
	Lance les processus calculant les mandels indiqués par le dictionnaire
	nb_digits est le nombre de chiffres à mettre dans le noms de fichiers.
	Attention : il faut que le nombre d'entrées de mandel_dict soit 
	divisible par nprocs sinon le résultat ne sera pas celui attendu
	"""

	t_init = time.time()
	nb_ids = len(mandel_dict)
	print('Quantité de processus à traiter : {}'.format(nb_ids))
	print('Quantité de pétites entre lequels on les réparti : {}'.format(nprocs))
	jobs = []
	
	# Si nb_digits est mal ou non specifié, on le déduit de nb_ids
	if type(nb_digits) != type(0):
		nb_digits = len(str(nb_ids))
	
	
	ecrire("Repartition des processus...")
	for k in range(nprocs):
		if verbose:
			chargement(k, nprocs)
		chunck 	= {cle: nb for cle, nb in mandel_dict.items() if k*nb_ids/nprocs <= cle < (k+1)*nb_ids/nprocs}		
		p	= Process(target = workers, args = (chunck, nb_digits, k))
		jobs.append(p)
		p.start()
	print("     Done!")
	
	ecrire("Récolte des pépites...")
	for p in jobs:
		p.join()

		# print('Joined {}'.format(p))
	print("     Done!")
		
	t_exec = time.time() - t_init
	print("Temps d'execution : {}".format(t_exec))


def images_zoom(pt_zoom = complex(0,0), pt_init = complex(-0.7,0), taille_min = 0.0005):
	"""
	Fonction qui génère les images pour la vidéo
	En zoomant en changeant de centre de telle sorte que :
		le centre initial soit pt_init
		le centre final soit pt_zoom
	"""
	dictionnaire = dict()
	dictionnaire = {}
	for k in range(nb_images):
		t = float(k)/nb_images
		dictionnaire[k]	= dict()
		dictionnaire[k]	= {}
		dictionnaire[k]["centre"]	= pt_init + t*(pt_zoom - pt_init)
		dictionnaire[k]["n_max"]	= 200
		dictionnaire[k]["largeur"]	= taille_min + (2.8 - taille_min)*(1 - t)

	launch_client(mandel_dict = dictionnaire, nb_digits = nb_digits)


# ET HOP ! On commence à travailler !
t_init_gen = time.time()
# On vide le dossier, hein on est pas des cochons
print("Suppression du contenu du dossier " + dossier_sav)
os.system("cd " + dossier_sav + " ; rm *")


# On calcule nos images :)
print("Calcul des images")
images_zoom(pt_zoom = complex(-1.250666667,0.345333333))

# On lance la création du film
print("Montage des images en film")
os.system("cd " + dossier_sav + " ; ffmpeg -v quiet -f image2 -r 10 -i img_%0{}d.png -vcodec mpeg4 -y movie.mp4".format(nb_digits))
t_exec = time.time() - t_init_gen
print("Temps total d'execution : {}".format(t_exec))
