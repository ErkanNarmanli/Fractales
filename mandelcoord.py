#!/usr/bin/python
# -*-coding:utf-8 -*

"""
Outil interactif avec interface graphique pour obtenir les coordonnées d'un point précis
et avoir des apperçus d'ensembles de Julia
"""

from Tkinter import *
import tkMessageBox
from PIL import Image, ImageTk
from libjulia import *

### Constantes
taille_img = 600
taille_miniature = 200
nb_decimales = 4

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


### Fenêtre principale
fenetre = Tk()
fenetre.geometry('{}x{}'.format(taille_img + taille_miniature + 40, taille_img + 10))
fenetre.title('Position sur le Mandelbrot')
### Fin fenêtre principale

### Mandelbrot
image_fond = Image.open('Images/mandelbrot_coord.png') # Attention utiliser la bonne image
image_fond = ImageTk.PhotoImage(image_fond)
mandel = Canvas(fenetre, height = taille_img, width = taille_img)
mandel.create_image(taille_img/2, taille_img/2, image = image_fond)
### Fin Mandelbrot

### Coordonnées de la souris
# Widgets
frame_coords = Frame(fenetre, border = 2, relief = GROOVE)
label_coord_x = Label(frame_coords, height = 1, text = 'x : 0.0000')
label_coord_y = Label(frame_coords, height = 1, text = 'y : 0.0000')
# Fonction affichant les coordonnées de la souris
def affiche_coord(event):
	x, y = get_coord(event.x, event.y)
	y = -y # Dans Tkinter, l'axes des ordonnées est orienté à l'envers
	label_coord_x['text'] = "x : {0:.4f}".format(x) # On tronque x et y à 4 digits
	label_coord_y['text'] = "y : {0:.4f}".format(y)
# On relie l'événement 'mouse motion' à la fonction d'affichage
mandel.bind('<Motion>', affiche_coord)
### Fin coordonnées de la souris

### Miniature de Julia
# Variables et widgets
frame_mini = Frame(fenetre, border = 2, relief = GROOVE)
miniature = cree_julia(taille = taille_miniature, n_max = 100, alpha = 3)
miniature = ImageTk.PhotoImage(miniature)
mini_julia = Canvas(frame_mini, height = taille_miniature, width = taille_miniature)
mini_julia.create_image(taille_miniature/2, taille_miniature/2, image = miniature)
label_coord_mini = Label(frame_mini, text = 'c = 0.0000 + 0.0000i')
### Fin miniature de Julia

### Grand Julia
# Variables et widgets
frame_grand_julia = Frame(fenetre, border = 2, relief = GROOVE)
var_choix_x = StringVar(value = '0')
var_choix_y = StringVar(value = '0')
var_choix_taille = StringVar(value = '700')
choix_x = Entry(frame_grand_julia, textvariable = var_choix_x)
choix_y = Entry(frame_grand_julia, textvariable = var_choix_y)
choix_taille = Entry(frame_grand_julia, textvariable = var_choix_taille)
bouton_julia = Button(frame_grand_julia, text = 'Générer')
label_choix_x = Label(frame_grand_julia, height = 1, text = 'x : ')
label_choix_y = Label(frame_grand_julia, height = 1, text = 'y : ')
label_choix_taille = Label(frame_grand_julia, height = 1, text = 'taille : ')
# Fonction affichant un grand ensemble de julia avec les paramètres fournis par l'utilisateur
def affiche_grand_julia():
	try:
		taille = int(var_choix_taille.get())
		c = complex(float(var_choix_x.get()), float(var_choix_y.get()))
		image = cree_julia(taille = taille, c = c)
		image.show()
		answer = tkMessageBox.askquestion('Sauvegarde', "Sauvegarder l'image ?")
		if answer == 'yes':
			name = 'Images/julia_{}+i{}_{}px.png'.format(c.real, c.imag, taille)
			print("{} saved".format(name))
			image.save(name)
		else:
			pass
	except:		# Si les arguments passés ne sont pas corrects, on ne fait rien
		pass
# On associe le bouton générer à la fonction affiche_grand_julia
bouton_julia['command'] = affiche_grand_julia
# Fonction qui crée un julia et l'affiche dans le label mini_julia
def affiche_julia(event):
	global miniature, gd_julia_utd
	x, y = get_coord(event.x, event.y)
	y = -y # Dans Tkinter, l'axes des ordonnées est orienté à l'envers
	miniature = ImageTk.PhotoImage(cree_julia(taille = taille_miniature, \
			c = complex(x, y), n_max = 100, alpha = 3, largeur = 4.2))
	mini_julia.create_image(taille_miniature/2, taille_miniature/2, image = miniature)
	label_coord_mini['text'] = 'c = {x:.4f} + {y:.4f}i'.format(x = x, y = y)
	var_choix_x.set(str(x))
	var_choix_y.set(str(y))
	gd_julia_utd = False
# On associe l'événement 'clic de souris' à affiche_julia
mandel.bind('<Button-1>', affiche_julia)
### Fin grand Julia

### Disposition des widgets
mandel.pack(side = LEFT, fill = Y)
frame_coords.pack(side = TOP, fill = X)
label_coord_x.pack(side = TOP)
label_coord_y.pack(side = TOP)
frame_mini.pack(side = TOP, fill = X)
mini_julia.pack(side = TOP)
label_coord_mini.pack(side = TOP)
frame_grand_julia.pack(side = TOP, fill = X)
label_choix_x.grid(row = 0, column = 0, sticky = E)
label_choix_y.grid(row = 1, column = 0, sticky = E)
label_choix_taille.grid(row = 2, column = 0, sticky = E)
choix_x.grid(row = 0, column = 1)
choix_y.grid(row = 1, column = 1)
choix_taille.grid(row = 2, column = 1)
bouton_julia.grid(row = 3, column = 0, columnspan = 2)
### Fin disposition des widgets

### Boucle principale
fenetre.mainloop()

