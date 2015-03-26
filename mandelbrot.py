#!/usr/bin/python
# -*-coding:utf-8 -*

from PIL import Image, ImageDraw, ImageFont
import sys
from cmath import *

# Constantes
centre = -0.7 	# -0.7
try:
	taille = int(sys.argv[1])
except:
	taille = 600 	# 700
largeur = 2.8	# 2.8
n_max = 200	# 200
alpha = 5	# 5
# Image
image = Image.new('RGB', (taille, taille), (255, 255, 255))
# Outil de dessin
draw = ImageDraw.Draw(image)

# Fonction qui aligne du texte à droite dans un espace de t_max caractères
def ecrire(chaine,t_max):
	for m in range(t_max-len(chaine)):
		sys.stdout.write(" ")
	sys.stdout.write(chaine)

# Affiche une barre de chargement
def chargement(k):
	pourc = 100*k/float(taille)
	pourv = 20*pourc/100.  #pourvingt, parce que j'ai envie
	pourc = int(pourc)+1
	pourv = int(pourv)+1
	sys.stdout.write("\r")
	ecrire("{}%%:".format(pourc),5)
	ecrire(str(k+1),len(str(taille)))
	sys.stdout.write("{} pix".format(taille))
	sys.stdout.write("   [")
	for m in range(pourv):
		sys.stdout.write(":")
	for m in range(20-pourv):
		sys.stdout.write(" ")
	sys.stdout.write("]")
	sys.stdout.flush()
	return

# Détermine les coordonnées dans le plan complexe
# à partir des coordonnées dans l'image
def ch_coord(k, l):
	return(complex( \
		(float(k) - taille/2.)*largeur/float(taille) + centre, \
		(float(l) - taille/2.)*largeur/float(taille) \
		))

# Détermine la couleur du pixel en fonction du rang à partir
# duquel on sort du cercle de rayon 2
def couleur_pix(n):
	if n == n_max:
		c = 0
	else:
		c = 20 + 235*((n_max - n)/float(n_max))**alpha
		c = int(c)
	return(c, c, c)

# Parcours
for k in range(taille):
	chargement(k)
	for l in range(taille/2+1):
		u = complex(0,0)
		c = ch_coord(k, l)
		n = 0
		# Si on est dans la cardioïde, on ne fait pas les tests
		if 2*abs(c-0.25) < (1 - cos(phase(c-0.25))).real:
			col = (0,0,0)
		else:
			while abs(u) <= 2 and n < n_max:
				u = u*u + c
				n = n + 1
			col = couleur_pix(n)
		draw.point((k, l), fill=col)
		draw.point((k, taille-l), fill=col) # On utilise l'invariance par conjugaison
sys.stdout.write("\n")

# Sauvegarde de l'image
image.save('Images/mandelbrot_{}px.png'.format(taille))

