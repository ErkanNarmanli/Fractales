#!/usr/bin/python
# -*-coding:utf-8 -*

"""
Script calculant suffisamment d'ensembles de Julia pour faire une animations
"""

from libjulia import *
from cmath import *
from time import time

NB_Images 	= 300			# Nombre d'images du clip
depart 		= complex(0.5,0)	# point de départ
arrivee 	= complex(-1.9,0)	# point d'arrivée
resolution 	= 200			# taille de la vidéo (carrée)
epsilon		= 0.1

nb_digit = len(str(NB_Images))

t = time()

for k in range(NB_Images):
	chargement(k, NB_Images)
	#On prend le nouveau nombre complexe sur le segment
	t = k/float(NB_Images)
	arg = t*pi
	mod = 0.5*(1-cos(arg)).real + epsilon
	c   = rect(mod, arg) + 0.25
	#LINEAIRE c = depart + k/float(NB_Images)*(arrivee-depart)
	#On crée l'image correspondante
	image = cree_julia(taille = resolution, c = c, verbose = False)
	#On l'enregistre au bon nom
	image.save('Images/Img_film/Film_' + str(k+1).zfill(nb_digit) + '.png')
	
print("Création des images terminée, temps d'execution : {} s".format(time() - t))
print('Pour finaliser faire la commande suivante dans le répertoire contenant les images :')
print('ffmpeg -f image2 -r 10 -i Film_%0{}d.png -vcodec mpeg4 -y movie.mp4'.format(nb_digit))
