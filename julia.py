#!/usr/bin/python
# -*-coding:utf-8 -*

"""
Script interactif pour dessiner des ensembles des Julia
"""

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

# Procédure d'enregistrement
enregistre(image, 'julia_{}+i{}'.format(c.real, c.imag), 'Images')
