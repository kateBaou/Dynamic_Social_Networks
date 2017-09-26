import matplotlib
import pylab as pl
import networkx as nx
import random as rnd
import pickle
import math

def euclidean_dist(i,moving):

	x1,y1=RGG.node[i]['pos']
	x2,y2=RGG.node[moving]['pos']
	return math.sqrt((x1-x2)**2+(y1-y2)**2)

def pick_nodes():
	node_name=[]
	degree_set=[]

	for i in RGG.nodes():
		degree_set.append(RGG.degree(i))
		node_name.append(i)

	degree_set,node_name=zip(*sorted(zip(degree_set,node_name)))
	picked_nodes.append(node_name[0])

	for i in range(0,1000):
		if (i+1) % 100 == 0:
			picked_nodes.append(node_name[i])
			

def save_metrics():

	global density,clustering,assortativity,initial_edges,impact,degree, avg_neigh_degree, initial_edges
	global ranked_nodes, ranked_degrees,degree_final,node_final, moving
	new_edges=list(RGG.edges())
	intersect = [filter(lambda x: x in new_edges, sublist) for sublist in initial_edges]
	impact.append(len(new_edges)-len(intersect))
	density.append(round(nx.density(RGG),2))
	clustering.append(round(nx.average_clustering(RGG),2))
	assortativity.append(round(nx.degree_assortativity_coefficient(RGG),2))
	degree.append(RGG.degree(moving))
	avg_neigh_degree.append(round(nx.average_neighbor_degree(RGG,nodes=[moving]).values()[0],2))
	degree_set=[]
	node_name=[]
	for i in RGG.nodes():
		degree_set.append(RGG.degree(i))
		node_name.append(i)
	degree_final.append(degree_set)
	node_final.append(node_name)
	degree_set,node_name=zip(*sorted(zip(degree_set,node_name)))
	ranked_degrees.append(degree_set)
	ranked_nodes.append(node_name)

def pickle_metrics(i,k):

	global density,clustering,assortativity,initial_edges,impact,degree, avg_neigh_degree
	global ranked_nodes, ranked_degrees

	with open('RGGmetrics/density/density'+str(k)+'_'+str(i)+'.pickle', 'wb') as f:
		pickle.dump(density, f, pickle.HIGHEST_PROTOCOL)

	with open('RGGmetrics/clustering/clustering'+str(k)+'_'+str(i)+'.pickle', 'wb') as f:
		pickle.dump(clustering, f, pickle.HIGHEST_PROTOCOL)

	with open('RGGmetrics/assortativity/assortativity'+str(k)+'_'+str(i)+'.pickle', 'wb') as f:
		pickle.dump(assortativity, f, pickle.HIGHEST_PROTOCOL)

	with open('RGGmetrics/impact/impact'+str(k)+'_'+str(i)+'.pickle', 'wb') as f:
		pickle.dump(impact, f, pickle.HIGHEST_PROTOCOL)

	with open('RGGmetrics/degree/degree'+str(k)+'_'+str(i)+'.pickle', 'wb') as f:
		pickle.dump(degree, f, pickle.HIGHEST_PROTOCOL)

	with open('RGGmetrics/neigh_degree/neigh_degree'+str(k)+'_'+str(i)+'.pickle', 'wb') as f:
		pickle.dump(avg_neigh_degree, f, pickle.HIGHEST_PROTOCOL)
	
	with open('RGGmetrics/ranked_degree/ranked_degrees'+str(k)+'_'+str(i)+'.pickle', 'wb') as f:
		pickle.dump(ranked_degrees, f, pickle.HIGHEST_PROTOCOL)
	
	with open('RGGmetrics/ranked_nodes/ranked_nodes'+str(k)+'_'+str(i)+'.pickle', 'wb') as f:
		pickle.dump(ranked_nodes, f, pickle.HIGHEST_PROTOCOL)

	with open('RGGmetrics/degrees/degrees'+str(k)+'_'+str(i)+'.pickle', 'wb') as f:
		pickle.dump(degree_final, f, pickle.HIGHEST_PROTOCOL)
	
	with open('RGGmetrics/nodes/nodes'+str(k)+'_'+str(i)+'.pickle', 'wb') as f:
		pickle.dump(node_final, f, pickle.HIGHEST_PROTOCOL)

def initialise(node):

	global density,clustering,assortativity,initial_edges,impact,degree, avg_neigh_degree, initial_edges
	global ranked_nodes, ranked_degrees,degree_final,node_final, moving, pos
	pos={}
	for i in list(RGG.nodes()):
		pos[i]=RGG.node[i]['pos']

	moving=node

	#Initialise the metrics that you are going to use
	density=[]
	clustering=[]
	assortativity=[]
	impact=[]
	degree=[]
	avg_neigh_degree=[]
	ranked_degrees=[]
	ranked_nodes=[]
	degree_final=[]
	node_final=[]
	initial_edges=list(RGG.edges())
	save_metrics()

def step():
	global moving,pos,R
	R=0.1
	#Choose the new random coordinates of the moving node that was picked in the readPickle function
	x=rnd.random()
	y=rnd.random()	
	#Create a list containing the previous neighbors of the node. This list will be used later on in measuring 
	#the impact of the movements in the network
	previous_neighbors=list(RGG.neighbors(moving))

	#Free the moving node from all his edges
	for i in range(len(previous_neighbors)):
		RGG.remove_edge(moving,previous_neighbors[i])
	
	#Put the moving node in the random position that was selected previously
	RGG.node[moving]['pos']=[x,y]
	pos[moving]=RGG.node[moving]['pos']
	
	#Wire the system 
	for i in list(RGG.nodes()):
		if euclidean_dist(i,moving)<R and i!=moving:
			RGG.add_edge(i,moving)

	#Store the graph metrics now that the network has stabilised
	save_metrics()


####################################################################################################################################
########################################--------------MAIN-------------#############################################################

global RGG, positions, moving, pos,density,clustering,assortativity, initial_edges,impact,degree, avg_neigh_degree
global ranked_nodes, ranked_degrees,degree_final,node_final,picked_nodes

for k in  range(10):
	with open('pickleRGG/RGG'+str(k)+'.pickle', 'rb') as f:
		RGG = pickle.load(f)
	print "RGG network number %d"%(k)
	picked_nodes=[]
	pick_nodes()
	for i in picked_nodes:
		initialise(i)
		for j in range(100):
			step()
		pickle_metrics(i,k)

print "The RGG metrics have been successfully pickled"