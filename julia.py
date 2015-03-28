#!/usr/bin/python
# -*-coding:utf-8 -*

from PIL import Image, ImageDraw, ImageFont
from math import sqrt
import os
import re
import sys
from libjulia import *

#On demande à l'utilisateur de rentrer les variables
taille = int(input("Taille en pixel : "))
part_r = float(input("Partie réelle : "))
part_i = float(input("Partie imaginaire : "))

# Constantes
largeur = 4.2
n_max = 200
alpha = 5
c = complex(part_r,part_i)

# On génère l'image
image = cree_julia(taille=taille, c=c, n_max=n_max, alpha=alpha, largeur = largeur)

# On l'affiche à l'écran et on demande à l'utilisateur s'il veut la sauvegarder
image.show()
reponse = ""
while (reponse != "o")and(reponse != "n"):
	reponse = raw_input("Voulez-vous sauvegarder l'image ?[O/n] : ")
	reponse = reponse.lower()

if reponse == "o":
	nom_ssext = 'julia_{}+i{}'.format(c.real,c.imag)
	# On récupère la liste des fichier dans Images et on filtre ceux qui sont
	# des julias de même paramètre c
	dossier = os.listdir('Images')
	expression = '^{}_([0-9]+)px\\.png$'.format(nom_ssext.replace('.', '\\.').replace('+', '\\+'))
	expression = re.compile(expression) # regex compilée
	versions = [fichier for fichier in dossier \
			if expression.match(fichier) ]
	if versions != []:
		# On génère la liste des tailles en pixels des Julias
		# de paramètre c déjà enregistrés
		versions_tailles = [int(expression.sub('\\1', fichier)) for fichier in versions]
		print("Cette image est déjà enregistrée dans les tailles suivantes :")
		for i in versions_tailles:
			print(i)
		reponse = ''
		while (reponse != 'o') and (reponse != 'n'):
			reponse = raw_input("Enregistrer quand même ?[O/n] : ")
			reponse = reponse.lower()
		if reponse == 'o':
			# Sauvegarde dans Images/
			image.save('Images/{nom}_{taille}px.png'.format(nom = nom_ssext, taille = taille))
			print("Image enregistrée")
		else:
			print('Image non enregistrée')
	else:
		image.save('Images/{nom}_{taille}px.png'.format(nom = nom_ssext, taille = taille))
		print('Image enregistrée')
else:
	print("Image non enregistrée")
