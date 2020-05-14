import random, time, threading
from matplotlib import pyplot as plt
from scipy.stats import poisson
from natsort import natsorted
import numpy as np
from juyou_classes import *
from juyou import *


# md = Juyou()
# ageki, hotters, zaiko = {}, {}, {}
# cost, price, profit = [], [], []
irassyai = []
aburahp = []
agequeue = {}
# thresL, thresH = 20, 100
plotlog = True
yoMoveIt = True
testtimes = 0

shiraki = Staff('Shiraki')
yano = Staff('Yano')
tajima = Staff('Tajima')
# thresSets = [(x,y) for x in range(0,101,5) for y in range(0,101,5) if x < y and x >= 20]
# thresSets = [(x,y) for x in range(0,101,5) for y in range(0,101,5) if x < y and y >= 20 and (y-x) > 10]
# thresSets = [(20,y) for y in range(0,101,5) if 20 < y and y >= 20 and (y-20) > 10]
thresSets = [(30, 80)]

def tovtime(t):
	day_shift = int(t / 86400)
	day = '2020' + '-' + '04' + '-' + str(day_shift + 1)
	t %= 86400
	return day + ' ' + str(int(t/3600)) + ':' + str(int((t%3600)/60)) + ':' + str(int((t%3600)%60))

# if __name__ == '__main__':
for thresL, thresH in thresSets:
	md = Juyou()
	cost, price, profit = [], [], []
	ageki, hotters, zaiko, deli = {}, {}, {}, {}
	testtimes += 1
	zannen = 0
	ts = time.time()
	np.random.seed(19880419)
	# np.random.seed(int(time.time()))
	agekiUsing = False
	for item in items:
		md.num_ureta[item] = 0
		md.num_haiki[item] = 0
		ageki[item], hotters[item], zaiko[item], deli[item] = [], [], [], []
		agequeue[item] = 0

	secToPass = 0
	koukankanryou = -1
	for t in range(simutime):
		# print('----------------------------------------------------------------')
		# print('timestamp: ', tovtime(t))

		# kosu log
		# print('ageki: ', md.list_ageki())
		# print('hotters: ', md.list_hotters())
		cost.append(md.cost)
		price.append(md.price)
		profit.append(md.price - md.cost)
		
		if yoMoveIt:
			# thL = thresL-100 if any(t%86400 >= (x[0]-1800) and t%86400 < (x[1]-1800) for x in md.cold) else thresL
			# thH = thresH-20 if any(t%86400 >= (x[0]-1800) and t%86400 < (x[1]-1800) for x in md.cold) else thresH
			thL = 0 if any(t%86400 >= (x[0]-1800) and t%86400 < (x[1]-1800) for x in md.cold) else thresL
			thH = 10 if any(t%86400 >= (x[0]-1800) and t%86400 < (x[1]-1800) for x in md.cold) else thresH
			thL = thresL+20 if any(t%86400 >= (x[0]-1200) and t%86400 < (x[1]-1200) for x in md.peak) else thresL
			thH = thresH+40 if any(t%86400 >= (x[0]-1200) and t%86400 < (x[1]-1200) for x in md.peak) else thresH
			thL = 0 if thL < 0 else thL
			thH = 100 if thH > 100 else thH
		else:
			thL = thresL
			thH = thresH

		if t % 86400 == 0:
			md.zaiko_ini()

		if len(md.list_ageki()) == 0:
			agekiUsing = False
		
		# log of aburahp, ageki, hotters, zaiko
		aburahp.append(md.oil.hp)
		for item in items:
			ageki[item].append(md.count_ageki(item))
			hotters[item].append(md.count_hotters(item))
			zaiko[item].append(md.num_zaiko[item])
			deli[item].append(md.oisisa(item, t))

		if t == koukankanryou:
			md.oil.changing = False
			koukankanryou = -1
			# print(tovtime(t), ',', 'OIL_CHANGE_FINISH')

		if secToPass != 0:
			# print('action being taken...')
			secToPass -= 1
			continue
		
		if md.raikyaku(t):
			kyaku = Customer()
			# print(kyaku.name, ' comes.')
			# irassyai.append(t)
			tobuy = kyaku.kau(t)
			# print('Wanna buy: ', tobuy)
			for z in tobuy:
				try:
					md.toru_ureta(z)
					secToPass += shiraki.time_packing
					# print(tovtime(t), ',', 'SOLD', ',', z)
				except:
					# print(z, ' is sold out now!')
					# print(tovtime(t), z, 'zannen')
					zannen += 1
					continue
			secToPass += shiraki.time_regi

		else:
			# check if the oil has to be changed
			if md.oil.koukansubeki():
				md.oil.changing = True
				koukankanryou = t + tajima.time_changeoil
				md.oil.hp_ini()
				# print('now: ', t, ' change finished at: ', koukankanryou)
				# print(tovtime(t), ',', 'OIL_CHANGE_START')

			# check hotters, if rotten dispose
			for z in md.hotters:
				if z.rotten(t):
					# print('dispose: ', z.name, ' ; ', z.ctime)
					# print(tovtime(t), ',', 'DISPOSE', ',', z.name)
					md.haiki(z)
					secToPass += yano.time_takeout
					break
			if secToPass != 0:
				continue

			# check hotters, if not enough fry
			if not md.oil.changing and not agekiUsing:
				for item in items:
					kosuh, kosua = md.count_hotters(item), md.count_ageki(item)
					limh, lima = youryou_hotters[item], youryou_ageki[item]
					
					if (kosuh <= limh * (thL/100) or agequeue[item] != 0) and md.count_ageki(item) == 0:
						agekosu = agequeue[item] if agequeue[item] != 0 else int(limh * thH/100) - kosuh
						if agekosu > youryou_ageki[item]:
							agequeue[item] = agekosu - youryou_ageki[item]
							agekosu = youryou_ageki[item]
						else:
							agequeue[item] = 0
						for i in range(agekosu):
							aget = t + i * tajima.time_putin
							md.ireru_ageki(item, aget)
							agekiUsing = True
							# print('fry: ', item, '; ', aget)
							# print(tovtime(t), ',', 'COOK_START', ',', item)
						secToPass += agekosu * tajima.time_putin
						break
					
			if secToPass != 0:
				continue

			# check ageki, if finished cooking move to hotters
			for z in md.ageki:
				if (t - z.ctime) > z.cooktime:
					md.idou(z, t)
					# print('move: ', z.name, ' ; ', z.ctime)
					# print(tovtime(t), ',', 'COOK_FINISH', ',', z.name)
					secToPass += tajima.time_takeout
					# break
			if secToPass != 0:
				continue
	
	# x = np.asarray([y for y in range(len())])
	
	# md.printsummary()
	toprint = str(testtimes) + ','
	toprint += str(thresL) 
	toprint += ','
	toprint += str(thresH)
	toprint += ','
	for z in items:
		toprint += str(md.num_haiki[z]) 
		toprint += ','
	for z in items:
		toprint += str(md.num_ureta[z]) 
		toprint += ','
	toprint += str(md.cost)
	toprint += ','
	toprint += str(md.price)
	toprint += ','
	toprint += str(md.price - md.cost)
	toprint += ','
	toprint += str(zannen)
	print(toprint)
	
	if plotlog:
		fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)
		for item in items:
			ax2.plot(hotters[item], label = item)
			# ax3.plot(ageki[item], label = item)
			ax3.plot(deli[item], label = item)
			ax4.plot(zaiko[item], label = item)
		# ax4.plot(aburahp)
		ax1.plot(profit, label = 'profit')
		ax1.plot(cost, label = 'cost')
		ax1.plot(price, label = 'earning')
		
		# ax1.legend()
		# ax2.legend()
		ax1.legend()
		ax4.legend()
		plt.show()
		
		'''
		savename = './200427-figs-adjusted/'
		savename += 'fig-' + str(thresL) + '-'
		savename += str(thresH) + '-'
		savename += str(md.avgArrInterv_hi) + '-'
		savename += str(md.avgArrInterv_mi) + '-'
		savename += str(md.avgArrInterv_lo) + '.tif'
		figu = plt.gcf()
		figu.set_size_inches(16, 12)
		plt.savefig(savename, dpi=100)
		plt.close()
		'''
	
	# print('time elapsed: ', time.time()-ts, ' seconds')
