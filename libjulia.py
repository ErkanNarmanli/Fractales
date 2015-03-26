#!/usr/bin/python
# -*-coding:utf-8 -*

from PIL import Image, ImageDraw, ImageFont
from math import sqrt
import time
import sys


# Détermine les coordonnées dans le plan complexe
# à partir des coordonnées dans l'image
def ch_coord(k, l, taille, largeur):
	return(complex( \
		(k - taille/2.)*largeur/float(taille), \
		(l - taille/2.)*largeur/float(taille) \
		))

# Détermine la couleur du pixel en fonction du rang à partir
# duquel on sort du cercle de rayon 2
def couleur_pix(n, n_max, alpha):
	if n == n_max: 
		col = 0
	else:
		col = 230*((n_max - n)/float(n_max))**alpha + 25
	col = int(col)
	return(col, col, col)

def ecrire(chaine,t_max):
	for m in range(t_max-len(chaine)):
		sys.stdout.write(" ")
	sys.stdout.write(chaine)

def chargement(k, taille):
	pourc = 100*k/float(taille)
	pourv = 20*pourc/100.  #pourvingt, parce que j'ai envie
	pourc = int(pourc)+1
	pourv = int(pourv)+1
	sys.stdout.write("\r")
	ecrire("{}%:".format(pourc),5)
	ecrire(str(k+1),len(str(taille)))
	sys.stdout.write("/{} pix".format(taille))
	sys.stdout.write("   [")
	for m in range(pourv):
		sys.stdout.write(":")
	for m in range(20-pourv):
		sys.stdout.write(" ")
	sys.stdout.write("]")
	sys.stdout.flush()
	return

def cree_image(taille=600, c = 0, n_max = 200, alpha = 5, largeur = 4.2):
	# Déclaration de l'image
	image = Image.new('RGB', (taille, taille), (255, 255, 255))
	# Outil de dessin
	draw = ImageDraw.Draw(image)
	for k in range(taille):
		chargement(k, taille)
		for l in range(taille/2+1):
			u = ch_coord(k,l,taille, largeur)
			n = 0
			while abs(u) <= 2 and n < n_max:
				u = u*u + c
				n = n + 1
			col = couleur_pix(n, n_max, alpha)
			draw.point((k, l), fill=col)
			draw.point((taille-k,taille-l), fill=col)
	sys.stdout.write("\n")
	print("Image générée")
	return(image)

def all_in_one(taille, part_r, part_i):
	image = cree_image(taille=taille, c=complex(part_r, part_i))
	image.show()
	reponse = ""
	while (reponse != "o")and(reponse != "n"):
		reponse = raw_input("Voulez-vous sauvegarder l'image ? [O/n] : ")
	
	if reponse == "o":
		image.save('Image/julia_{}+i{}.png'.format(part_r,part_i))
		print("Image enregistrée\n")

	else:
		print("Image non enregistrée\n")
	
