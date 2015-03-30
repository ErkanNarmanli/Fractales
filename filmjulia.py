#!/usr/bin/python
# -*-coding:utf-8 -*

from libjulia import *

NB_Images 	= 200			#Nombre d'images de le clip
depart 		= complex(0.5,0)	#point de départ
arrivee 	= complex(-1.9,0)	#point d'arrivée
resolution 	= 200			#taille de la vidéo (carrée)

pas 	 = abs(depart - arrivee)/float(NB_Images)
nb_digit = len(str(NB_Images))

for k in range(NB_Images):
	chargement(k, NB_Images)
	#On prend le nouveau nombre complexe sur le segment
	c = depart + float(k)*pas*(arrivee - depart)
	#On crée l'image correspondante
	image = cree_julia(taille = resolution, c = c, verbose = False)
	#On l'enregistre au bon nom
	image.save('Images/Img_film/Film_' + str(k+1).zfill(nb_digit) + '.png')
	
print('Création des images terminées')
print('Pour finaliser faire la commande suivante dans le répertoire contenant les images :')
print('ffmpeg -f image2 -r 10 -i Film_%0{}d.png -vcodec mpeg4 -y movie.mp4'.format(nb_digit))
