#!/usr/bin/python
# -*-coding:utf-8 -*

from libmandel import *

taille = 10000 

image = cree_mandelbrot_zoli(taille = taille, largeur = 3, couleur_fond = (20,20,20) , couleur_bord = (220, 220, 220), couleur_mandel = (5,5,5))

image = ameliore_bord(image, taille)
image.show()

enregistre(image, 'Mandel_zoli')
