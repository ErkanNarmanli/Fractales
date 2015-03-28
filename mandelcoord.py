#!/usr/bin/python
# -*-coding:utf-8 -*

from Tkinter import *
from PIL import Image, ImageTk
from libjulia import *

### Constantes
taille_img = 600
taille_miniature = 200
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
fenetre.geometry('{}x{}'.format(taille_img + taille_miniature + 20, taille_img + 10))
fenetre.title('Position sur le Mandelbrot')
### Images
image_fond = Image.open('Images/mandelbrot_coord.png') # Attention à utiliser la bonne image
image_fond = ImageTk.PhotoImage(image_fond)
miniature = cree_julia(taille = taille_miniature, n_max = 100, alpha = 3)
miniature = ImageTk.PhotoImage(miniature)
### Quelques frames pour la déco
frame_coords = Frame(fenetre, border = 2, relief = GROOVE)
frame_mini = Frame(fenetre, border = 2, relief = GROOVE)
### Canvas contenant l'image et la miniature
mandel = Canvas(fenetre, height = taille_img, width = taille_img)
mandel.create_image(taille_img/2, taille_img/2, image = image_fond)
mini_julia = Canvas(frame_mini, height = taille_miniature, width = taille_miniature)
mini_julia.create_image(taille_miniature/2, taille_miniature/2, image = miniature)
### Labels destinés à afficher les coordonnées
label_coord_x = Label(frame_coords, height = 2, width = taille_miniature, text = 'x : 0.0000')
label_coord_y = Label(frame_coords, height = 2, width = taille_miniature, text = 'y : 0.0000')
label_coord_mini = Label(frame_mini, width = taille_miniature, text = 'c = 0.0000 + 0.0000i')

### Gestion des événements
# Fonction affichant les coordonnées de la souris dans le label label_coord
def affiche_coord(event):
	x, y = get_coord(event.x, event.y)
	y = -y # Dans Tkinter, l'axes des ordonnées est orienté à l'envers
	label_coord_x['text'] = "x : {0:.4f}".format(x) # On tronque x et y à 4 digits
	label_coord_y['text'] = "y : {0:.4f}".format(y)
# On associe l'événement 'déplacement de la souris' à affiche_coord
mandel.bind('<Motion>', affiche_coord)
# Fonction qui crée un julia et l'affiche dans le label mini_julia
def affiche_julia(event):
	global miniature
	x, y = get_coord(event.x, event.y)
	y = -y # Même remarque que dans affiche_coord
	miniature = ImageTk.PhotoImage(cree_julia(taille = taille_miniature, \
			c = complex(x, y), n_max = 100, alpha = 3, largeur = 4.2))
	mini_julia.create_image(taille_miniature/2, taille_miniature/2, image = miniature)
	label_coord_mini['text'] = 'c = {x:.4f} + {y:.4f}i'.format(x = x, y = y)
	
# On associe l'événement 'clic de souris' à affiche_julia
mandel.bind('<Button-1>', affiche_julia)
### Disposition des widgets
mandel.pack(side = LEFT, fill = Y)
frame_coords.pack(side = TOP)
label_coord_x.pack(side = TOP)
label_coord_y.pack(side = TOP)
frame_mini.pack(side = TOP)
mini_julia.pack(side = TOP)
label_coord_mini.pack(side = TOP)
### Boucle principale
fenetre.mainloop()

