#Spatially embedded social networks with mobile nodes#

The aim of this project is to explore the changes made in the salient features of
spatially embedded social networks once they start moving in space and time.

The idea behind this project is very inventive since there is not enough related
work in this field per se. The interest of the researchers was focused in examin-
ing spatially embedded networks and social networks in a static way. However,
in this project the spatial constraints and community structure of social networks
are going to be altered due to a set of mobility models. These mobility models
are going to mimic the unpredictable and regional ways entities move in nature.
During, this procedure the characteristic values (e.g the clustering coefficient, the
density, the assortativity etc.) of the network will be calculated in every time step
and then presented in specific diagrams. Through this study, it is denoted that the
social networks with high community structure (i.e REDS social networks) reflect
more accurately in their characteristic values the changes performed by the mobility
models than the equivalent canonical spatial/social network models (i.e RGG net-
works).

The main objectives of this project are the following:

-Move the networks in time and space according to predefined mobility models
and store the variations of their salient features.
-Show in fitting diagrams (e.g frequency plots, rank plots etc.) the key findings
and analyse them thoroughly.

The project’s added value is immense since it provides an accurate model of
complex societies which have always been the centre of attention of all research-
ers. The former social network models static nature made them unrealistic since
modern societies are characterised by constant changes. This dynamic model can
help researchers model the internal relationships of the society in a precise way and
propose well-targeted solutions in serious social problems.


##In this repository##

The brownian motion and the random walk simulation folders containt the codes responsible for the construction, 
relocation and storage of the networks. 

1.To initialise the construction you need to run the RGGpickle.py in any of the folders that is responsible for 
creating 10 RGG and 10 REDS networks with the same density values.
2. To run the simulation in a RGG network you need to run RGG_random_walk.py or RGG_brownian_motion.py and the 
respective file for REDS networks.
3. To produce the diagrams you need to run the code that describes the type of network followed by the kind of 
diagram you want to produce.

The produced RGG/REDS networks, metrics and plots are stored in the appropriate folders of each simulation.
