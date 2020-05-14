import random
from matplotlib import pyplot as plt

simutime = 86400

class Juyou:

	tyourijikanmin = 300 
	tyourijikanmax = 600
	ageki_youryou = 20
	hotters_youryou = 40
	karaagelife = 10800
	
	def __init__(self): #, name):
		# self.name = name

		self.num_zaiko = 100000
		self.ageki = []
		self.hotters = []
		self.num_ureta = 0
		self.num_haiki = 0
	
	def ireru_ageki(self, oid):
		if len(self.ageki) + 1 > self.ageki_youryou:
			raise ValueError('frying machine full!')
		self.num_zaiko -= 1
		self.ageki.append(oid)
		return oid
	
	def ireru_hotters(self, oid):
		if len(self.hotters) + 1 > self.hotters_youryou:
			raise ValueError('hotters full!')
		self.hotters.append(oid)

	def toru_ageki(self, oid):
		if len(self.ageki) == 0:
			ValueError('nothing in ageki!')
		self.ageki.remove(oid)

	def toru_ureta(self, n):
		if len(self.hotters) - n < 0:
			raise ValueError('not enough on hotters')
		ureta = self.hotters[:n]
		del self.hotters[:n]
		self.num_ureta += n
		return ureta

	def haiki(self, oid):
		self.num_haiki += 1
		self.hotters.remove(oid)
	
	def raikyaku(self, t):
		if t % random.randint(600, 800) == 599:
			return True
		return False

	def kau(self):
		return random.randint(0,3)

	def rireki(self):
		print('frying machine: ', self.ageki)
		print('hotters: ', self.hotters)
		print('number sold:', self.num_ureta)
		print('number disposed: ', self.num_haiki)


md = Juyou()
ageki, hotters = [], []
for t in range(simutime):
	print('----------------------------------------------------------------')
	print('timestamp: ', t)
	if md.raikyaku(t):
		n = md.kau()
		ureta = md.toru_ureta(n)
		print('sold: ', ureta)
	elif len(md.hotters) < 12 and len(md.ageki) + len(md.hotters) < md.hotters_youryou and len(md.ageki)+1 <= md.ageki_youryou:
		md.ireru_ageki(t)
		print('fry: ', t)
	else:
		for z in md.ageki:
			if t - z > md.tyourijikanmin and t-z <= md.tyourijikanmax:
				md.toru_ageki(z)
				md.ireru_hotters(z)
				print('move ', z, ' from frying to hotters')
				break
			elif t - z > md.tyourijikanmax:
				md.toru_ageki(z)
				print('dispose', z, ' from the frying machine')
				break
		for z in md.hotters:
			if t - z > md.karaagelife:
				md.haiki(z)
				print('dispose: ', z)
				break
	ageki.append(len(md.ageki))
	hotters.append(len(md.hotters))
	md.rireki()

plt.plot(ageki)
plt.show()
