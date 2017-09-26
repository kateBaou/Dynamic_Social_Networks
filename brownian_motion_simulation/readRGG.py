import pickle
import networkx as nx
import matplotlib.pyplot as plt

with open('pickleRGG/RGG9.pickle', 'rb') as f:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    RGG = pickle.load(f)

with open('pickleREDS/REDS9.pickle', 'rb') as w:
    # The protocol version used is detected automatically, so we do not
    # have to specify it.
    REDS = pickle.load(w)


print "RGG edges and nodes"
print nx.number_of_nodes(RGG)
print nx.number_of_edges(RGG) 
print "REDS edges and nodes"
print nx.number_of_nodes(REDS)
print nx.number_of_edges(REDS) 
