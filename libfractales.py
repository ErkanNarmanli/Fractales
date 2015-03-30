#!/usr/bin/python
# -*-coding:utf-8 -*-


import sys
import os
import re
from colorsys import *
from cmath import *
from PIL import Image, ImageDraw, ImageFont

#Améliore les bords du contour de la fractale
def ameliore_bord(image, taille):
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

#Rend TRUE si (k,l) a au moins un voisin noir
def voisin_noirs((k,l), image):
	return((image.getpixel((k-1, l-1)) == (0,0,0)) \
		or (image.getpixel((k-1, l)) == (0,0,0)) \
		or (image.getpixel((k-1, l+1)) == (0,0,0)) \
		or (image.getpixel((k-1, l-1)) == (0,0,0)) \
		or (image.getpixel((k, l-1)) == (0,0,0)) \
		or (image.getpixel((k, l+1)) == (0,0,0)) \
		or (image.getpixel((k+1, l-1)) == (0,0,0)) \
		or (image.getpixel((k+1, l)) == (0,0,0)) \
		or (image.getpixel((k-1, l+1)) == (0,0,0)))

#Rend la moyenne des prixels à coté
def moyenne((k,l), image):
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
	
	
	
	
	
	
#Multiplier un truple par un scalaire
#REND UN TRUPLE **ENTIER**
def mult_tpl(t, v):
	a = int(t*v[0])
	b = int(t*v[1])
	c = int(t*v[2])
	return (a, b, c)

#Additionne deux truples
def add_tpl(v, w):
	a = v[0] + w[0]
	b = v[1] + w[1]
	c = v[2] + w[2]
	return (a, b, c)

#Fonction de coloration d'un complexe
def couleur_complexe(z, largeur = 2.8):
	teinte = phase(z)/(2*pi)
	lumino = max(0, (1-abs(z)/largeur))
	col = hls_to_rgb(teinte, 150, lumino)
	c_1 = int(col[0])
	c_2 = int(col[1])
	c_3 = int(col[2])
	return (c_1, c_2, c_3)

#Fonction de coloration pour un truc zoli :)
def coloration_zoli(n, n_max, col_a, col_b):
	h = add_tpl(col_b, mult_tpl(-1, col_a))
	t = ((n_max - n)/float(n_max))**10
	res = add_tpl(col_a, mult_tpl(t, h))
	return res

# Fonction qui aligne du texte à droite dans un espace de t_max caractères
def ecrire(chaine, t_max):
	l = len(chaine)
	for m in range(t_max - l):
		sys.stdout.write(" ") 
	sys.stdout.write(chaine)

# Affiche une barre de chargement
def chargement(k, taille):
	pourc = 100*k/float(taille)
	pourv = 20*pourc/100. #pourvingt, parce que j'ai envie
	pourc = int(pourc) + 1
	pourv = int(pourv) + 1
	sys.stdout.write('\r')
	ecrire("{}% : ".format(pourc), 7)
	ecrire(str(k+1), len(str(taille)))
	sys.stdout.write('/{} pix'.format(taille))
	sys.stdout.write('   [')
	for m in range(pourv):
		sys.stdout.write(':')
	for m in range(20 - pourv):
		sys.stdout.write(' ')
	sys.stdout.write(']')
	sys.stdout.flush() # Rend l'affichage plus fluide

# Détermine les coordonnées dans le plan complexe
# à partir des coordonnées dans l'image
def ch_coord(k, l, taille, largeur, centre):
	return(complex( \
		(float(k) - taille/2.)*largeur/float(taille) + centre, \
		(float(l) - taille/2.)*largeur/float(taille) \
		))

# Demande à l'utilisateur s'il veut l'enregistrer et gère les versions
def enregistre(image, nom, dossier = 'Images'):
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
				image.save('{dossier}/{nom}_{taille}px.png'.format(dossier = dossier, nom = nom, taille = taille))
				print("Image enregistrée")
			else:
				print('Image non enregistrée')
		else:
			image.save('{dossier}/{nom}_{taille}px.png'.format(dossier = dossier, nom = nom, taille = taille))
			print('Image enregistrée')
	# L'utilisateur ne veut pas enregistrer
	else:
		print("Image non enregistrée")

# Détermine la couleur du pixel sur une echelle de gris en
# fonction du rang à partir duquel on sort du cercle de rayon 2
def couleur_pix(n, n_max, alpha = 5):
	if n == n_max:
		c = 0
	else:
		c = 20 + 235*((n_max - n)/float(n_max))**alpha
		c = int(c)
	return(c, c, c)

# Autre façon de colorier (toujours en noir en echelle de gris)
def couleur_pix_v2(n, n_max, n_min = 0, alpha = 5):
	if n == n_max:
		c = 0
	else:
		c = 20 + 235*((n_max - n)/float(n_max - n_min))**alpha
		c = int(c)
	return(c, c, c)


