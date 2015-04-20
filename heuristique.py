#!/usr/bin/python
# -*-coding:utf-8 -*-

"""
On cherche ici à obtenir des informations nous permettant de
savoir comment l'on doit faire avancer n_max lorsque l'on se 
rapproche de l'ensemble de mandelbrot
"""

from cmath import *
import matplotlib.pyplot as plt
import numpy as np

nb_points = 100

pos_1 	= complex(-0.620, -0.476)
pos_2	= complex(-0.616, -0.462)

dist	= abs(pos_1 - pos_2)

h = np.linspace(0,1,nb_points)
x = np.linspace(0,dist,nb_points)
y = np.zeros(nb_points)

plt.plot(x,x)
plt.show()

