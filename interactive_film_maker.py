#!/usr/bin/python
# -*- coding:utf-8 -*-

from Tkinter import *
from PIL import Image, ImageTk
from libmandel import cree_mandelbrot
from libjulia import cree_julia
from libfractales import ch_coord

	
##### Deux classes pour gérer la liste déroulant des segments 
class SegItem(Frame):

	""" Un item d'une SegList """

	def __init__(self, parent, seg_id, start_pt, end_pt, img_freq = 150, cnf = {}, **kw):
		""" Initialisation de l'objet """
		Frame.__init__(self, parent, cnf, **kw)
		self.seg_id = seg_id
		self.start_pt = start_pt
		self.end_pt = end_pt
		self.img_freq = IntVar()
		self.img_freq.set(str(img_freq))
		self.pts_label = Label(self, text = seg_format(start_pt, end_pt), bg = kw['bg'])
		self.img_freq_label = Label(self, text = 'Nb images/unité longueur :', bg = kw['bg'])
		self.img_freq_entry = Entry(self, textvariable = self.img_freq, width = 5)

	def __displaycontent__(self):
		""" Dispose correctement les widgets dans le frame de l'objet """
		self.pts_label.grid(row = 0, column = 0, columnspan = 2)
		self.img_freq_label.grid(row = 1, column = 0)
		self.img_freq_entry.grid(row = 1, column = 1)

	def pack(self, cnf = {}, **kw):
		""" On surcharge la méthode pack """
		self.__displaycontent__()
		Frame.pack(self, cnf, **kw)
	
	def grid(self, cnf = {}, **kw):
		""" On surcharge la méthode grid """
		self.__displaycontent__()
		Frame.grid(self, cnf, **kw)
		
# Le code est inspiré de http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame
# et légèrement adapté à nos besoins
class SegList(Frame):
	
	""" Liste avec scrollbar dont les items (segments) comportent des
	options spécifiques à interactive_film_maker """
	
	def __init__(self, parent, title = 'Liste des segments', cnf = {}, **kw):
		""" Initialisation de l'objet """
		Frame.__init__(self, parent, cnf, **kw)
		self.segs_list = []
		# Titre
		self.title_label = Label(self, text = title, pady = 3)
		# Bouton supprimer
		self.del_button = Button(self, text = 'Supprimer dernier')
		## Configuration de la scrollbar
		# On est obligés de passer par un canvas
		self.scrollbar = Scrollbar(self, orient = VERTICAL)
		self.canvas = Canvas(self, bd = 0, highlightthickness = 0, height = kw['height'], \
				yscrollcommand = self.scrollbar.set)
		self.scrollbar.config(command = self.canvas.yview)
		# Initialisation de la vue
		self.canvas.xview_moveto(0)
		self.canvas.yview_moveto(0)
		# Frame interieur sur le quel on poura faire agir le scroll
		self.innerframe = Frame(self.canvas, height = kw['height'])
		innerframe_id = self.canvas.create_window(0, 0, window = \
				self.innerframe, anchor = NW)
		# Disposition des widgets
		self.__displaycontent__()
	
		def _configure_innerframe(event):
			""" Mise à jour de la configuration de innerframe """
			# Update scrollbar
			size = (self.innerframe.winfo_reqwidth(), \
					self.innerframe.winfo_reqheight())
			self.canvas.config(scrollregion = "0 0 {} {}".format(size[0], size[1]))
		self.innerframe.bind('<Configure>', _configure_innerframe)

		def _configure_canvas(event):
			""" Mise à jour de la configuration du canvas """
			if self.innerframe.winfo_reqwidth() != self.canvas.winfo_width():
				# Update innerframe à la taille du canvas
				self.canvas.itemconfigure(innerframe_id, \
						width = self.canvas.winfo_width())
		self.canvas.bind('<Configure>', _configure_canvas)
	
	# On sépare cette tâche pour alléger __init__
	def __displaycontent__(self):
		""" Dispose correctement les widgets à l'intérieur de l'objet """
		self.title_label.pack(side = TOP, fill = X, expand = FALSE)
		self.del_button.pack(side = BOTTOM, fill = X, expand = FALSE)
		self.scrollbar.pack(side = RIGHT, fill = Y, expand = FALSE)
		self.canvas.pack(side = LEFT, fill = BOTH, expand = TRUE)


	def add_item(self, seg_id, start_pt, end_pt, img_freq= 150):
		""" Ajoute un segment à la liste """
		new_seg = SegItem(self.innerframe, seg_id, start_pt, end_pt, img_freq, bd = 1, \
				relief = GROOVE, bg = '#fafafa') 
		new_seg.pack(side = TOP, anchor = CENTER, padx = 5)
		self.segs_list.append(new_seg)
	
	def total_images(self):
		""" calcul le nombre total d'images de la seglist """
		total = 0
		for seg in self.segs_list:
			total += int(seg.img_freq.get()*abs(seg.start_pt - seg.end_pt))
		return total
	
##### Fonctions utiles
# Changement de coordonnées
def get_coord(k, l):
	""" Récupère les coordonnées dans le plan complexe d'un événement sur l'image """
	c = ch_coord(k, l, taille_image, mandel_largeur, mandel_centre)
	x = c.real
	y = -c.imag	# tkinter oriente l'axe des ordonnées à l'envers
	return(x, y)

