#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Déclaration des classes
"""

# Pour dire à python d'importer aussi depuis le répertoire parent
import sys
sys.path.append('../')


from Tkinter import *
from misc import *
from filmserver import runserver
from PIL import Image, ImageTk
from libmandel import cree_mandelbrot
from libjulia import cree_julia
import pickle



##### Une exception
class ImgFreqError(Exception):

	""" Exception soulevée lorsqu'on essaie de sauvegarder avec un champ img_freq mal rempli """

	def __init__(self, cause):
		""" Initialisation """
		Exception.__init__(self)
		self.cause = cause

	def __str__(self):
		""" Fonction appelée lorsqu'on veut afficher l'exception """
		return(self.cause)

##### Canvas contenant un Mandelbrot et affichant les segments
class MandelCanvas(Canvas):

	""" Classe affichant un mandelbrot cliquable et des segments """

	def __init__(self, parent, cnf = {}, **kw):
		""" Initialisation de l'objet """
		Canvas.__init__(self, parent, cnf, **kw)
		self.emphasized_seg = None
		# On charge l'image de fond (Mandelbrot)
		try:
			self.image_fond = Image.open(fichier_image)
		except IOError:		# Si l'image n'existe pas, on la génère
			self.image_fond = cree_mandelbrot(taille = taille_image, verbose = verbose)
			self.image_fond.save(fichier_image)
		self.image_fond = ImageTk.PhotoImage(self.image_fond)
		self.create_image(taille_image/2, taille_image/2, image = self.image_fond)
		# Curseur pour le tracé des segments
		self.last_click = None
		self.last_click_id = None
		# Fonction à appeler lors d'un clic sur le canvas
		self.call_whenclicked = None

	# Fonction appelée lors d'un clic sur le canvas
	def add_segment(self, x1, y1):
		""" Trace le segment allant de last_click au point (x, y) """
		if self.last_click: 		# last_click est différent de None
			x0, y0 = self.last_click
			# Ajout du segment
			seg_id = self.create_line(x0, y0, x1, y1, fill = 'red')
			# Déplacement du curseur
			self.coords(self.last_click_id, x1 - 3, y1 - 3, x1 + 3, y1 + 3)
			self.last_click = (x1, y1)
			return(seg_id, x0, y0)
		else:
			# Déplacement du curseur
			self.last_click_id = self.create_rectangle(\
					x1 - 3, y1 - 3, x1 + 3, y1 + 3, fill = 'red')
			self.last_click = (x1, y1)
			return(None, None, None)
		
	# Suppression d'un segment
	def del_segment(self, seg_id = None, x = None, y = None):
		""" Supprime le dernier segment """
		if seg_id:	# seg_id n'est pas None
			# Suppression du segment
			self.delete(seg_id)
			# Déplacement du curseur
			self.last_click = (x, y)
			self.coords(self.last_click_id, x - 3, y - 3, x + 3, y + 3)
			# Si le segment était mis en valeur, on remet emphasized_seg à zéro
			if seg_id == self.emphasized_seg:
				self.emphasized_seg = None
		elif self.last_click: 	# last_click existe encore
			# Remise à zéro du curseur
			self.last_click = None
			self.delete(self.last_click_id)
			self.last_click_id = None
		else:
			pass

	# Mise en valeur d'un segment
	def emph_seg(self, seg_id):
		""" Met en valeur le segment d'id seg_id """
		if self.emphasized_seg == seg_id: # On clique sur le même segment
			# On désactive la mise en valeur
			self.itemconfig(self.emphasized_seg, width = 1)
			self.emphasized_seg = None
		else:
			if self.emphasized_seg:	# Un autre segment était déjà mis en valeur
				# On désactive la mise en valeur de l'ancien segment
				self.itemconfig(self.emphasized_seg, width = 1)
			# On l'active pour le nouveau segment
			self.itemconfig(seg_id, width = 3)
			# On met la bonne valeur dans emphasized_seg
			self.emphasized_seg = seg_id
		

##### Widget affichant une miniature d'ensemble de Julia
class MiniJulia(Frame):

	""" Classe affichant un ensemble de Julia """

	def __init__(self, parent, cnf = {}, **kw):
		""" Initialisation de l'objet """
		Frame.__init__(self, parent, cnf, **kw)
		# Canvas contenant l'image
		self.canvas = Canvas(self, width = taille_miniature, height = taille_miniature)
		# Initialisation de l'image
		self.image = None
		self.set_new_julia(complex(0, 1))
		# Affichage du canvas
		self.canvas.pack(side = TOP)
	
	def set_new_julia(self, c):
		# Remise à zéro du canvas
		self.canvas.delete('all')
		# Image de Julia
		self.image = ImageTk.PhotoImage(cree_julia(taille = taille_miniature, c = c, verbose = verbose))
		self.canvas.create_image(taille_miniature/2, taille_miniature/2, image = self.image)
		# Légende
		title = 'Miniature'
		self.canvas.create_text(taille_miniature/2, 10, text = title)
		caption = 'c = ' + complex_format(c)
		self.canvas.create_text(taille_miniature/2, taille_miniature - 10, text = caption)


