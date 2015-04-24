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
import tkFileDialog
import tkMessageBox

##### Classe de l'application
class InteractiveFilmMaker(Tk):

	""" L'application elle même """

	def __init__(self):
		""" Initialisation """
		Tk.__init__(self)
		# Titre
		self.title('Julia Film Maker')
		# Image du mandelbrot
		self.mandel = MandelCanvas(self, width = taille_image, height = taille_image)
		# Miniature d'ensemble de Julia
		self.minijulia = MiniJulia(self, border = 2, relief = GROOVE)
		# Affichage des infos
		self.info_widget = InfoFrame(self, border = 2, relief = GROOVE)
		# Liste des segments parcourus
		seglist_height = taille_image - taille_miniature - 170
		self.seglist = SegList(self, title = 'Segments du chemin', border = 2, \
				relief = GROOVE, height = seglist_height)
		# Gestion des événements
		self.__init_events__()
		# Barre des menus
		self.__init_menubar__()
		# Affichage des widgets
		self.__displaycontent__()
		
	# Affiche les widgets
	def __displaycontent__(self):
		""" Dispose correctement les widgets dans le fenêtre """
		self.mandel.pack(side = LEFT, fill = Y)
		self.minijulia.pack(side = TOP, fill = X)
		self.info_widget.pack(side = TOP, fill = X)
		self.seglist.pack(side = TOP, fill = X)
	
	# Barre des menus
	def __init_menubar__(self):
		""" Initialise la barre des menus """
		# barre des menus
		menubar = Menu(self)
		# Menu 'Fichier'
		filemenu = Menu(menubar)
		filemenu.add_command(label = 'Ouvrir', command = self.load_seglist, \
				accelerator = 'Ctrl+o')
		filemenu.add_command(label = 'Enregistrer', command = self.save_seglist, \
				accelerator = 'Ctrl+s')
		filemenu.add_command(label = 'Quitter', command = self.quit, \
				accelerator = 'Ctrl+q')
		menubar.add_cascade(label = 'Fichier', menu = filemenu)
		# Menu 'Édition'
		editmenu = Menu(menubar)
		editmenu.add_command(label = 'Supprimer dernier', command = self.del_last_segment, \
				accelerator = 'Ctrl+d')
		editmenu.add_command(label = 'Supprimer tout', command = self.del_all_segments, \
				accelerator = 'Ctrl+Shift+d')
		menubar.add_cascade(label = 'Édition', menu = editmenu)
		# Menu Aide
		helpmenu = Menu(menubar)
		helpmenu.add_command(label = "Mode d'emploi")
		helpmenu.add_command(label = "À propos")
		menubar.add_cascade(label = 'Aide', menu = helpmenu)
		# On attache le menu à la fenêtre principale
		self['menu'] = menubar

	# Gestion des événements
	def __init_events__(self):
		""" Définit le déclenchement des événements """
		# Chargement/sauvegarde
		self.bind_all('<Control-o>', lambda event: self.load_seglist())
		self.bind_all('<Control-s>', lambda event: self.save_seglist())
		# Quitter l'application
		self.bind_all('<Control-q>', lambda event: self.quit())
		# Affichage des coordonnées de la souris
		self.mandel.bind('<Motion>', self.info_widget.update_position)
		# Ajout d'un segment au clic de la souris
		self.mandel.bind('<Button-1>', self.add_segment)
		# Affichage d'un ensemble de Julia au clic-droit
		self.mandel.bind('<Button-2>', lambda event: self.minijulia.set_new_julia( \
				complex(*get_coord(event.x, event.y))))
		# Boutons de suppression
		self.seglist.del_button['command'] = self.del_last_segment
		self.bind_all('<Control-d>', lambda event: self.del_last_segment())
		self.seglist.delall_button['command'] = self.del_all_segments
		self.bind_all('<Control-Shift-d>', lambda event: self.del_all_segments())
		

	# Ajout manuel d'un segment
	def __add_segment_man__(self, x, y):
		""" Ajout un segment sur le canvas et dans la seglist """
		# Ajout d'un segment au canvas
		seg_id, x0, y0 = self.mandel.add_segment(x, y)
		if seg_id:	# seg_id est différent de None
			# Ajout d'un item dans seglist
			end_pt = complex(*get_coord(x, y))
			start_pt = complex(*get_coord(x0, y0))
			f = lambda: self.info_widget.update_nbimgs(self.seglist.total_images())
			self.seglist.add_item(seg_id, start_pt, end_pt, f)
			# Mise à jour du nombre d'images
			f()

	# Ajout d'un segment
	def add_segment(self, event):
		""" Ajoute un segment sur le canvas et dans la seglist à partir d'un event """
		self.__add_segment_man__(event.x, event.y)

	# Suppression d'un segment
	def del_last_segment(self):
		""" Supprime le dernier segment de la liste du canvas contenant le Mandelbrot """
		# Appel des méthodes de suppression de la seglist et du canvas
		seg_id, x, y = self.seglist.del_last_item()
		self.mandel.del_segment(seg_id, x, y)
		# Mise à jour du nombre total d'images
		nbimgs = self.seglist.total_images()
		self.info_widget.update_nbimgs(nbimgs)
	
	# Supprime tous les segments
	def del_all_segments(self):
		""" Supprime tous les segments """
		nbseg = len(self.seglist.segs_list) 
		for i in xrange(nbseg + 1):
			self.del_last_segment()

	# Enregistrement de la seglist
	def save_seglist(self):
		""" enregistre la seglist """
		path = tkFileDialog.asksaveasfilename( \
				title = 'Enregistrer', \
				filetypes = [("Liste de segments", "*.seglist")], \
				defaultextension = ".seglist", \
				parent = self)
		if len(path) > 0:	# path n'est pas une chaine vide
			self.seglist.save_list(path)
	
	# Chargement d'une seglist
	def load_seglist(self):
		""" Charge la seglist indiquée par path """
		if self.seglist.segs_list:	# La liste des segments n'est pas vide
			b = tkMessageBox.askokcancel('Liste non vide', 'La liste actuelle est non vide, elle sera perdue')
			if not b:
				return
			else:
				self.del_all_segments()
		path = tkFileDialog.askopenfilename( \
				title = 'Ouvrir', \
				filetypes = [("Liste de segments", "*.seglist")], \
				defaultextension = ".seglist", \
				parent = self)
		if len(path) > 0:	# path n'est pas une chaîne vide
			with open(path, 'rb') as save_file:
				unpickler = pickle.Unpickler(save_file)
				fst_seg = True
				while True:
					try:
						start_pt, end_pt, img_freq = unpickler.load()
						if fst_seg:
							x0, y0 = inv_get_coord(start_pt.real, start_pt.imag)
							self.__add_segment_man__(x0, y0)
							fst_seg = False
						x, y = inv_get_coord(end_pt.real, end_pt.imag)
						self.__add_segment_man__(x, y)
					except EOFError:
						break


# Lancement de l'application
App = InteractiveFilmMaker()
App.mainloop()


