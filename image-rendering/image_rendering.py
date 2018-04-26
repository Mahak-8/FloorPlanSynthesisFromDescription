class Room:
	name = ""
	shape = ""
	sides = 0
	dimensions = []
	door_placement = []
	coordinates = []
	#door_coordinates_list = []
	image_path = ""
	furnitures = []

	def set_shape(self, s):
		self.shape = s

	def set_sides(self, sides_count):
		self.sides = sides_count

	def set_dimensions(self, d):
		self.dimensions = d

	def set_open_area(self, o):
		self.open_area = o

	def set_door_placement(self, doors):
		self.door_placement = doors

#-------------- Main File starts -------------------

def get_box_for_furniture(room_coordinates,count,furn_len,furn_bre):
	x,y = room_coordinates[count-1]
	if count == 4:
		return (int(x),int(y-furn_bre),int(x + furn_len),int(y))
	elif count == 3:
		return (int(x-furn_len),int(y-furn_bre),int(x),int(y))
	elif count == 2:
		return (int(x-furn_len),int(y),int(x),int(y+furn_bre))
	elif count == 1:
		return (int(x),int(y),int(x+furn_len),int(y+furn_bre))
	return None

#Recursion Function
def generate_room(previous_room, door_number):
	global pointer
	global room_count
	global rooms_list
	global connectivity_matrix
	global floor_plan_image
	global door_length
	global frame_size
	global scaling_ratio

	room = Room()
	room.door_placement = []
	room.dimensions = []
	room.coordinates = []
	room.furnitures = []
	room_count = room_count+1

	#--------extract room name ----------------------
	sentence = sentences[pointer]
	pointer = pointer+1
	tokenized = word_tokenize(sentence)
	for token in tokenized:
		if token in rooms_set:
			room.name = token
			break
	if room.name == "":
		room.name = "room_" + str(room_count)
	print("Type - " + room.name)

	#--------extract room shape ----------------------
	sentence = sentences[pointer]
	pointer = pointer+1
	tokenized = word_tokenize(sentence)
	for token in tokenized:
		if token in shapes_set:
			room.shape = token
			break
	print("Shape - " + room.shape)

	#--------extract room sides ----------------------
	if room.shape == "square":
		room.sides = 4
	elif room.shape == "rectangular":
		room.sides = 4
	elif room.shape == "pentagonal":
		room.sides = 5
	elif room.shape == "hexagonal":
		room.sides = 6
	elif room.shape == "triangular":
		room.sides = 3

	if room.sides == 0: 
		# search for "4 walls/sides/sided"
		regex = r'([0-9]+ (sided|sides|walled|walls))'
		match = re.search(regex, sentence)
		regex = r'([0-9]+)'
		match2 = re.search(regex,match.group(0))
		room.sides = int(match2.group(0))
	print("Sides - " + str(room.sides))

	#--------extract room dimensions ------------------
	if room.sides == 4:
		# search for "30X20"
		regex = r'([0-9]+x[0-9]+)'
		match = re.search(regex, sentence)
		if match:
			len_breadth = match.group(0).split("x")
			room.dimensions.append(int(len_breadth[0]))
			room.dimensions.append(int(len_breadth[1]))
			room.dimensions.append(int(len_breadth[0]))
			room.dimensions.append(int(len_breadth[1]))
		if len(room.dimensions) == 0 and room.shape == "square":
			regex = r'([0-9]+)'
			match = re.search(regex, sentence)
			if match:
				side = match.group(0)
				for i in range(0,4):
					room.dimensions.append(int(side))
	else:
		#search for "23, 34, 45 and 23"
		regex = r'([0-9]+, [0-9]+(, [0-9]+)* and [0-9]+)'
		match = re.search(regex, sentence)
		if match:
			room.dimensions = match.group(0).replace(' and', ',').split(", ")
	print("Dimensions - " + str(room.dimensions))

	#--------extract furnitures ----------------------
	sentence = sentences[pointer]
	pointer = pointer+1
	tokenized = word_tokenize(sentence)
	prev_token = ""
	for token in tokenized:
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
	sentence = sentences[pointer]
	pointer = pointer+1
	tokenized = word_tokenize(sentence)
	for token in tokenized:
		if token in wall_dict.keys():
			room.door_placement.append(wall_dict[token])

	print("Door Placement - " + str(room.door_placement))
	rooms_list.append(room)

	""""
	#------Generate room image ---------------------------
	room.image_path = "./Room_Images/room_"+str(room_count)+".PNG"
	image = Image.new("RGB", (int(room.dimensions[0]), int(room.dimensions[1])), "white")
	draw = ImageDraw.Draw(image)
	font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 24, encoding="unic")
	draw.text((int(room.dimensions[0])/2, int(room.dimensions[1])/2),room.name,fill='black', font=font)
	room_image = ImageOps.expand(image, border=10)
	room_image.save(room.image_path)
	"""

	#-----Generate Coordinates----------------------------
	if previous_room is None and door_number == 0:
		start_x = (frame_size - room.dimensions[0])/2
		start_y = 20
		room.coordinates.append((start_x,start_y))
		start_x = start_x + room.dimensions[0]
		room.coordinates.append((start_x,start_y))
		start_y = start_y + room.dimensions[1]
		room.coordinates.append((start_x,start_y))
		start_x = start_x - room.dimensions[0]
		room.coordinates.append((start_x,start_y))

		x1,y1 = room.coordinates[0]
		x2,y2 = room.coordinates[1]
		#door_coordinates = []
		#Horizontal door
		door_x = int((x1+x2-door_length)/2)
		door_y = int(y1)
		"""
		door_coordinates.append((door_x,door_y))
		door_x = door_x + door_length
		door_coordinates.append((door_x,door_y))
		"""

		#-----Sketch Image, Doors and Furnitures -------------------------
		draw = ImageDraw.Draw(floor_plan_image)
		draw.polygon(room.coordinates, fill=None, outline="black")
		door_img = Image.open("./Input/SESYD/door.png")
		door_img = door_img.resize((door_length, door_length), Image.ANTIALIAS)
		door_img = door_img.rotate(180)
		floor_plan_image.paste(door_img,(door_x,door_y, door_x + door_length,door_y + door_length))

		random_num = 4
		for furniture_tuple in room.furnitures:
			furniture,furn_count = furniture_tuple
			furn_img = Image.open("./Input/SESYD/"+ furniture +".png")
			length, width = furn_img.size
			furn_len = int(length*scaling_ratio)
			furn_wid = int(width*scaling_ratio)
			furn_img = furn_img.resize((furn_len,furn_wid), Image.ANTIALIAS)
			box = get_box_for_furniture(room.coordinates,random_num,furn_len,furn_wid)
			floor_plan_image.paste(furn_img,box)
			random_num = random_num-1

		#draw.line(door_coordinates,fill="black", width=10
		font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 15, encoding="unic")
		draw.text((int((x1+x2)/2 - 15), y1 + 30),room.name,fill='black', font=font)

	elif door_number == 1:
		x1,y1 = previous_room.coordinates[0]
		x2,y2 = previous_room.coordinates[3]
		x = x1 - room.dimensions[0]
		if previous_room.dimensions[1] == room.dimensions[1]:
			y = y1
			room.coordinates.append((x,y))
			room.coordinates.append((x1,y1))
			room.coordinates.append((x2,y2))
			y = y2
			room.coordinates.append((x,y))
		elif previous_room.dimensions[1] < room.dimensions[1]:
			t = (room.dimensions[1] + y1 - y2)/2
			room.coordinates.append((x,y1-t))
			room.coordinates.append((x1,y1-t))
			room.coordinates.append((x2,y2+t))
			room.coordinates.append((x,y2+t))
		else:
			t = (y2 - y1 - room.dimensions[1])/2
			room.coordinates.append((x,y1+t))
			room.coordinates.append((x1,y1+t))
			room.coordinates.append((x2,y2-t))
			room.coordinates.append((x,y2-t))
		#door_coordinates = []
		#Vertical Door
		door_img = Image.open("./Input/SESYD/door.png")
		door_img = door_img.resize((door_length, door_length), Image.ANTIALIAS)
		door_img = door_img.rotate(270)
		door_x = int(x1)
		door_y = int((y1+y2-door_length)/2)
		"""
		door_coordinates.append((door_x,door_y))
		door_y = door_y + door_length
		door_coordinates.append((door_x,door_y))
		"""

	elif door_number == 2:
		x1,y1 = previous_room.coordinates[3]
		x2,y2 = previous_room.coordinates[2]
		y = y1 + room.dimensions[1]
		if previous_room.dimensions[0] == room.dimensions[0]:
			room.coordinates.append((x1,y1))
			room.coordinates.append((x2,y2))
			x = x2
			room.coordinates.append((x,y))
			x = x1
			room.coordinates.append((x,y))
		elif previous_room.dimensions[0] < room.dimensions[0]:
			t = (room.dimensions[0] + x1 - x2)/2
			room.coordinates.append((x1-t,y1))
			room.coordinates.append((x2+t,y2))
			room.coordinates.append((x2+t,y))
			room.coordinates.append((x1-t,y))
		else:
			t = (x2 - x1 - room.dimensions[0])/2
			room.coordinates.append((x1+t,y1))
			room.coordinates.append((x2-t,y2))
			room.coordinates.append((x2-t,y))
			room.coordinates.append((x1+t,y))

		#door_coordinates = []
		door_img = Image.open("./Input/SESYD/door.png")
		door_img = door_img.resize((door_length, door_length), Image.ANTIALIAS)
		door_img = door_img.rotate(180)
		door_x = int((x1+x2-door_length)/2)
		door_y = int(y1)
		"""
		door_coordinates.append((door_x,door_y))
		door_x = door_x + door_length
		door_coordinates.append((door_x,door_y))
		"""

	elif door_number == 3:
		x1,y1 = previous_room.coordinates[1]
		x2,y2 = previous_room.coordinates[2]
		x = x1 + room.dimensions[0]
		if previous_room.dimensions[1] == room.dimensions[1]:
			room.coordinates.append((x1,y1))
			y = y1
			room.coordinates.append((x,y))
			y = y2
			room.coordinates.append((x,y))
			room.coordinates.append((x2,y2))
		elif previous_room.dimensions[1] < room.dimensions[1]:
			t = (room.dimensions[1] + y1 - y2)/2
			room.coordinates.append((x1,y1-t))
			room.coordinates.append((x,y1-t))
			room.coordinates.append((x,y2+t))
			room.coordinates.append((x2,y2+t))
		else:
			t = (y2 - y1 - room.dimensions[1])/2
			room.coordinates.append((x1,y1+t))
			room.coordinates.append((x,y1+t))
			room.coordinates.append((x,y2-t))
			room.coordinates.append((x2,y2-t))
		#door_coordinates = []
		#Vertical Door
		door_img = Image.open("./Input/SESYD/door.png")
		door_img = door_img.resize((door_length, door_length), Image.ANTIALIAS)
		door_img = door_img.rotate(270)
		door_x = int(x1)
		door_y = int((y1+y2-door_length)/2)
		"""
		door_coordinates.append((door_x,door_y))
		door_y = door_y + door_length
		door_coordinates.append((door_x,door_y))
		"""

	#-----Sketch Image and Doors-------------------------
	xt1,yt1 = room.coordinates[0]
	xt2,yt2 = room.coordinates[1]
	draw = ImageDraw.Draw(floor_plan_image)
	draw.polygon(room.coordinates, fill=None, outline="black")
	floor_plan_image.paste(door_img,(door_x,door_y, door_x + door_length,door_y + door_length))
	#draw.line(door_coordinates,fill="black", width=10)
	random_num = 3
	for furniture_tuple in room.furnitures:
		furniture,furn_count = furniture_tuple
		furn_img = Image.open("./Input/SESYD/"+ furniture +".png")
		length, width = furn_img.size
		furn_len = int(length*scaling_ratio)
		furn_wid = int(width*scaling_ratio)
		furn_img = furn_img.resize((furn_len,furn_wid), Image.ANTIALIAS)
		box = get_box_for_furniture(room.coordinates,random_num,furn_len,furn_wid)
		floor_plan_image.paste(furn_img,box)
		random_num = (random_num-1)%4

	font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 15, encoding="unic")
	draw.text((int((xt1+xt2)/2 - 15), yt1 + 30),room.name,fill='black', font=font)

	print("Room Coordinates - " + str(room.coordinates))
	print(room.name + " generated.")
	if previous_room is not None:
		print("Previous room - " + previous_room.name)

	for door in room.door_placement:
		room_next = generate_room(room,door)
		connectivity_matrix.append((room,room_next))

	pointer= pointer+1
	return room

#-----------Imports------------------------
import helper
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from collections import defaultdict
import re
from PIL import Image, ImageOps, ImageFont, ImageDraw

#-----------file-input -----------------------------
input_file = "./Input/dfs_description_furniture.txt"
f = open(input_file,'r')
description = f.read()
f.close()
description = description.lower()

#----Tokenizing the text into sentences-------------
from nltk.tokenize import sent_tokenize
sentences = sent_tokenize(description)

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
wall_dict["fourth"] = 4
wall_dict["fifth"] = 5
wall_dict["sixth"] = 6
wall_dict["seventh"] = 7

#----------Important Global Variables----------------
pointer = 0
room_count = 0
rooms_list = []
connectivity_matrix = []
frame_size = 600
floor_plan_image = Image.new("RGB", (frame_size,frame_size), "white")
door_length = 30
scaling_ratio = 0.18
floor_plan = generate_room(None, 0)
floor_plan_image.show()
floor_plan_image.save("./Output/floor_plan.PNG")

import matplotlib.pyplot as plt
import networkx as nx

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
#plt.show() # display


