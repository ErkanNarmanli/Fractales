#!/usr/bin/python
# -*-coding:utf-8 -*

from Tkinter import *
from PIL import Image, ImageTk

### Constantes
taille_img = 600
nb_decimales = 4

### Fonctions utiles

# Fonction indiquant les coordonnées d'un point dans le plan
# à partir des coordonnées de la souris sur l'image
def get_coord(k, l):
	i = k - 1 # Petit correction : tkinter n'est pas très précis
	j = l - 2 # idem
	x = ((i - taille_img/2.)*2.8)/taille_img - 0.7
	y = ((j - taille_img/2.)*2.8)/taille_img
	# Les constantes 2.8 et -0.7 sont respectivements les constantes
	# 'largeur' et 'centre' utilisées dans le script 'mandelbrot.py'
	return(x, y)

# Fonction qui fixe le nombre de décimales d'un float
# C'est peut-être un peu sale
def set_nb_dec(x, n):
	return(int(x*(10**n))/float(10**n))

### Fenêtre principale
fenetre = Tk()
fenetre.title('Position sur le Mandelbrot')
### Image
image_fond = Image.open('Images/mandelbrot_coord.png') # Attention à utiliser la bonne image
image_fond = ImageTk.PhotoImage(image_fond)
### Canvas contenant l'image
mandel = Canvas(fenetre, height = taille_img, width = taille_img)
mandel.create_image(taille_img/2, taille_img/2, image = image_fond)
### Label destiné à afficher les coordonnées
label_coord = Label(fenetre)
### Gestion des événements

# Fonction affichant les coordonnées de la souris dans le label label_coord
def affiche_coord(event):
	x, y = get_coord(event.x, event.y)
	x = set_nb_dec(x, nb_decimales)
	y = set_nb_dec(y, nb_decimales)
	y = -y # Dans Tkinter, l'axes des ordonnées est orienté à l'envers
	label_coord['text'] = 'position : x = {} ; y = {}'.format(x, y)
# On associe l'événement 'déplacement de la souris' à affiche_coord
mandel.bind('<Motion>', affiche_coord)

### Disposition des widgets
mandel.pack(side = TOP, fill = X)
label_coord.pack(side = TOP, fill = X)
### Boucle principale
fenetre.mainloop()
