import random, time
from names_dataset import NameDataset
from natsort import natsorted
import numpy as np
from juyou_params import *

NDB = NameDataset()
FNAMES, LNAMES = list(NDB.first_names), list(NDB.last_names)

class Agemon:

	def __init__(self, name, ctime,
			  cooktime, cooktimemax, lifetime,
			  cost, price, oilabrasion):
		self.name, self.lifetime = name, lifetime
		self.cooktime, self.cooktimemax = cooktime, cooktimemax
		self.cost, self.price, self.oilabrasion = cost, price, oilabrasion
		self.ctime = ctime # time.time()
		self.cooked = False
		self.ftime = 0 # timestamp of leaving oil
	
	def id(self):
		return str(self.ctime)
	
	def profit(self):
		return self.price - self.cost
	
	def imamade(self, t):
		return t - self.ftime
	
	def rotten(self, t):
		return True if self.imamade(t) >= self.lifetime else False
	
	def oisisa(self, t):
		res = 100. - 100. * float(self.imamade(t)/self.lifetime)
		return 0 if res < 0 else res
	
	def overcooked(self, t):
		return True if self.imamade(t) >= self.cooktimemax else False
	
	def undercooked(self, t):
		return True if self.imamade(t) < self.cooktime else False

class Abura:

	def __init__(self, hp = 150):
		self.fullhp = hp
		self.hp = hp
		self.itime = time.time()
		self.changing = False
	
	def id(self):
		return str(self.itime)
	
	def fry(self, item):
		self.hp -= aburasyoumou[item]
	
	def hp_ini(self):
		self.hp = self.fullhp
	
	def koukansubeki(self):
		return True if self.hp < 20 else False

class Staff:

	def __init__(self, name, 
			  time_putin = 2, time_takeout = 2, time_tohotters = 5, 
			  time_packing = 10, time_regi = 30, time_changeoil = 5400):
		self.name = name
		self.time_putin, self.time_takeout = time_putin, time_takeout
		self.time_tohotters = time_tohotters
		self.time_packing, self.time_regi = time_packing, time_regi
		self.time_changeoil = time_changeoil
		self.busy = False

class Customer:

	def __init__(self):
		self.name = random.choice(FNAMES) + ' ' + random.choice(LNAMES)
		self.login = time.time()
		self.logout = None
		self.tobuy = None
	
	def kau(self, t):
		# 'famichiki', 'spichiki', 'tsukune', 'amedog', 'hash potato', 'pokechiki', 'coroquette'
		t %= 86400
		# kosu = int(np.random.choice([0, 1, 2, 3, 4, 5], 1, p = [.20, .50, .15, .05, .05, .05]))
		kosu = int(np.random.choice([1, 2, 3, 4, 5], 1, p = [.60, .20, .10, .05, .05]))
		# kosu = int(np.random.choice([1, 2, 3, 4, 5], 1, p = [.70, .25, .03, .01, .01]))
		if t < 43200:
			self.tobuy = np.random.choice(items, kosu, p = [.30, .30, .08, .08, .08, .08, .08])
		else:
			self.tobuy = np.random.choice(items, kosu, p = [.25, .25, .10, .10, .10, .10, .10])
		return natsorted(list(self.tobuy))

