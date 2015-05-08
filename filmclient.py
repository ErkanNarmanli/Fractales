#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Lancement d'un client qui reçoit des ensembles de Julia à dessiner
"""

from multiprocessing.managers import SyncManager
from Queue import Queue, Empty
from mp_film import *

IP = 'sas.eleves.ens.fr' 
PORT = 12345
AUTHKEY = 'akey'

# Calcul des Julias
def mp_julia(job_queue, result_queue):
	""" Calcule de ensembles de Julia et enregistre les images """
	while True:
		try:
			julia_dict, taille = job_queue.get_nowait()
			launch_client(julia_dict, result_queue, taille)
		except Empty:
			return


# Création du client
def make_client_manager(ip, port, authkey):
	""" Renvoie un client capable d'exécuter les tâches d'un manager distant """
	class JuliaManager(SyncManager):
		pass

	JuliaManager.register('get_job_queue')
	JuliaManager.register('get_result_queue')

	manager = JuliaManager(address = (ip, port), authkey = authkey)
	manager.connect()
	print('Client connecté à {}:{}'.format(ip, port))
	return(manager)

# Mise en route du client
def runclient(ip = IP, port = PORT, authkey = AUTHKEY):
	""" Crée un client et le connecte au serveur distant pour recevoir les tâches à exécuter """
	manager = make_client_manager(ip, port, authkey)
	job_queue = manager.get_job_queue()
	result_queue = manager.get_result_queue()
	mp_julia(job_queue, result_queue)
