#!/usr/bin/python
# -*-coding:utf-8 -*

from libjulia import *
from multiprocessing import *
import time

t = time.time()

def worker(a, b, q):
	for i in range(a, b):
		q.put(cree_julia(taille = 100, c = complex(0,i*0.01), verbose = False))
	print('fini : {}'.format((a, b)))

jobs = []

images_q = Queue()

for k in range(4):
	p = Process(target = worker, args = (k*25, (k+1)*25, images_q))
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
	
t_2 = time.time() - t

print("Temps d'execution 2 : {}".format(t_2))

