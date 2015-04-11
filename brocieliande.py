#!/usr/bin/python
# -*-coding:utf-8 -*

from libjulia import *
from multiprocessing import *
import time
import sys

t = time.time()

def worker(a,b):
	for i in range(a,b):
		chargement(i,100)
		image = cree_julia(taille = 100, c = complex(0,-i*(0.001)), verbose = False)
	return

jobs = []

for k in range(4):
	p = Process(target = worker, args = (k*25,k*25+25))
	jobs.append(p)
	p.start()
	p.join()


t_1 = time.time() - t
print("Temps d'execution 1 : {}".format(t_1))

t = time.time()


for k in range(100):
	chargement(k,100)
	image = cree_julia(taille = 100, c = complex(0,-k*(0.001)), verbose = False)
	
t_2 = time.time() - t

print("Temps d'execution 2 : {}".format(t_2))

