#!/usr/bin/python
# -*-coding:utf-8 -*

from PIL import Image, ImageDraw, ImageFont
from math import sqrt
import time
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

# On initialise l'image
image = cree_image(taille=taille, c=c, n_max=n_max, alpha=alpha, largeur = largeur)

#Et on la sauvegarde
image.save('Images/julia_{}+i{}.png'.format(c.real,c.imag))
image.show()
