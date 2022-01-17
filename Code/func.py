import random
import hashlib
from Node import Node
from scipy.stats import powerlaw
from collections import Counter
import csv

''' Big Data Management - Msc Data Science -
    1st Programming Assignment
    Chord - based simulation of a distributed file system'''


def checkInputs(message):
	"""Check if the user's input is an integer"""

	while True:
		try:
			Userinput = int(raw_input(message))
		except ValueError:
			print("No valid integer! Please try again ...")
		else:
			return Userinput

def hashing(requests, nodes):
	"""Function that read the given file line by line and hash each string using SHA-1.
	The function returns a list of tuples. Each tuple has the requested item, the file's name and a random start"""

	hash_list = []
	with open('filenames.txt') as f:
		count = 0
		lines = random.sample(f.readlines(), requests)
		popularity = powerlaw.rvs(1.65, size=len(lines), discrete=True, scale=10)
		for line in lines:
			hash_object = hashlib.sha1(line)
			hash_key = int(hash_object.hexdigest(), 16) % (2 ** 15)
			hash_tuple = (hash_key, line.rstrip('\n'), popularity[count])
			hash_list.append(hash_tuple)
			count += 1
	return hash_list


def create_nodes(nodes):
	""" This function gets the # of nodes as input. It creates a dictionary with node's hashed ip as key and as value the node object
	From this dictionary we export a list which contains the keys of the dictionary sorted from min to max"""

	diction = {}
	for i in range(nodes):
		node = Node(nodes)
		diction[node.hashed_ip] = node
	keylist = diction.keys()
	keylist.sort()
	return keylist, diction


def fill_requests(keylist, diction, movie, popularity):
	"""Fill each node's list with the requests"""
	for i in range(popularity):
		diction[random.choice(keylist)].messages_list(movie)


def read_requests(diction, nodes):
	"""Reads the requests one by one and serve them"""
	list_nodes = []
	responsible_nodes = []
	messages_for_each = []
	for start in diction.keys():
		for item in diction[start].message:
			first_message = (None, item)
			diction[start].msg_to_next(first_message)
			counter_message = 0
			list_nodes.append(start)
			resp_node, count_msg, list_nodes = lookup(start, diction, nodes, counter_message, list_nodes)
			responsible_nodes.append(resp_node)
			messages_for_each.append(count_msg)
	return responsible_nodes, messages_for_each, list_nodes


def lookup(start, diction, nodes, count_messages, list_nodes):
	"""This function is the implementation of the lookup in the Chord. With this lookup the algorithm searches for the Node that has
	the requested item"""

	request = diction[start].msg[1]
	next_message = (start, request)
	if diction[start].predecessor > diction[start].hashed_ip:
		if diction[start].predecessor < request <= (2 ** 15)-1 or 0 <= request <= diction[start].hashed_ip:
			return (start, count_messages, list_nodes)
	else:
		if diction[start].predecessor < request <= diction[start].hashed_ip:
			return (start, count_messages, list_nodes)
        
	if diction[start].successor < diction[start].hashed_ip:
		if diction[start].hashed_ip < request <= (2 ** 15)-1 or 0 <= request <= diction[start].successor:
			return (diction[start].successor, count_messages, list_nodes)
	else:
		if diction[start].hashed_ip < request <= diction[start].successor:
			return (diction[start].successor, count_messages, list_nodes)
        
	for item in reversed(diction[start].finger_table):
		if request < start:
			if diction[start].hashed_ip < item[1] <= (2 ** 15)-1 or 0 <= item[1] < request:
				diction[item[1]].msg_to_next(next_message)
				count_messages = count_messages + 1
				list_nodes.append(item[1])
				return lookup(item[1], diction, nodes, count_messages, list_nodes)
		else:
			if diction[start].hashed_ip < item[1] < request:
				diction[item[1]].msg_to_next(next_message)
				count_messages = count_messages + 1
				list_nodes.append(item[1])
				return lookup(item[1], diction, nodes, count_messages, list_nodes)

def statistical_analysis(diction, messages_for_each, list_nodes, responsible_nodes):
	"""Exports .csv files with the statistical measures"""

	tot_messages = {}
	all_requests = []
	for k in diction.keys():
		all_requests.append(diction[k].message)
	all_requests = [item for sublist in all_requests for item in sublist]
	my_tuples = zip(all_requests, messages_for_each)
	for x, y in my_tuples:
		tot_messages.setdefault(x, []).append(y)
	for item in tot_messages.keys():
		tot_messages[item] = round(sum(tot_messages[item])/float(len(tot_messages[item])), 2)
	occurencies_router = Counter(list_nodes)
	occurencies_requests = Counter(responsible_nodes)
	write_files('Load of node by requests.csv', occurencies_requests)
	write_files('Load of node by routed.csv', occurencies_router)
	write_files('Average messages.csv', tot_messages)
	test = sum(messages_for_each)
	test2 = []
	test2.append(test)
	writefile = open('Sum of messages.csv', 'a')
	writer = csv.writer(writefile)
	writer.writerow(test2)
	writefile.close()


def write_files(file, type_of_data):
	"""write to .csv files"""
	writefile = open(file, 'a')
	writer = csv.writer(writefile)
	for key, count in type_of_data.iteritems():
		writer.writerow([key, str(count)])
	writefile.close()