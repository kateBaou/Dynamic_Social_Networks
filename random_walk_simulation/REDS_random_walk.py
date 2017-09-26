import matplotlib
import pylab as pl
import networkx as nx
import random as rnd
import pickle
import math

#Find the euclidean distance between two points in the 2D plane
def euclidean_dist(i,j):

	x1,y1=REDS.node[i]['pos']
	x2,y2=REDS.node[j]['pos']
	return math.sqrt((x1-x2)**2+(y1-y2)**2)

def pick_nodes():
	node_name=[]
	degree_set=[]

	for i in REDS.nodes():
		degree_set.append(REDS.degree(i))
		node_name.append(i)

	degree_set,node_name=zip(*sorted(zip(degree_set,node_name)))
	middle=(len(node_name)/2)-1
	picked_nodes.append(node_name[0])
	
	picked_nodes.append(node_name[middle])
	
	picked_nodes.append(node_name[len(node_name)-1])

	
	
def pickle_metrics_random(i,k):

	global density,clustering,assortativity,initial_edges,impact,degree, avg_neigh_degree
	global ranked_nodes, ranked_degrees

	with open('REDSmetrics_random/density/density'+str(k)+'_'+str(i)+'.pickle', 'wb') as f:
		pickle.dump(density, f, pickle.HIGHEST_PROTOCOL)

	with open('REDSmetrics_random/clustering/clustering'+str(k)+'_'+str(i)+'.pickle', 'wb') as f:
		pickle.dump(clustering, f, pickle.HIGHEST_PROTOCOL)

	with open('REDSmetrics_random/assortativity/assortativity'+str(k)+'_'+str(i)+'.pickle', 'wb') as f:
		pickle.dump(assortativity, f, pickle.HIGHEST_PROTOCOL)

	with open('REDSmetrics_random/impact/impact'+str(k)+'_'+str(i)+'.pickle', 'wb') as f:
		pickle.dump(impact, f, pickle.HIGHEST_PROTOCOL)

	with open('REDSmetrics_random/degree/degree'+str(k)+'_'+str(i)+'.pickle', 'wb') as f:
		pickle.dump(degree, f, pickle.HIGHEST_PROTOCOL)

	with open('REDSmetrics_random/neigh_degree/neigh_degree'+str(k)+'_'+str(i)+'.pickle', 'wb') as f:
		pickle.dump(avg_neigh_degree, f, pickle.HIGHEST_PROTOCOL)
	
	with open('REDSmetrics_random/ranked_degree/ranked_degrees'+str(k)+'_'+str(i)+'.pickle', 'wb') as f:
		pickle.dump(ranked_degrees, f, pickle.HIGHEST_PROTOCOL)
	
	with open('REDSmetrics_random/ranked_nodes/ranked_nodes'+str(k)+'_'+str(i)+'.pickle', 'wb') as f:
		pickle.dump(ranked_nodes, f, pickle.HIGHEST_PROTOCOL)

	with open('REDSmetrics_random/degrees/degrees'+str(k)+'_'+str(i)+'.pickle', 'wb') as f:
		pickle.dump(degree_final, f, pickle.HIGHEST_PROTOCOL)
	
	with open('REDSmetrics_random/nodes/nodes'+str(k)+'_'+str(i)+'.pickle', 'wb') as f:
		pickle.dump(node_final, f, pickle.HIGHEST_PROTOCOL)

def save_metrics_random():

	global density,clustering,assortativity,initial_edges,impact,degree, avg_neigh_degree
	global ranked_degrees,ranked_nodes,degree_final,node_final
	new_edges=list(REDS.edges())
	intersect = [filter(lambda x: x in new_edges, sublist) for sublist in initial_edges]
	impact.append(len(new_edges)-len(intersect))
	density.append(round(nx.density(REDS),2))
	clustering.append(round(nx.average_clustering(REDS),2))
	assortativity.append(round(nx.degree_assortativity_coefficient(REDS),2))
	degree.append(REDS.degree(moving))
	avg_neigh_degree.append(round(nx.average_neighbor_degree(REDS,nodes=[moving]).values()[0],2))
	degree_set=[]
	node_name=[]
	for i in REDS.nodes():
		degree_set.append(REDS.degree(i))
		node_name.append(i)
	degree_final.append(degree_set)
	node_final.append(node_name)
	degree_set,node_name=zip(*sorted(zip(degree_set,node_name)))
	ranked_degrees.append(degree_set)
	ranked_nodes.append(node_name)

#Calculate the cost_function
def cost_function(i,j):
   	global S
	common= len(set(list(REDS.neighbors(i))).intersection(list(REDS.neighbors(j))))
	distance=euclidean_dist(i,j)
	cost=distance/(1+S*common)
	return cost

