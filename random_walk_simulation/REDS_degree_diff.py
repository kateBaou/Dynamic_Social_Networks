import matplotlib.pyplot as plt
import pylab as pl
import networkx as nx
import random as rnd
import pickle
import math 
import numpy as np
from matplotlib import rc
#Read the pickles
def read_pickled_metrics(k,l):
	global degrees,nodes,moving
	with open('REDSmetrics_brownian/degrees/degrees'+str(k)+'_'+str(l)+'.pickle', 'rb') as f:
		degrees = pickle.load(f)

	with open('REDSmetrics_brownian/nodes/nodes'+str(k)+'_'+str(l)+'.pickle', 'rb') as f:
		nodes = pickle.load(f)

for k in range(10):
	for l in range(1,4):
		plt.cla()
		plt.clf()
		read_pickled_metrics(k,l)

		plt.ylim(-10,60)
		x=np.arange(len(degrees))

		for j in range(len(degrees[0])):
			Dr=[]
			for i in range(len(degrees)):
				Dr.append(degrees[i][j]-degrees[0][j])
			plt.plot(x,Dr)
		rc('text',usetex=True)
		plt.ylabel(r"$\Delta d= d'-d$, $d$ initial degree $d'$ new degree")
		plt.title("REDS Degree Differences in Brownian motion model")
		plt.savefig('REDSplots_brownian/degree_diff/degree_dif'+str(k)+'_'+str(l)+'.eps', format='eps', dpi=1000)


