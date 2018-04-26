class Room:
	name = ""
	shape = ""
	sides = 0
	dimensions = []
	door_placement = []
	furnitures = []

	def set_name(self, n):
		self.name = n

	def set_shape(self, s):
		self.shape = s

	def set_sides(self, sides_count):
		self.sides = sides_count

	def set_dimensions(self, d):
		self.dimensions = d

	def set_door_placement(self, doors):
		self.door_placement = doors

	def set_furniture(self, f):
		self.furnitures = f

from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import re
import helper

#-----------file-input -----------------------------
input_file = "./Input/labeled_description.txt"
input_sentences = []
with open(input_file, "r") as ins:
    for line in ins:
        input_sentences.append(line.lower())

roomwise_descriptions =  defaultdict(list)
for tagged_sentence in input_sentences:
	temp = tagged_sentence.split(":")
	roomwise_descriptions[temp[0]].append(temp[1])

#--------Load Information-----------------------------
rooms_file = "./Input/rooms.txt"
rooms_set = helper.load_rooms(rooms_file)

arch_obj_file = "./Input/architectural_objects.txt"
furniture_set = helper.load_architectural_objects(arch_obj_file)

shapes_file = "./Input/shapes.txt"
shapes_set = helper.load_shapes(shapes_file)

#--------Wall Placement Dictionary------------------
wall_dict = defaultdict()
wall_dict["first"] = 1
wall_dict["second"] = 2
wall_dict["third"] = 3

relational_info = []
rooms_list = []

for room_tag,description in roomwise_descriptions.items():
	if room_tag == "relation":
		relational_info = description
	else:
		room = Room()
		room.name = ""
		room.shape = ""
		room.sides = 0
		room.dimensions = []
		room.door_placement = []
		room.furnitures = []

		room.name = room_tag
		print("Type - " + room.name)

		tokens = []
		appended_description = ""
		for sentence in description:
			appended_description = appended_description + sentence
			tokenized = word_tokenize(sentence)
			for token in tokenized:
				tokens.append(token)


		#--------extract room shape ----------------------
		for token in tokens:
			if token in shapes_set:
				room.shape = token
				break
		print("Shape - " + room.shape)

		#--------extract room sides ----------------------
		if room.shape == "square":
			room.sides = 4
		elif room.shape == "rectangular":
			room.sides = 4
		elif room.shape == "triangular":
			room.sides = 3

		if room.sides == 0: 
			# search for "4 walls/sides/sided"
			regex = r'([0-9]+ (sided|sides|walled|walls))'
			match = re.search(regex, appended_description)
			regex = r'([0-9]+)'
			match2 = re.search(regex,match.group(0))
			room.sides = int(match2.group(0))
		print("Sides - " + str(room.sides))


		#--------extract room dimensions ------------------
		if room.sides == 4:
			# search for "30X20"
			regex = r'([0-9]+x[0-9]+)'
			match = re.search(regex, appended_description)
			if match:
				len_breadth = match.group(0).split("x")
				room.dimensions.append(int(len_breadth[0]))
				room.dimensions.append(int(len_breadth[1]))
				room.dimensions.append(int(len_breadth[0]))
				room.dimensions.append(int(len_breadth[1]))
			if len(room.dimensions) == 0 and room.shape == "square":
				regex = r'([0-9]+)'
				match = re.search(regex, appended_description)
				if match:
					side = match.group(0)
					for i in range(0,4):
						room.dimensions.append(int(side))
		else:
			#search for "23, 34, 45 and 23"
			regex = r'([0-9]+, [0-9]+(, [0-9]+)* and [0-9]+)'
			match = re.search(regex, appended_description)
			if match:
				room.dimensions = match.group(0).replace(' and', ',').split(", ")
		print("Dimensions - " + str(room.dimensions))

		#--------extract furnitures ----------------------
		num_dict = [("one",1), ("two",2), ("three",3), ("four",4), ("five",5), ("six",6), ("seven",7), ("eight",8)]
		prev_token = ""
		for token in tokens:
			if token in furniture_set:
				num = 1
				if prev_token == "":
					num = 1
				else:
					#---either 2 or two(set correct num)-------
					regex = r'([0-9]+)'
					match = re.search(regex, prev_token)
					if match:
						num = int(match.group(0))
					for a,b in num_dict:
						if prev_token == a:
							num = b
							break
				room.furnitures.append((token,num))
			prev_token = token
		print("Furnitures - " + str(room.furnitures))

		#--------extract door placements ------------------
		for token in tokens:
			if token in wall_dict.keys():
				room.door_placement.append(wall_dict[token])

		print("Door Placement - " + str(room.door_placement))
		rooms_list.append(room)


#Build graph using relational info-----------
import matplotlib.pyplot as plt
import networkx as nx

connectivity_matrix = []

for sentence in relational_info:
	rooms_found = []
	tokens = word_tokenize(sentence)
	for token in tokens:
		if token in rooms_set:
			for room in rooms_list:
				if token == room.name:
					rooms_found.append(room)
	connectivity_matrix.append((rooms_found[0],rooms_found[1]))

G=nx.cubical_graph()
pos=nx.spring_layout(G) # positions for all nodes

# nodes
nodelist = []
i = 0
for room in rooms_list:
	nodelist.append(i)
	i = i+1
nx.draw_networkx_nodes(G,pos, nodelist, node_color='b', node_size=1800, alpha=0.8)

edgelist = []
for node1,node2 in connectivity_matrix:
	edgelist.append((rooms_list.index(node1),rooms_list.index(node2)))
# edges
nx.draw_networkx_edges(G,pos,edgelist, width=8,alpha=0.5,edge_color='r')

labels={}
i = 0
for room in rooms_list:
	labels[i] = room.name
	i = i+1
nx.draw_networkx_labels(G,pos,labels,font_size=10, color = 'r')

plt.axis('off')
plt.savefig("./Output/connectivity_graph.png") # save as png
plt.show() # display