# Formatage d'un couple de point pour l'affichage dans SegItem
def seg_format(pt1, pt2):
	""" Formate le couple de points (pt1, pt2) qui représente une segment
	pour l'affichage """
	# 5 digits partout
	string = ''
	if pt1.real >= 0:
		string += ' '
	string += '{0:.4f}'.format(pt1.real)
	if pt1.imag < 0:
		string += ' -{0:.4f}i'.format(-pt1.imag)
	else:
		string += ' +{0:.4f}i'.format(pt1.imag)
	string += '  ;  '
	if pt2.real >= 0:
		string += ' '
	string += '{0:.4f}'.format(pt2.real)
	if pt2.imag < 0:
		string += ' -{0:.4f}i'.format(-pt2.imag)
	else:
		string += ' +{0:.4f}i'.format(pt2.imag)
	return(string)

##### Variables globales
taille_image = 700
mandel_largeur = 2.8			# Correspond aux options par défaut de cree_mandel
mandel_centre = complex(-0.7, 0)	# idem, normalement on ne touche pas
fichier_image = 'fond_film_maker_{}px.png'.format(taille_image)
# Variable contenant la position du deernier clic de la souris
# Important pour tracer le chemin à parcourir
last_click = None

##### Fenêtre principale
fenetre = Tk()
fenetre.title('Julia Film Maker')

##### Image du mandelbrot
mandel = Canvas(fenetre, width = taille_image, height = taille_image)
try:
	image_fond = Image.open(fichier_image)
except IOError:		# Si l'image n'existe pas, on la génère
	image_fond = cree_mandelbrot(taille = taille_image)
	image_fond.save(fichier_image)
image_fond = ImageTk.PhotoImage(image_fond)
mandel.create_image(taille_image/2, taille_image/2, image = image_fond)
mandel.pack(side = LEFT, fill = Y)

##### Affichage des infos
# Les différents widgets et variables
info_frame = Frame(fenetre, border = 2, relief = GROOVE)
info_frame.pack(side = TOP, fill = X)
x_title_label = Label(info_frame, text = 'x : ')
x_title_label.grid(row = 0, column = 0, sticky = E)
x_value_label = Label(info_frame, text = '')
x_value_label.grid(row = 0, column = 1, sticky = W)
y_title_label = Label(info_frame, text = 'y : ')
y_title_label.grid(row = 1, column = 0, sticky = E)
y_value_label = Label(info_frame, text = '')
y_value_label.grid(row = 1, column = 1, sticky = W)
nbimgs_title_label = Label(info_frame, text = "Nombre d'images : ")
nbimgs_title_label.grid(row = 2, column = 0, sticky = E)
nbimgs_value_label = Label(info_frame, text = '')
nbimgs_value_label.grid(row = 2, column = 1, sticky = W)
# Fonction pour changer les valeurs des variables
def update_position(event):
	""" Affiche les coordonnées de l'événement dans les champs x et y """
	x, y = get_coord(event.x, event.y)
	x_value_label['text'] = '{0:.4f}'.format(x)	# 5 digits
	y_value_label['text'] = '{0:.4f}'.format(y)	# idem
# Au déplacement de la souris sur le Mandelbrot, on met à jours les coordonnées
mandel.bind('<Motion>', update_position)

##### Liste des segments parcourus
seglist = SegList(fenetre, title = 'Segments du chemin', border = 2, \
		relief = GROOVE, height = taille_image - 300)
seglist.pack(side = TOP, fill = X)

# Mise à jour du nombre d'images
def update_nbimgs():
	""" Met à jour le nombre d'image affiché dans le frame infos """
	new_total = seglist.total_images()
	nbimgs_value_label['text'] = str(new_total)

# Fonction pour ajouter un segment
def add_segment(event):
	""" Ajoute le segment reliant le dernier clic de la souris et le clic
	présent qui cause l'appel de la fonction.
	Au tout premier clic, on initialise juste la variable last_click """
	global last_click
	# Premier clic
	if last_click: 	# last_click est différent de None
		# Ajout du segment sur le canvas
		seg_id = mandel.create_line(last_click[0], last_click[1], event.x, event.y, fill = 'red')
		# Ajout du segment à seglist
		x, y = get_coord(last_click[0], last_click[1])
		start_pt = complex(x, y)
		x, y = get_coord(event.x, event.y)
		end_pt = complex(x, y)
		seglist.add_item(seg_id, start_pt, end_pt)
		# Mise à jour du nombre total d'images
		update_nbimgs()
	last_click = (event.x, event.y)

# Au clic de la souris sur le Mandelbrot, on appelle add_segment
mandel.bind('<Button-1>', add_segment)

# Fonction pour enlever un segment
def del_last_segment():
	""" Supprime le dernier segment de la liste du canvas contenant le Mandelbrot """
	if seglist.segs_list:	# La liste des segments n'est pas vide
		segitem = seglist.segs_list.pop()
		seg_id = segitem.seg_id
		segitem.pack_forget()
		del(segitem)
		mandel.delete(seg_id)
		# recalcul du nombre d'images
		update_nbimgs()

# On relie le bouton de suppression à del_last_segment
seglist.del_button['command'] = del_last_segment

##### Options d'enregistrement
save_frame = Frame(fenetre, border = 2, relief = GROOVE)
save_frame.pack(side = TOP, fill = X)
name_label = Label(save_frame, text = 'Nom : ')
name_label.grid(row = 0, column = 0, sticky = E)
save_name = StringVar()
name_entry = Entry(save_frame, textvariable = save_name)
name_entry.grid(row = 0, column = 1, sticky = W)
save_button = Button(save_frame, text = 'Sauvegarder')
save_button.grid(row = 1, column = 1, sticky = W)

##### Comme son nom l'indique, la mainloop
fenetre.mainloop()
