#!/usr/bin/python
# -*-coding:utf-8 -*-

"""
On cherche ici à obtenir des informations nous permettant de
de trouver une constante qui nous permetrait de calculer le temps
de calcul nécessaire AVANT de lancer le calcul
"""

from cmath import *
from zoomMandel import *

nb_points = 50
max_taille = 50
nb_images = 300


h = []
y = []
for k in range(nb_points):
	a = int(float(k)*max_taille/nb_points) + 1
	h = h + [a]
	y = y + [0]


for k in range(nb_points):
	t = h[k]
	chargement(k,nb_points)
	y[k] = faire_film(nb_images = t, verbose = False) 
print(" ")

print(y)

for k in range(nb_points):
	y[k] = y[k]/(h[k]*h[k])

print(y)

tot = 0
for k in range(nb_points):
	tot = tot + y[k]

tot = tot/nb_points
print(tot)
