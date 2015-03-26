#!/usr/bin/python
# -*-coding:utf-8 -*

from PIL import Image, ImageDraw, ImageFont
from math import sqrt
import time
import sys

# Constantes
cote = int(input("Taille en pixel : "))
largeur = 4.4
n_max = 200
alpha = 5
part_r = float(input("Partie réelle : "))
part_i = float(input("Partie imaginaire : "))
c = complex(part_r,part_i)
# Image
image = Image.new('RGB', (cote, cote), (255, 255, 255))
# Outil de dessin
draw = ImageDraw.Draw(image)

# Détermine les coordonnées dans le plan complexe
# à partir des coordonnées dans l'image
def ch_coord(k, l):
	return(complex( \
		(k - cote/2.)*largeur/float(cote), \
		(l - cote/2.)*largeur/float(cote) \
		))

# Détermine la couleur du pixel en fonction du rang à partir
# duquel on sort du cercle de rayon 2
def couleur_pix(n):
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

def chargement(k):
	pourc = 100*k/float(cote)
	pourv = 20*pourc/100.  #pourvingt, parce que j'ai envie
	pourc = int(pourc)+1
	pourv = int(pourv)+1
	sys.stdout.write("\r")
	ecrire("%d%%:" % pourc,5)
	ecrire("%d"  % (k+1),len("%d" % cote))
	sys.stdout.write("/%d pix" % cote)
	sys.stdout.write("   [")
	for m in range(pourv):
		sys.stdout.write(":")
	for m in range(20-pourv):
		sys.stdout.write(" ")
	sys.stdout.write("]")
	sys.stdout.flush()
	return

for k in range(cote):
	chargement(k)
	for l in range(cote/2+1):
		u = ch_coord(k,l)
		n = 0
		while abs(u) <= 2 and n < n_max:
			u = u*u + c
			n = n + 1
		draw.point((k, l), fill=couleur_pix(n))
		draw.point((cote-k,cote-l), fill=couleur_pix(n))
sys.stdout.write("\n")

image.save('julia_{}+i{}.png'.format(c.real,c.imag))

