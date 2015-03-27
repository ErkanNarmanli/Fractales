#!/usr/bin/python
# -*-encoding:utf-8-*-

from libmandel import *

# On demande une taille à l'utilisateur
taille = int(raw_input("Taille en pixels : "))

# On génère l'image
image = cree_mandelbrot(taille = taille)

# On montre l'image à l'utilisateur
image.show()

reponse = ''
while (reponse != 'o') and (reponse != 'n'):
	reponse = raw_input("Voulez-vous sauvegarder l'image ?[O/n] : ")
	reponse = reponse.lower()

if reponse == 'o':
	image.save('Image/mandelbrot_{}px.png'.format(taille))
	print('Image enregistrée dans Images/')
else:
	print('Image non enregistrée')

