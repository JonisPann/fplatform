import random, time, threading
from matplotlib import pyplot as plt
from scipy.stats import poisson
from natsort import natsorted
import numpy as np
from juyou_classes import *


class Juyou:

	avgArrInterv_hi = 600
	avgArrInterv_mi = 1200
	avgArrInterv_lo = 3600
	
	def __init__(self): #, name):
		# self.name = name
		self.zaiko_ini()
		self.oil = Abura()
		self.cost ,self.price, self.profit = 0, 0, 0
		self.ageki, self.hotters = [], []
		self.uretalist, self.haikilist = [], []
		self.num_ureta, self.num_haiki = {}, {}
		self.arrInterv_hi = poisson.rvs(mu = self.avgArrInterv_hi, size = 10000)
		self.arrInterv_mi = poisson.rvs(mu = self.avgArrInterv_mi, size = 10000)
		self.arrInterv_lo = poisson.rvs(mu = self.avgArrInterv_lo, size = 10000)
		self.peak = self.get_sec(peakhr)
		self.cold = self.get_sec(coldhr)
	
	def zaiko_ini(self):
		self.num_zaiko = {'famichiki': 100, 'spichiki': 100,
					'tsukune': 50, 'amedog': 50,
					'hash potato': 50, 'pokechiki': 50,
					'coroquette': 50}
	
	def tosecond(self, x):
		h, m, s = [int(y) for y in x.split(':')]
		return h * 3600 + m * 60 + s

	def get_sec(self, x):
		res = []
		for z in x:
			res.append((self.tosecond(z[0]), self.tosecond(z[1])))
		return res
	
	def list_ageki(self):
		return natsorted([x.name for x in self.ageki])
	
	def list_hotters(self):
		return natsorted([x.name for x in self.hotters])
	
	def count_ageki(self, item):
		return len([x for x in self.ageki if x.name == item])
	
	def count_hotters(self, item):
		return len([x for x in self.hotters if x.name == item])

	def ireru_ageki(self, item, t):
		if self.count_ageki(item) + 1 > youryou_ageki[item]:
			raise ValueError('frying machine full!')
		self.num_zaiko[item] -= 1
		self.oil.fry(item)
		agemon = Agemon(item, t, tyourijikan[item], tyourijikanmax[item], 
				  seizonjikan[item], genka[item], kakaku[item], aburasyoumou[item])
		self.ageki.append(agemon)
		self.cost += agemon.cost
	
	def ireru_hotters(self, toput):
		if self.count_hotters(toput.name) + 1 > youryou_hotters[toput.name]:
			raise ValueError('hotters full!')
		self.hotters.append(toput)
	
	def toru_ageki(self, totake):
		if len(self.ageki) == 0:
			ValueError('nothing in ageki!')
		self.ageki.remove(totake)
		return totake
	
	def idou(self, obj, t):
		# toru_ageki -> ireru_hotters
		if len(self.ageki) == 0:
			ValueError('nothing in ageki!')
		obj.ftime = t
		self.ageki.remove(obj)
		if self.count_hotters(obj.name) + 1 > youryou_hotters[obj.name]:
			print(obj.name, ' cannot be put into the hotters!')
			raise ValueError('hotters full!')
		self.hotters.append(obj)
	
	def toru_ureta(self, item):
		hot = self.list_hotters()
		if item not in hot:
			raise ValueError('not enough', item, 'on the hotters')
		idx = hot.index(item)
		self.uretalist.append(self.hotters[idx])
		self.num_ureta[item] += 1
		self.price += self.hotters[idx].price
		self.profit += self.hotters[idx].profit()
		# print('sold: ', item, ';', self.hotters[idx].id())
		del self.hotters[idx]
	
	def oisisa(self, item, t):
		accugrade, kosu, ref = 0, 0, []
		for z in self.hotters:
			if z.name == item:
				accugrade += z.oisisa(t)
				kosu += 1
				ref.append(int(z.oisisa(t)))
		print('time: ', t, ' item: ', item, 'deciousness: ', ref)
		return 0 if kosu == 0 else accugrade / kosu
	
	def haiki(self, obj):
		self.num_haiki[obj.name] += 1
		self.hotters.remove(obj)
	
	def raikyaku(self, t):
		t %= 86400
		if t == 0:
			return False
		idx = 0
		tt = t
		while t > 0:
			# t = t % 86400
			if any(tt >= x[0] and tt < x[1] for x in self.peak):
				t -= self.arrInterv_hi[idx]
			elif any(tt >= x[0] and tt < x[1] for x in self.cold):
				t -= self.arrInterv_lo[idx]
			else:
				t -= self.arrInterv_mi[idx]
			idx += 1
		if t == 0:
			return True
		return False
	
	def rireki(self):
		print('frying machine: ', self.ageki)
		print('hotters: ', self.hotters)
		# print('number sold:', self.num_ureta)
		# print('number disposed: ', self.num_haiki)

	def printsummary(self):
		print('numbers sold: ', self.num_ureta)
		print('numbers disposed: ', self.num_haiki)
		print('total cost: ', self.cost)
		print('total earning: ', self.price)
		print('total profit: ', self.price - self.cost)

