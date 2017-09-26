import matplotlib.pyplot as plt
import pylab as pl
import networkx as nx
import random as rnd
import pickle
import math 
import numpy as np

#Read the pickles
def read_pickled_metrics(i,j):
	global density,clustering,assortativity,impact,degree, neigh_degree
	with open('REDSmetrics_random/density/density'+str(i)+'_'+str(j)+'.pickle', 'rb') as f:
		density = pickle.load(f)

	with open('REDSmetrics_random/clustering/clustering'+str(i)+'_'+str(j)+'.pickle', 'rb') as f:
		clustering = pickle.load(f)

	with open('REDSmetrics_random/assortativity/assortativity'+str(i)+'_'+str(j)+'.pickle', 'rb') as f:
		assortativity = pickle.load(f)

	with open('REDSmetrics_random/impact/impact'+str(i)+'_'+str(j)+'.pickle', 'rb') as f:
		impact = pickle.load(f)

	with open('REDSmetrics_random/degree/degree'+str(i)+'_'+str(j)+'.pickle', 'rb') as f:
		degree = pickle.load(f)

	with open('REDSmetrics_random/neigh_degree/neigh_degree'+str(i)+'_'+str(j)+'.pickle', 'rb') as f:
		neigh_degree = pickle.load(f)


def frequencies(lst):
	val_lst=[]
	frq_val=[]
	for i in lst:
		if not(i in val_lst):
			val_lst.append(i)
			frq_val.append(lst.count(i))

	#Sort the values and the corresponding frequencies		
	val_lst,frq_val=zip(*sorted(zip(val_lst,frq_val)))
	return val_lst,frq_val

for i in range(10):
	for j in range(1,4):
		read_pickled_metrics(i,j)

		f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(30,30))
		bar_width=0.5
		opacity=0.5
		#Create the density bar chart
		val, frq =frequencies(density)
		index=np.arange(len(val))
		ax1.bar(index,frq,bar_width,align='center',alpha=opacity)
		ax1.set_xticks(index)
		ax1.set_xticklabels(val)
		ax1.set_ylabel('Frequency',fontsize=20)
		ax1.set_xlabel('Density',fontsize=20)

		#Create the clustering bar chart
		val, frq =frequencies(clustering)
		index=np.arange(len(val))
		ax2.bar(index,frq,bar_width,alpha=opacity)
		ax2.set_xticks(index+bar_width/2)
		ax2.set_xticklabels(val)
		ax2.set_ylabel('Frequency',fontsize=20)
		ax2.set_xlabel('Clustering',fontsize=20)

		#Create the assortativity bar chart
		val, frq =frequencies(assortativity)
		index=np.arange(len(val))
		ax3.bar(index,frq,bar_width,alpha=opacity)
		ax3.set_xticks(index+bar_width/2)
		ax3.set_xticklabels(val)
		ax3.set_ylabel('Frequency',fontsize=20)
		ax3.set_xlabel('Assortativity',fontsize=20)

		#Create the impact bar chart
		val, frq =frequencies(impact)
		index=np.arange(len(val))
		ax4.bar(index,frq,bar_width,alpha=opacity)
		ax4.set_xticks(index+bar_width/2)
		ax4.set_xticklabels(val)
		ax4.set_ylabel('Frequency',fontsize=20)
		ax4.set_xlabel('Impact',fontsize=20)

		fig = pl.gcf()
		fig.suptitle("Frequency vs REDS Metrics", fontsize=30)

		plt.savefig('REDSplots_random/frequency_plots/frequency'+str(i)+'_'+str(j)+'.eps', format='eps', dpi=1000)
