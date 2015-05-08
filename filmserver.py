#!/usr/bin/python
# -*-coding:utf-8-*-

"""
Serveur utilisant multiprocessing pour distribuer le calcul d'un grand
nombre d'ensembles de Julia sur différentes machines
"""

from multiprocessing.managers import SyncManager
from Queue import Queue, Empty
from time import sleep
import os

from PIL import Image

PORT = 12345
AUTHKEY = 'akey'

# Création du manager
def make_server_manager(port , authkey):
	""" Renvoit un objet qui gère la distribution des tâches """
	job_queue = Queue()
	result_queue = Queue()
	
	# On surcharge la classe SyncManager
	class JuliaManager(SyncManager):
		pass
	
	JuliaManager.register('get_job_queue', callable = lambda: job_queue)
	JuliaManager.register('get_result_queue', callable = lambda: result_queue)

	manager = JuliaManager(address = ('', port), authkey = authkey)
	manager.start()
	print('Serveur lancé sur le port {}'.format(port))
	return(manager)

# Lancement du serveur
def runserver(julia_dict, save_dir, taille):
	""" Lance le serveur qui va distribuer le calcul sur plusieurs machines """

	# On lance le manager qui va superviser les opérations
	manager = make_server_manager(PORT, AUTHKEY)
	job_queue = manager.get_job_queue()
	result_queue = manager.get_result_queue()

	# Séparation du dictionnaire en chuncks de petites tailles et envoi aux clients
	chunk_size = 30
	for i in xrange(0, len(julia_dict), chunk_size):
		little_dict = {k: c for k, c in julia_dict.items() if i <= k < i + chunk_size} 
		job_queue.put((little_dict, taille))
	
	# On attend les clients
	print('Attente des réponses des clients ... ')
	for i in xrange(len(julia_dict)):
		image, number = result_queue.get()
		image.save(save_dir + '/img_' + str(number).zfill(6) + '.png')
	
	# On monte le film
	print('\nGénération du film\n')
	os.system("cd " + save_dir + " ; ffmpeg -framerate 10 -i img_%06d.png -c:v libx264 -r 30 -pix_fmt yuv420p movie.mp4")

	# On laisse un peu de temps aux clients pour réaliser que leur travail est terminé
	sleep(2)
	print('Fermeture du serveur')
	manager.shutdown()


