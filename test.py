#!/usr/bin/python
# -*-coding:utf-8 -*

from mp_film import *

dictionnaire = dict()
dictionnaire = {}

for i in range(200):
	dictionnaire[i] = complex(i/200*1.5+0.2,0)

launch_client(julia_dict = dictionnaire)
