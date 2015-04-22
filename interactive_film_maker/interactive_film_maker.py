#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Application facilitant la création de films sur les ensembles de Julia
"""

# Pour dire à python d'importer aussi depuis le répertoire parent
import sys
sys.path.append('../')


from misc import *
from classes import *
from libmandel import cree_mandelbrot
from libjulia import cree_julia


##### Fenêtre principale
fenetre = Tk()
fenetre.title('Julia Film Maker')


##### Image du mandelbrot
mandel = MandelCanvas(fenetre, width = taille_image, height = taille_image)
mandel.pack(side = LEFT, fill = Y)


##### Affichage des infos
info_widget = InfoFrame(fenetre, border = 2, relief = GROOVE)
info_widget.pack(side = TOP, fill = X)

##### Liste des segments parcourus
seglist = SegList(fenetre, title = 'Segments du chemin', border = 2, \
		relief = GROOVE, height = taille_image - 200)
seglist.pack(side = TOP, fill = X)

##### Ajout d'un segment
def add_segment(event):
	""" Ajoute un segment sur le canvas et dans la seglist """
	seg_id, x0, y0 = mandel.add_segment(event.x, event.y)
	if seg_id:	# seg_id est différent de None
		# Ajout d'un item dans seglist
		end_pt = complex(*get_coord(event.x, event.y))
		start_pt = complex(*get_coord(x0, y0))
		f = lambda: info_widget.update_nbimgs(seglist.total_images())
		seglist.add_item(seg_id, start_pt, end_pt, f)
		# Mise à jour du nombre d'images
		f()

##### Suppression d'un segment
def del_last_segment():
	""" Supprime le dernier segment de la liste du canvas contenant le Mandelbrot """
	seg_id, x, y = seglist.del_last_item()
	mandel.del_segment(seg_id, x, y)
	nbimgs = seglist.total_images()
	info_widget.update_nbimgs(nbimgs)

##### Gestion des événements
mandel.bind('<Motion>', info_widget.update_position)
mandel.bind('<Button-1>', add_segment)
seglist.del_button['command'] = del_last_segment


##### La barre des menus
menubar = Menu(fenetre)

# Menu Fichier
filemenu = Menu(menubar)
filemenu.add_command(label = 'Ouvrir')
filemenu.add_command(label = 'Enregistrer')
filemenu.add_command(label = 'Quitter', command = fenetre.quit)
menubar.add_cascade(label = 'Fichier', menu = filemenu)

# Menu Aide
helpmenu = Menu(menubar)
helpmenu.add_command(label = "Mode d'emploi")
helpmenu.add_command(label = "À propos")
menubar.add_cascade(label = 'Aide', menu = helpmenu)

# On attache le menu à la fenêtre principale
fenetre['menu'] = menubar


##### Comme son nom l'indique, la mainloop
fenetre.mainloop()


