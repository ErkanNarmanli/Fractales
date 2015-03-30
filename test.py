#!/usr/bin/python
# -*-coding:utf-8 -*

from libmandel import *

taille = 1000 

image = cree_mandelbrot_zoli(taille = taille, couleur_fond = (16,27,37) , couleur_bord = (94, 40, 0))
image = ameliore_bord(image, taille)
image.show()

enregistre(image, 'Mandel_zoli')
