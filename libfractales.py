#!/usr/bin/python
# -*-coding:utf-8 -*-

from sys import stdout

# Fonction qui aligne du texte à droite dans un espace de t_max caractères
def ecrire(chaine, t_max):
	l = len(chaine)
	for m in range(t_max - l):
		stdout.write(" ") 
	stdout.write(chaine)

# Affiche une barre de chargement
def chargement(k, taille):
	pourc = 100*k/float(taille)
	pourv = 20*pourc/100. #pourvingt, parce que j'ai envie
	pourc = int(pourc) + 1
	pourv = int(pourv) + 1
	stdout.write('\r')
	ecrire('{}% : '.format(pourc), 5)
	ecrire(str(k+1), len(str(taille)))
	stdout.write('/{} pix'.format(taille))
	stdout.write('   [')
	for m in range(pourv):
		stdout.write(':')
	for m in range(20 - pourv):
		stdout.write(' ')
	stdout.write(']')

# Détermine les coordonnées dans le plan complexe
# à partir des coordonnées dans l'image
def ch_coord(k, l, taille, largeur, centre):
	return(complex( \
		(float(k) - taille/2.)*largeur/float(taille) + centre, \
		(float(l) - taille/2.)*largeur/float(taille) \
		))

# Détermine la couleur du pixel en fonction du rang à partir
# duquel on sort du cercle de rayon 2
def couleur_pix(n, n_max, alpha = 5):
	if n == n_max:
		c = 0
	else:
		c = 20 + 235*((n_max - n)/float(n_max))**alpha
		c = int(c)
	return(c, c, c)

