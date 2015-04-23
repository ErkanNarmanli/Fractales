#!/usr/bin/python
# -*-coding:utf-8 -*-

"""
On cherche ici à obtenir des informations nous permettant de
savoir comment l'on doit faire avancer n_max lorsque l'on se 
rapproche de l'ensemble de mandelbrot
"""

from cmath import *
from libfractales import *
import matplotlib.pyplot as plt
import numpy as np

nb_points = 2000
n_max	  = 2000

pos_1 	= complex(-0.75, 0)
pos_2	= complex(-0.75, 0.3)

dist	= abs(pos_1 - pos_2)


def my_fonction(t, n_max):
	c = pos_1 - t*(pos_1 - pos_2)
	u = complex(0,0)
	n = 0
	# Si on est dans la cardioïde, on ne fait pas les tests
	if 2*abs(c-0.25) < (1 - cos(phase(c-0.25))).real:
		res = n_max
	else:
		while abs(u) <= 2 and n < n_max:
			u = u*u + c
			n = n + 1
	res = n
	return res

h = np.linspace(0,1,nb_points)
x = np.linspace(0,dist,nb_points)
y = np.zeros(nb_points)

for k in range(nb_points):
	t = h[k]
	chargement(k,nb_points)
	y[k] = my_fonction(t, n_max)
print(" ")

plt.plot(x,y)
plt.show()

