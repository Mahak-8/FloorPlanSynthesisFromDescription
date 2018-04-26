def load_rooms(room_file):
	#User defined AOs input from a file (architectural_objects.txt)
	f = open(room_file,'r')
	data = f.read()
	rooms = data.split(",")
	return set(rooms)

def load_shapes(shape_file):
	#User defined AOs input from a file (architectural_objects.txt)
	f = open(shape_file,'r')
	data = f.read()
	shapes = data.split(",")
	return set(shapes)

def load_architectural_objects(AOs_file):
	#User defined AOs input from a file (architectural_objects.txt)
	f = open(AOs_file,'r')
	data = f.read()
	AOs = data.split(",")
	return set(AOs)

import string
from nltk.corpus import stopwords
def preprocess(sentences):
	english_stops = set(stopwords.words('english'))
	preprocessed_sentences = []
	for sentence in sentences:
		# Remove WhiteSpaces from string
		sentence = " ".join(sentence.split())
		tokenized = word_tokenize(sentence)
		tokens = [token for token in tokenized if token not in english_stops]
		sentence = " ".join(tokens)
		# Lower case coversion
		sentence = sentence.lower()
		#Remove punctuation
		for c in string.punctuation:
			sentence = sentence.replace(c,"")
		preprocessed_sentences.append(sentence)
	return preprocessed_sentences

def tokenization_step2(tagged_sentences):
	new_tagged_sentences = []
	for sentence, tag in tagged_sentences:
		tokens = re.split(';|,|and|which|also',sentence)
		if(len(tokens) > 1):
			for token in tokens:
				new_tagged_sentences.append((token,tag))
		else:
			new_tagged_sentences.append((sentence,tag))
	return new_tagged_sentences

import re
def extract_dimensions(tagged_sentences):
	regexes = []
	regexes.append(r'(\d{1,4}.{0,2}m[.]?[2|xb2])')                                 # Finds 16m2
	regexes.append(r'(\d{1,4}[.,]?\d{0,3}[ ]?[x]?[ ]\d{1,4}[.,]?\d{0,3}[ ?]m)')     # Finds 3.90 x 3,00m & 3.90 x 3,00
	regexes.append(r'(\d{1,4}[ ]?x[ ]?\d{1,4})')                                     # Finds 640x390
	dimensions = []
	i = 0
	for tagged_sentence in tagged_sentences:  # Try regex in the order described above
		for regex in regexes:
			match = re.search(regex, tagged_sentence[0])
			if match is not None:
				dimensions.append((tagged_sentence[1],match.group(0)))
				#tagged_sentences.pop(i)
		i = i+1
	return dimensions

import nltk
from nltk.tokenize import word_tokenize
def identify_rooms(sentences, rooms_set):
	identified_rooms = set()
	for sentence in sentences:
		#Tokenize
		tokenized = word_tokenize(sentence)
		#Extracting proper nouns and AOs
		objects = [token for token in tokenized if token in rooms_set]
		for obj in objects:
			identified_rooms.add(obj)
	return identified_rooms;

def identify_AOs(sentences, AOs_set):
	identified_AOs = set()
	for sentence in sentences:
		#Tokenize
		tokenized = word_tokenize(sentence)
		#Extracting proper nouns and AOs
		objects = [token for token in tokenized if token in AOs_set]
		for obj in objects:
			identified_AOs.add(obj)
	return identified_AOs;

"""
Three types of sentences can be here:
[1] Which describes its location w.r.t to other AOs
[2] Which describes its location wrt to floorplan itself
[3] Which describes the structure and properties of the floorplan
^^Dealing with only Type I sentences for now.
"""
#-- Classes are rooms (For now - Bedroom, Bathroom, Kitchen, Informative(useless for us))
#--Implement using text classification here. Ouptut [(sentence,tag), (sentence,tag)...]
def sentence_tagging(sentences):
	tagged_sentences = []
	#Decided manually for now
	tags = ["entrance","entrance","hall","hall","hall","bathroom","bathroom","kitchen","bedroom"]
	for i in range(0,len(sentences)):
		tagged_sentences.append((sentences[i],tags[i]))

	return tagged_sentences

def update_relation_tag(tagged_sentences,identified_rooms):
	updated_tagged_sentences = []
	for sentence,tag in tagged_sentences:
		sentence_as_list = []
		sentence_as_list.append(sentence)
		rooms = identify_rooms(sentence_as_list,identified_rooms)
		if(len(rooms) > 1):
			tag = "relation"
		updated_tagged_sentences.append((sentence,tag))
	return updated_tagged_sentences

#---Output - [(bathroom, list<sentence> description)...]
from collections import defaultdict
def generate_grouped_description(tagged_sentences):
	room_descriptions =  defaultdict(list)
	for tagged_sentence in tagged_sentences:
		room_descriptions[tagged_sentence[1]].append(tagged_sentence[0])
	return room_descriptions

"""
Positional classes (TBRL)
__1001__|__1000__|__1010__
__0001__|__0000__|__0010__
__0101__|__0100__|__0110__

"""
def load_similar_directions(normalized_direction_file):
	direction_dict = dict()
	f = open(normalized_direction_file,'r')
	for line in f:
		line = line.rstrip()
		sim_directions = line.split(":")
		direction_dict[sim_directions[1]] = sim_directions[0]
	return direction_dict


def positional_classification(room, description, identified_AOs, direction_dict):
	#intialize labels to NULL
	room_position = []
	object_positions = dict()
	print(room)
	print(description)
	print(identified_AOs)
	for sentence in description:
		tokenized = word_tokenize(sentence)
		AO = ""
		#Indentify AO in sentence
		for token in tokenized:
			if token in identified_AOs:
				AO = token
		#Extracting positional words (Find positional code)
		codes = []
		positional_words = [token for token, pos in nltk.pos_tag(tokenized) if pos in ('JJ', 'JJS', 'JJR','NN', 'VBR')]
		print("Printing positional tags of Architectural Objects........")
		print(AO,positional_words)
		for ps in positional_words:
			if ps in direction_dict.keys():
				position = direction_dict[ps]
				codes.append(position)
		if AO == "":
			room_position = codes
		else:
			object_positions[AO] = codes

	return (room,room_position,object_positions)
