import func

"""Big Data Management - Msc Data Science -1st Programming Assignment
    Chord - based simulation of a distributed file system"""


def __main__():
	"""This function is the function main which calls all the other functions and runs the Chord Algorithm
	It also performs some measurements regarding the number of messages needed to locate a single file and the load of each node"""

	#ask user to give the number of requests
	requests = func.checkInputs("Enter the number of Requests \n ")
	# ask user to give the number of alive Nodes
	nodes = func.checkInputs("Enter the number of nodes \n ")
	# fill the ordered list of alive Nodes and a dictionary which has as key node and as value the movie
	keylist, diction = func.create_nodes(nodes)
	# for each one of the nodes call the method predecessor_successor and the one that fills the finger_table
	for i in keylist:
		diction[i].predecessor_successor(keylist)
		diction[i].fill_finger_table(nodes,keylist)
	# fill a list of tuples concerning requests
	hashed_req = func.hashing(requests, nodes)
	for j in hashed_req:
		func.fill_requests(keylist, diction, j[0], j[2])
	responsible_nodes, messages_for_each, list_nodes = func.read_requests(diction, nodes)
	#computes statistical analysis for messages and nodes
	func.statistical_analysis(diction, messages_for_each, list_nodes, responsible_nodes)







