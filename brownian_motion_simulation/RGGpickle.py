import math 
import matplotlib.pyplot as plt
import numpy as np
import random as rnd
import networkx as nx
from REDSpickle import net_creation
import pickle
import datetime
#define global variables N and R
N=50
R=0.2
global pos


def euclidean_dist(i,j):
	
	x1,y1=RGG.node[i]['pos']
	x2,y2=RGG.node[j]['pos']
	return math.sqrt((x1-x2)**2+(y1-y2)**2)

def creation(k):
	global RGG,pos
	tmp_dense=0.0
	RGG=nx.Graph()
	RGG.add_nodes_from(range(N))
	pos={}
	
	dense=net_creation(k)
	for i in range(N):
		x=round(rnd.random(),2)
		y=round(rnd.random(),2)
		#Allocate the random x,y coordinates
		RGG.node[i]['pos']=[x,y]
		pos[i]=RGG.node[i]['pos']

	
	for i in range(N-1):
		for j in range(i+1,N):
			if euclidean_dist(i,j)<R:
				RGG.add_edge(i,j)
				tmp_dense=nx.density(RGG)
			if tmp_dense>=dense:
				break
		if tmp_dense>=dense:
			break

start=datetime.datetime.now().time()
#Create 10 networks
for i in range(10):
	creation(i)

	var="pickleRGG/RGG"+str(i)+".pickle"
	with open(var, 'wb') as f:
	    # Pickle the 'data' dictionary using the highest protocol available.
	    pickle.dump(RGG, f, pickle.HIGHEST_PROTOCOL)

end= datetime.datetime.now().time()

file=open("logfile.txt","w") 
file.write("Start: "+str(start)+" End: "+str(end))
file.close




