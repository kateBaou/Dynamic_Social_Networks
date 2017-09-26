import matplotlib.pyplot as plt
import pylab as pl
import networkx as nx
import random as rnd
import pickle
import math 
import numpy as np

#Read the pickles
def read_pickled_metrics(u,v):
	global ranked_degrees,ranked_nodes,moving
	ranked_degrees=[[0 for x in range(101)] for y in range(101)] 
	ranked_nodes=[[0 for x in range(101)] for y in range(101)] 
	
	with open('REDSmetrics_brownian/ranked_degree/ranked_degrees'+str(u)+'_'+str(v)+'.pickle', 'rb') as f:
		order_degrees = pickle.load(f)

	with open('REDSmetrics_brownian/ranked_nodes/ranked_nodes'+str(u)+'_'+str(v)+'.pickle', 'rb') as f:
		order_nodes = pickle.load(f)

	k=0
	for i in range(len(order_degrees)):
		l=0
		for j in range(899,len(order_degrees[i])):
			ranked_degrees[k][l]=order_degrees[i][j]
			ranked_nodes[k][l]=order_nodes[i][j]
			l=l+1
		k=k+1


def turn_red(rect,i):
	global to_compare
	for j in range(len(ranked_nodes[i])):
		comparable=str(ranked_nodes[i][j])+str(ranked_degrees[i][j])
		if not(comparable in to_compare):
			rect[j].set_color('r')






for u in range(10):
	for v in range(1,4):

		read_pickled_metrics(u,v)
		#Draw the base case---> The initial network
		fig, ax = plt.subplots()
		bar_width=1
		index=np.arange(len(ranked_nodes[0]))
		rect=ax.bar(index,ranked_degrees[0],0.8)
		plt.ylim(20,50)
		plt.savefig('REDSplots_brownian/rank_plots/rank'+str(u)+'/ranked'+str(u)+'_'+str(v)+'_0'+'.eps', format='eps', dpi=1000)

		#Create a list containing the concatenation of the name of the node and its degree
		#This will demonstate the initial node and degree correspodence
		global to_compare
		to_compare=[]
		for i in range(len(ranked_nodes[0])):
			to_compare.append(str(ranked_nodes[0][i])+str(ranked_degrees[0][i]))

		for i in range(1,len(ranked_nodes),49):
			fig, ax = plt.subplots()
			index=np.arange(len(ranked_nodes[i]))
			rect=ax.bar(index,ranked_degrees[i],0.8)
			#the differences should be painted red
			turn_red(rect,i)
			plt.ylim(20,60)
			name='REDSplots_brownian/rank_plots/rank'+str(u)+'/ranked'+str(u)+'_'+str(v)+'_'+str(i)+'.eps'
			plt.savefig(name,format='eps',dpi=1000)