##### Widget affichant les infos utiles
class InfoFrame(Frame):

	""" Classe affichant les infos utiles de l'application """

	def __init__(self, parent, cnf = {}, **kw):
		""" Initialisation de l'objet """
		Frame.__init__(self, parent, cnf, **kw)
		# Coodronnées
		self.x_title_label = Label(self, text = 'x : ')
		self.x_value_label = Label(self, text = '')
		self.y_title_label = Label(self, text = 'y : ')
		self.y_value_label = Label(self, text = '')
		# Nombre total d'images
		self.nbimgs_title_label = Label(self, text = "Nombre d'images : ")
		self.nbimgs_value_label = Label(self, text = '')
		# Affichage du contenu
		self.__displaycontent__()
	
	# Tâche séparée pour alléger __init__
	def __displaycontent__(self):
		""" Dispose correctement les widgets dans le frame de l'objet """
		self.x_value_label.grid(row = 0, column = 1, sticky = W)
		self.x_title_label.grid(row = 0, column = 0, sticky = E)
		self.y_title_label.grid(row = 1, column = 0, sticky = E)
		self.y_value_label.grid(row = 1, column = 1, sticky = W)
		self.nbimgs_title_label.grid(row = 2, column = 0, sticky = E)
		self.nbimgs_value_label.grid(row = 2, column = 1, sticky = W)
	
	# Pour mettre à jour les coordonnées
	def update_position(self, event):
		""" Affiche les coordonnées de l'événement """
		x, y = get_coord(event.x, event.y)
		self.x_value_label['text'] = '{0:.4f}'.format(x)
		self.y_value_label['text'] = '{0:.4f}'.format(y)

	# Pour mettre à jour le nombre d'images
	def update_nbimgs(self, nbimgs):
		""" Affiche le nombre d'image provisoir """
		self.nbimgs_value_label['text'] = str(nbimgs)


##### Classe utile dans les SegLists déclarées plus bas 
class SegItem(Frame):

	""" Un item d'une SegList """

	def __init__(self, parent, seg_id, start_pt, end_pt, img_freq = 150, cnf = {}, **kw):
		""" Initialisation de l'objet """
		Frame.__init__(self, parent, cnf, **kw)
		# Un id c'est pratique
		self.seg_id = seg_id
		# Point de départ du segment
		self.start_pt = start_pt
		# Point d'arrivée du segment
		self.end_pt = end_pt	
		# Nombre d'image par unité de longueur (Pour la génération du film)
		self.img_freq = IntVar()	
		self.img_freq.set(str(img_freq))
		# Widgets affichant les infos ci dessus
		self.pts_label = Label(self, text = seg_format(start_pt, end_pt))
		self.img_freq_label = Label(self, text = 'Nb images/unité longueur :')
		self.img_freq_entry = Entry(self, textvariable = self.img_freq, width = 5)
		# Disposition des widgets
		self.__displaycontent__()
	
	# Tâche séparée pour alléger __init__
	def __displaycontent__(self):
		""" Dispose correctement les widgets dans le frame de l'objet """
		self.pts_label.grid(row = 0, column = 0, columnspan = 2)
		self.img_freq_label.grid(row = 1, column = 0)
		self.img_freq_entry.grid(row = 1, column = 1)
		self.set_bg(DEFAULT_SEG_COLOR)
	
	def set_bg(self, bgcolor):
		""" Définit la couleur de fond """
		self['bg'] = bgcolor
		self.pts_label['bg'] = bgcolor
		self.img_freq_label['bg'] = bgcolor

	# Relie la modification du champ img_freq à l'appel de f
	def set_wcallback(self, f):
		""" Définit la fonction à appliquer lorsque la variable img_freq est modifée """
		self.img_freq.trace('w', lambda name, index, mode, var = self.img_freq: f())
	
	
