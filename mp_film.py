#!/usr/bin/python
# -*-coding:utf-8 -*

from libjulia import *
from multiprocessing import *
import time

dossier_sav = 'Images/broceliande'

t = time.time()
nprocs = 4

img_queue = Queue()

def worker(a, b):
	for i in range(a, b):
		image = cree_julia(taille = 100, c = complex(0,i*0.01), verbose = False)
		image.save(dossier_sav + '/img_{}.png'.format(i))
	print('fini : {}'.format((a, b)))

jobs = []

for k in range(nprocs):
	p = Process(target = worker, args = (k*100/nprocs, (k+1)*100/nprocs))
	jobs.append(p)
	p.start()

for p in jobs:
	p.join()
	print('Joined {}'.format(p))

t_1 = time.time() - t
print("Temps d'execution 1 : {}".format(t_1))

t = time.time()


for k in range(100):
	chargement(k,100)
	image = cree_julia(taille = 100, c = complex(0,k*(0.01)), verbose = False)
	image.save(dossier_sav + '/img_{}.png'.format(k))

t_2 = time.time() - t

print("\nTemps d'execution 2 : {}".format(t_2))

