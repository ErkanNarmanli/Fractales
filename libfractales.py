#!/usr/bin/python
# -*-coding:utf-8 -*-

"""
Fonctions utiles un peu partout
""" 

import sys
import os
import re
from colorsys import *
from cmath import *
from PIL import Image, ImageDraw, ImageFont

def ecrire_temps(t):
	nb_sec = t%60
	nb_min = t/60
	if nb_min < 1:
		print("Temps d'exécution : {} sec".format(nb_sec))
	else:
		print("Temps d'exécution : {} min et {} sec".format(nb_min, nb_sec))

def ameliore_bord(image, taille):
	"""Améliore les bords du contour de la fractale """
	print("Lissage de l'image")
	draw = ImageDraw.Draw(image)
	for k in range(taille):
		chargement(k, taille)
		for l in range (taille):
			if image.getpixel((k,l)) == (0,0,0):
				if not voisin_noirs((k,l), image):
					draw.point((k,l), moyenne((k,l), image))	
	print("\n")
	return image

def voisin_noirs((k,l), image):
	""" Rend TRUE si (k,l) a au moins un voisin noir"""
	return((image.getpixel((k-1, l-1)) == (0,0,0)) \
		or (image.getpixel((k-1, l)) == (0,0,0)) \
		or (image.getpixel((k-1, l+1)) == (0,0,0)) \
		or (image.getpixel((k-1, l-1)) == (0,0,0)) \
		or (image.getpixel((k, l-1)) == (0,0,0)) \
		or (image.getpixel((k, l+1)) == (0,0,0)) \
		or (image.getpixel((k+1, l-1)) == (0,0,0)) \
		or (image.getpixel((k+1, l)) == (0,0,0)) \
		or (image.getpixel((k-1, l+1)) == (0,0,0)))

def moyenne((k,l), image):
	"""Rend la moyenne des pixels à coté"""
	tot = (0,0,0)
	tot = add_tpl(tot, (image.getpixel((k-1, l-1))))
	tot = add_tpl(tot, (image.getpixel((k-1, l))))
	tot = add_tpl(tot, (image.getpixel((k-1, l+1))))
	tot = add_tpl(tot, (image.getpixel((k, l-1))))
	tot = add_tpl(tot, (image.getpixel((k, l+1))))
	tot = add_tpl(tot, (image.getpixel((k+1, l-1))))
	tot = add_tpl(tot, (image.getpixel((k+1, l))))
	tot = add_tpl(tot, (image.getpixel((k+1, l+1))))
	tot = mult_tpl(0.125, tot)
	return tot
	
def mult_tpl(t, v):
	"""Multiplie un truple par un scalaire
	REND UN TRUPLE ***ENTIER***"""
	a = int(t*v[0])
	b = int(t*v[1])
	c = int(t*v[2])
	return (a, b, c)

def add_tpl(v, w):
	"""Additionne deux truples"""
	a = v[0] + w[0]
	b = v[1] + w[1]
	c = v[2] + w[2]
	return (a, b, c)

def couleur_complexe(z, largeur = 2.8):
	"""Fonction de coloration d'un complexe
	la teinte dépend de l'argument et la saturation du module"""
	teinte = phase(z)/(2*pi)
	lumino = max(0, (1-abs(z)/largeur))
	col = hls_to_rgb(teinte, 150, lumino)
	c_1 = int(col[0])
	c_2 = int(col[1])
	c_3 = int(col[2])
	return (c_1, c_2, c_3)

#Fonction de coloration pour un truc zoli :)
def coloration_zoli(n, n_max, col_a, col_b):
	"""Colorie en fonction de la vitesse de divergence
	colorie selon un dégradé entre col_a et col_b
	le dégradé est écrasé par un puissance"""
	h = add_tpl(col_b, mult_tpl(-1, col_a))
	t = ((n_max - n)/float(n_max))**10
	res = add_tpl(col_a, mult_tpl(t, h))
	return res

def ecrire(chaine, t_max = 0):
	"""Fonction qui aligne du texte à droite dans un espace de t_max caractères"""
	l = len(chaine)
	for m in range(t_max - l):
		sys.stdout.write(" ") 
	sys.stdout.write(chaine)

