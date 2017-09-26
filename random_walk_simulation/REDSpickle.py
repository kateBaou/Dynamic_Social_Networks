

#REDS network construction
"""

"""

import matplotlib
import math 
import matplotlib.pyplot as plt
import numpy as np
import random as rnd
import networkx as nx
import pickle

#define variables N,E,R,S
def net_creation(w):
	N=50
	E=0.25
	R=0.2
	S=1
	global pos

	#Calculate the euclidean distance between two nodes
	def euclidean_dist(i,j):
		
		x1,y1=REDS.node[i]['pos']
		x2,y2=REDS.node[j]['pos']
		return math.sqrt((x1-x2)**2+(y1-y2)**2)

	#Calculate the value of the cost function c(i,j)=euclidean_dist(i,j)/(1+S*common)
	def cost_function(i,j):
	
		common= len(set(list(REDS.neighbors(i))).intersection(list(REDS.neighbors(j))))
		distance=euclidean_dist(i,j)
		cost=distance/(1+S*common)
		
		return cost

	#Find out how much the node has spent on its edges
	def current_cost(i):
		cost=0
		for j in REDS.neighbors(i):
			cost+=cost_function(i,j)
		REDS.node[i]['edge_cost']=cost
		return cost

	#Decide whether an adge can be afforded by a node
	def is_affordable(i):
		
		REDS.node[i]['affordable']=[]
		#Loop through all the near_enough nodes and add them in affordable if the cost of adding the edge is less than the current
		for j in REDS.node[i]['near_enough']:
			#Calculate the cost of the edge
			possible_cost=cost_function(i,j)
			#if they both can afford this edge
			if current_cost(i)+cost_function(i,j)<=E:
				if current_cost(j)+cost_function(i,j)<=E:
					REDS.node[i]['affordable'].append(j)

	#Initialise the network with the parameters given in the begining of the code
	def initialise():
		global REDS,pos
		REDS=nx.Graph()
		REDS.add_nodes_from(range(N))
		pos={}
		#Initialise the nodes' position, edge_cost, set of possible neighbours and a subset of affordable neighbours
		for i in range(N):
			x=rnd.random()
			y=rnd.random()
			#Allocate the random x,y coordinates
			REDS.node[i]['pos']=[x,y]
			#Allocate the current edge_cost
			REDS.node[i]['edge_cost']=0
			#Store the position of the node in a list
			pos[i]=REDS.node[i]['pos'] 
			#Create a list containing the nodes that are close to i. This will be initially empty
			REDS.node[i]['near_enough']=[]
			#Create a list/subset of the previous one containing the affordable neighbours. Again this will be initially empty
			REDS.node[i]['affordable']=[]

		"""Fill the "near_enough" list with each node's closest neighbours. For that reason it is necessary to calculate the 
			Euclidean distance betwen the node in question and the rest of the nodes in the graph. A neighbour is close if and
			only if the euclidean distance between the two is less than R.
		"""
		for i in range(N-1):
			for j in range(i+1,N):
				if euclidean_dist(i,j)<R:
					REDS.node[i]['near_enough'].append(j)
					REDS.node[j]['near_enough'].append(i)

		"""Fill the "affordable" list with the node's affordable neighbours. Affordable neighbours are the possible neighbours 
			(i.e the nodes that already exist in near_enough list)which edge cost is less than the total current edge_cost of each node. 
		"""
		for i in range(N):
			is_affordable(i)
	


	#Start wiring the network
	def wiring():

		#Store all the nodes of the network that have the potential to afford an edge
		afford=[]
		
		only_afford=dict(nx.get_node_attributes(REDS,'affordable'))

		for i in only_afford:
			if(only_afford[i]):
				
				afford.append(i)

		if afford:
			#Choose a node at random and another one from its affordable list
			i=rnd.choice(afford)
			

			j=rnd.choice(only_afford[i])
			
			
			#Add the edge from i to j
			REDS.add_edge(i,j)
			
			#Update the related lists and values (i.e near_enough, affordable, edge_cost)
			REDS.node[i]['near_enough'].remove(j)
			REDS.node[j]['near_enough'].remove(i)
			current_cost(i)
			current_cost(j)

			#In order to update the affordables after adding the edge we need to consider all the neighbors of i & j and the nodes
			#that are not yet neighbor of i or j (i.e the nodes in each node's near enough list)
			neighborhood=list(REDS.neighbors(i))+list(REDS.neighbors(j))

			for u in range(N):
				if (u in neighborhood) or (i in REDS.node[u]['near_enough']) or (j in REDS.node[u]['near_enough']):
					is_affordable(u)
			return True
		


	#Create the seed network
	initialise()
	nodes_afford=True

	#Wire the network until there are no more valid and affordable edges to be placed
	while nodes_afford:
		nodes_afford=wiring()
	
	
	hist=nx.degree_histogram(REDS)
	dense=nx.density(REDS)
	
	total= REDS.number_of_edges()
	
	var="pickleREDS/REDS"+str(w)+".pickle"
	with open(var, 'wb') as f:
	    # Pickle the 'data' dictionary using the highest protocol available.
	    pickle.dump(REDS, f, pickle.HIGHEST_PROTOCOL)


	
	return dense