##### Liste avec scrollbar pour afficher les segments séléctionnés par l'utilisateur
# Le code est inspiré de http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame
# et légèrement adapté à nos besoins
class SegList(Frame):
	
	""" Liste avec scrollbar dont les items (segments) comportent des
	options spécifiques à interactive_film_maker """
	
	def __init__(self, parent, title = 'Liste des segments', cnf = {}, **kw):
		""" Initialisation de l'objet """
		Frame.__init__(self, parent, cnf, **kw)
		self.segs_list = []
		self.emphasized_item = None
		# Correspondances id/index pour des questions de performances
		# dict[id] = index
		self.id_index = {}
		# Titre
		self.title_label = Label(self, text = title, pady = 3, bd = 1, relief = GROOVE)
		# Boutons de suppressions
		self.del_button = Button(self, text = 'Supprimer dernier')
		self.delall_button = Button(self, text = 'Supprimer tout')
		## Configuration de la scrollbar
		# On est obligés de passer par un canvas
		self.scrollbar = Scrollbar(self, orient = VERTICAL)
		self.canvas = Canvas(self, bd = 0, highlightthickness = 0, \
				height = kw['height'], yscrollcommand = self.scrollbar.set)
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
			# Update la scrollbar
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
		self.delall_button.pack(side = BOTTOM, fill = X, expand = FALSE)
		self.del_button.pack(side = BOTTOM, fill = X, expand = FALSE)
		self.scrollbar.pack(side = RIGHT, fill = Y, expand = FALSE)
		self.canvas.pack(side = LEFT, fill = BOTH, expand = TRUE)
	
	def seg_by_id(self, seg_id):
		""" Renvoit un pointeur vers le segitem d'id seg_id """
		return (self.segs_list[self.id_index[seg_id]])

	# Fait toutes les initialisations nécessaires à l'ajout d'un item
	def add_item(self, seg_id, start_pt, end_pt, callback, img_freq = 150):
		""" Ajoute un segment à la liste """
		# Nouvel item
		new_seg = SegItem(self.innerframe, seg_id, start_pt, end_pt, img_freq, bd = 1, \
				relief = GROOVE)
		new_seg.pack(side = TOP, anchor = CENTER, padx = 5)
		self.segs_list.append(new_seg)
		self.id_index[new_seg.seg_id] = len(self.segs_list) - 1
		new_seg.set_wcallback(callback) # Fonction à appeler en cas de modification

	# Supprime le dernier item
	def del_last_item(self):
		""" Supprime le dernier item """
		if self.segs_list:	# la liste n'est pas vide
			# On récupère des infos pour la suppression du segment dans le canvas
			segitem = self.segs_list.pop()
			x, y = inv_get_coord(segitem.start_pt.real, segitem.start_pt.imag)
			seg_id = segitem.seg_id
			# Si l'item supprimé était mis en valeur, on remet emphasized_item à zéro
			if seg_id == self.emphasized_item:
				self.emphasized_item = None
			# Destruction du segitem
			del(self.id_index[segitem.seg_id])
			segitem.destroy()
			return(seg_id, x, y)	
		else:
			return(None, None, None)

	# Met en valeur un item
	def emph_item(self, seg_id):
		""" Met en valeur l'item d'id seg_id """
		if self.emphasized_item == seg_id:	# L'item était déjà en relief
			# On désactive la mise en valeur
			self.seg_by_id(seg_id).set_bg(DEFAULT_SEG_COLOR)
			self.emphasized_item = None
		else:
			if self.emphasized_item:	# Un autre item était déjà mis en valeur
				# On désactive la mise en valeur de l'ancien item
				self.seg_by_id(self.emphasized_item).set_bg(DEFAULT_SEG_COLOR)
			# On l'active pour le nouvel item
			self.seg_by_id(seg_id).set_bg(EMPH_SEG_COLOR)
			# On met la bonne valeur dans emphasized_item
			self.emphasized_item = seg_id
	
	# Calcule le nombre total d'images du film
	def total_images(self, err_msg = False):
		""" Calcul le nombre total d'images de la seglist.
		Si err_msg vaut True, un message d'erreur sera envoyé si un champ contient une valeur
		incorecte. Sinon, on ignore l'erreur et fixe la valeur à zéro
		"""
		# On calcul sum( |start_pt - end_pt|*img_freq ) en parcourrant les segitems
		total = 0
		for seg in self.segs_list:
			try:
				total += int(seg.img_freq.get()*abs(seg.start_pt - seg.end_pt))
			except ValueError:
				if err_msg:
					raise ImgFreqError('Un des champs "Nb images/unité de longueur" est mal rempli')
				else:
					pass
		return total

	# Sauvegarde de la SegList
	def save_list(self, path):
		""" Sauvegarde la liste des segments dans le fichier indiqué par path """
		with open(path, 'wb') as save_file:
			pickler = pickle.Pickler(save_file)
			for seg in self.segs_list:
				# Seules les données suivantes sont importantes
				pickler.dump((	seg.start_pt, \
						seg.end_pt,  \
						seg.img_freq.get() ))
	
	# Génère le film
	def make_film(self):
		""" Génère le film associé à la seglist """
		julia_dict = {}
		index = 0
		# Remplissage du dictionnaire
		for seg in self.segs_list:
			try:
				i_max = int(seg.img_freq.get()*abs(seg.start_pt - seg.end_pt))
				for i in xrange(i_max):
					index += 1
					julia_dict[index] = seg.start_pt + i*(seg.end_pt - seg.start_pt)/float(i_max)
			except ValueError:
				pass
		runserver(julia_dict, 'imgs', 800)
				


