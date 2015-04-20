#!/usr/bin/python
# -*-coding:utf-8-*-

"""
Serveur utilisant multiprocessing pour distribuer le calcul d'un grand
nombre d'ensembles de Julia sur différentes machines
"""

from multiprocessing.managers import SyncManager
from Queue import Queue, Empty
from time import sleep

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
def runserver(julia_dict):
	""" Lance le serveur qui va distribuer le calcul sur plusieurs machines """

	# On lance le manager qui va superviser les opérations
	manager = make_server_manager(PORT, AUTHKEY)
	job_queue = manager.get_job_queue()
	result_queue = manager.get_result_queue()

	# Séparation du dictionnaire en chuncks de petites tailles
	chunk_size = 50
	for i in xrange(0, len(julia_dict), chunk_size):
		little_dict = {k: c for k, c in julia_dict.items() if i <= k < i + chunk_size} 
		job_queue.put(little_dict)
	
	for i in xrange(0, len(julia_dict), chunk_size):
		print('Waiting for client ... ')
		print(result_queue.get())

	sleep(2)
	manager.shutdown()