def chargement(k, taille):
	"""Affiche une barre de chargement
	ne fini pas par un \n"""
	pourc = 100*k/float(taille)
	pourv = 20*pourc/100. #pourvingt, parce que j'ai envie
	pourc = int(pourc) + 1
	pourv = int(pourv) + 1
	sys.stdout.write('\r')
	ecrire("{}% : ".format(pourc), 7)
	ecrire(str(k+1), len(str(taille)))
	sys.stdout.write('/{} item'.format(taille))
	sys.stdout.write('   [')
	for m in range(pourv):
		sys.stdout.write(':')
	for m in range(20 - pourv):
		sys.stdout.write(' ')
	sys.stdout.write(']')
	sys.stdout.flush() # Rend l'affichage plus fluide

# Utile dans in_ch_coord
def arrondi(x):
	""" Renvoit l'entier le plus proche de x """
	x_inf = int(x)
	x_sup = x_inf +  1
	if x - x_inf < x_sup - x:
		return(x_inf)
	else:
		return(x_sup)

def ch_coord(k, l, taille, largeur, centre):
	""" Détermine les coordonnées dans le plan complexe du pixel k,l """
	return(complex( \
		(float(k) + 0.5 - taille/2.)*largeur/float(taille) + centre.real, \
		(float(l) + 0.5 - taille/2.)*largeur/float(taille) + centre.imag\
		))

def inv_ch_coord(c, taille, largeur, centre):
	""" Fonction inverse de la fonction ch_coord
	Retourne des entiers """
	x, y = c.real, c.imag
	k = arrondi((x-centre.real)*taille/float(largeur) + taille/2. - 0.5)
	l = arrondi((y-centre.imag)*taille/float(largeur) + taille/2. - 0.5)
	return(k, l)

def enregistre(image, nom, nom_dossier = 'Images'):
	""" On demande à l'utilisateur s'il souhaite enregistrer l'image.
	Le cas échéant, on cherche dans le dossier 'nom_dossier' d'autres versions de la même image qu'on présente à l'utilisateur.
	On demande ensuite une confirmation si d'autres versions existent """
	# On demande à l'utilisateur de faire un choix
	reponse = ''
	while (reponse != 'o') and (reponse != 'n'):
		reponse = raw_input("Voulez-vous sauvegarder l'image ?[O/n] : ")
		reponse = reponse.lower()
	# Début des vérifications
	if reponse == "o":
		taille = image.size[0]
		# On récupère la liste des fichier
		dossier = os.listdir('Images')
		# On échappe les . et les +
		expression = '^{}_([0-9]+)px\\.png$'.format(nom.replace('.', '\\.').replace('+', '\\+')) 
		expression = re.compile(expression) # regex compilée
		# On cherche les autres versions de la même image
		versions = [fichier for fichier in dossier \
			if expression.match(fichier) ]
		if versions != []:
			# On génère la liste des tailles en pixels des images déjà enregistrées
			versions_tailles = [int(expression.sub('\\1', fichier)) for fichier in versions]
			print("Cette image est déjà enregistrée dans les tailles suivantes :")
			for i in versions_tailles:
				print(i)
			# On attend une réponse de l'utilisateur
			reponse = ''
			while (reponse != 'o') and (reponse != 'n'):
				reponse = raw_input("Enregistrer quand même ?[O/n] : ")
				reponse = reponse.lower()
			if reponse == 'o':
				# Sauvegarde dans le dossier choisi
				image.save('{dossier}/{nom}_{taille}px.png'.format(dossier = nom_dossier, nom = nom, taille = taille))
				print("Image enregistrée")
			else:
				print('Image non enregistrée')
		else:
			image.save('{dossier}/{nom}_{taille}px.png'.format(dossier = nom_dossier, nom = nom, taille = taille))
			print('Image enregistrée')
	# L'utilisateur ne veut pas enregistrer
	else:
		print("Image non enregistrée")

# Fonction pour la coloration
def couleur_pix(n, n_max, alpha = 5):
	""" Assigne une couleur en fonction du rang n à partir duquel la suite qui intervient dans la définition du mandelbrot dépasse le module 2 """
	if n == n_max:
		c = 0
	else:
		c = 20 + 235*((n_max - n)/float(n_max))**alpha
		c = int(c)
	return(c, c, c)

# Autre coloration
def couleur_pix_v2(n, n_max, n_min = 0, alpha = 5):
	""" Autre coloration """
	if n == n_max:
		c = 0
	else:
		c = 20 + 235*((n_max - n)/float(n_max - n_min))**alpha
		c = int(c)
	return(c, c, c)


