#!/usr/bin/python
# -*-coding:utf-8 -*

from cmath import cos, rect, pi
from mp_film import *
import pickle

def ajoute_ligne(depart, arrivee, inv_vitesse, pickler):
	""" Ajoute une ligne d'images à la liste """
	i_max = int(inv_vitesse*abs(arrivee - depart))
	for i in xrange(i_max):
		pickler.dump(depart + i*(arrivee-depart)/float(i_max))

			
with open('liste', 'ab') as fichier:
	pickler = pickle.Pickler(fichier)

	# Cardioïde
	for i in range(314):
		pickler.dump(0.25 + rect((0.5*(1 - cos(pi*i/314)) + 0.05).real, pi*i/314))
	
	ajoute_ligne(complex(-0.80, 0), complex(-2, 0), 125, pickler)
	ajoute_ligne(complex(-2, 0), complex(-1.3, 0.06), 100, pickler)
	ajoute_ligne(complex(-1.3, 0.06), complex(-1.25, 0.028), 125, pickler)
	ajoute_ligne(complex(-1.25, 0.028), complex(-1.22, 0.16), 125, pickler)
	ajoute_ligne(complex(-1.22, 0.16), complex(-1.1433, 0.2147), 125, pickler)
	ajoute_ligne(complex(-1.1433, 0.2147), complex(-1.2553, 0.3780), 125, pickler)
	ajoute_ligne(complex(-1.2553, 0.3780), complex(-0.7607, 0.0887), 125, pickler)
	ajoute_ligne(complex(-0.7607, 0.0887), complex(-0.4573, 0.5973), 125, pickler)
	ajoute_ligne(complex(-0.4573, 0.5973), complex(-0.2380, 0.7607), 125, pickler)
	ajoute_ligne(complex(-0.2380, 0.7607), complex(0.35, 0.5833), 125, pickler)
	ajoute_ligne(complex(0.35, 0.5833), complex(0.3173, 0.0607), 125, pickler)
	ajoute_ligne(complex(0.3173, 0.0607), complex(0.3173, 0), 300, pickler)