#Find out how much the node spents on its edges
def current_cost(i):
	global E
	cost=0
	for j in REDS.neighbors(i):
		cost+=cost_function(i,j)
	REDS.node[i]['edge_cost']=cost
	return cost

def is_near():
	global moving
	#Remove the moving node from every node's near_enough list
	for i in list(REDS.nodes()):
		if (moving in REDS.node[i]['near_enough']):
			REDS.node[i]['near_enough'].remove(moving)

	#Update the moving node's 'near_enough' list
	for i in list(REDS.nodes()):
		if euclidean_dist(moving,i)<R and i!=moving:
			REDS.node[moving]['near_enough'].append(i)
			if not(moving in REDS.node[i]['near_enough']):
				REDS.node[i]['near_enough'].append(moving)

#Decide whether an adge can be afforded by a node
def is_affordable(i):
	global E 
	REDS.node[i]['affordable']=[]
	#Loop through all the near_enough nodes and add them in affordable if the cost of adding the edge is less than the current
	for j in REDS.node[i]['near_enough']:
		#Calculate the cost of the edge
		possible_cost=cost_function(i,j)
		#if they both can afford this edge
		if current_cost(i)+cost_function(i,j)<=E:
			if current_cost(j)+cost_function(i,j)<=E:
				REDS.node[i]['affordable'].append(j)

#Initialise the attributes of the moving node
def initialise(x,y):

	REDS.node[moving]['pos']=[x,y]
	pos[moving]=REDS.node[moving]['pos']
	REDS.node[moving]['edge_cost']=0
	REDS.node[moving]['near_enough']=[]
	REDS.node[moving]['affordable']=[]

#Make sure that all nodes' spent energy doesnt exceed the predefined threshold. 
#If some nodes spend more energy than they should remove an edge at random and re-stablise the network
def stabilise():
	global E
	over_spend=[]
	for i in list(REDS.nodes()):
		if current_cost(i)>E:
			over_spend.append(i)

	if over_spend:
		# for i in over_spend:
		the_node=rnd.choice(over_spend)
		to_remove=rnd.choice(list(REDS.neighbors(the_node)))
		REDS.remove_edge(the_node,to_remove)
		stabilise()

def wiring():
	#Start wiring the network
	

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

		for u in list(REDS.nodes()):
			if (u in neighborhood) or (i in REDS.node[u]['near_enough']) or (j in REDS.node[u]['near_enough']):
				is_affordable(u)
		return True
	else:
		return False

def initialisation(node):

	global density,clustering,assortativity,initial_edges,impact,degree, avg_neigh_degree, initial_edges
	global ranked_nodes, ranked_degrees,degree_final,node_final, moving, pos
	#Store the positions of the nodes as they are stored in the 'pos' attr of the RGG net
	pos={}
	for i in list(REDS.nodes()):
		pos[i]=REDS.node[i]['pos']

	#Pick at random a node from the list of nodes. This node will be the moving node of the simulation
	moving=node

	#Initialise the metrics_random that you are going to use
	density=[]
	clustering=[]
	assortativity=[]
	impact=[]
	degree=[]
	avg_neigh_degree=[]
	initial_edges=list(REDS.edges())
	ranked_degrees=[]
	ranked_nodes=[]
	degree_final=[]
	node_final=[]
	save_metrics_random()

def step():
	global moving,pos,R, REDS, E,S
	E=0.25
	R=0.2
	S=1
	#Choose the new random coordinates of the moving node that was picked in the readPickle function
	x=rnd.random()
	y=rnd.random()

	#Create a list containing the previous neighbors of the node. This list will be used later on in measuring 
	#the impact of the movements in the network
	previous_neighbors=list(REDS.neighbors(moving))

	#Free the moving node from all his edges
	for i in range(len(previous_neighbors)):
		REDS.remove_edge(moving,previous_neighbors[i])
	
	#Initialise the moving node's attributes
	initialise(x,y)
	#Stabilise the REDS network 
	stabilise()

	#First remove the node from every other node's 'near_enough' list and then update the moving node's near enough list
	is_near()

	#Update the 'affordable' attribute for all the nodes in the network
	for i in list(REDS.nodes()):
		is_affordable(i)

	nodes_afford=True
	while nodes_afford:
		nodes_afford=wiring()
	save_metrics_random()

################################################################################################################################
########################################################------MAIN-----########################################################################

for k in  range(2,10):
	with open('pickleREDS/REDS'+str(k)+'.pickle', 'rb') as f:
		REDS = pickle.load(f)
	print "REDS network number %d"%(k)
	picked_nodes=[]
	pick_nodes()
	for i in picked_nodes:
		initialisation(i)
		for j in range(100):
			step()
		pickle_metrics_random(i,k)

print "The REDS metrics_random have been successfully pickled"