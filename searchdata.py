#Importing module
import os
import math

#Declaring global variable
data_dir_name = "crawling_data"
url_map_folder = {}
page_rank = []
idf_data = {}
tf_data = {}
#Get data
#These below function will open the crawling_data directory and find the needed data, then store in the appropriate database.
#Time complexity O(N), N is the number of crawled url
def get_mapping_data():
	global url_map_folder
	filein = open(os.path.join(os.getcwd(), data_dir_name, "crawling_url.txt"), "r")
	url = filein.readline()
	while(url != ""):
		number = int(filein.readline().strip())
		url = url.strip()
		url_map_folder[url] = number
		url = filein.readline()
	filein.close()
#Time complexity O(N), N is the number of crawled url
def get_matrix_data():
	global page_rank
	filein = open(os.path.join(os.getcwd(), data_dir_name, "matrix_data.txt"), "r")
	value = filein.readline()
	while(value != ""):
		value = float(value.strip())
		page_rank.append(value)
		value = filein.readline()
	filein.close()

#Time complexity O(N), N is the number of crawled word
def get_idf_data():
	filein = open(os.path.join(os.getcwd(), data_dir_name, "idf_data.txt"), "r")
	word = filein.readline()
	while(word != ""):
		value = float(filein.readline().strip())
		word = word.strip()
		idf_data[word] = value
		word = filein.readline()
	filein.close()

def get_tf_data():
	global tf_data
	for url in url_map_folder:
		folder = url_map_folder[url]
		filein = open(os.path.join(os.getcwd(), data_dir_name, str(folder), "tf_data.txt"), "r")
		tf_data[folder] = {}

		word = filein.readline()
		while(word != ""):
			word = word.strip()
			value = float(filein.readline().strip())
			tf_data[folder][word] = value
			word = filein.readline()
		filein.close()
#Time complexity O(N), N is the number of crawled url
def get_data():
	if idf_data != {}:
		return
	get_idf_data()
	get_mapping_data()
	get_matrix_data()
	get_tf_data()

#Operating
#Time complexity O(N), N is the number of url
def get_outgoing_incoming_data(directory, method):
	#This function takes the name of the directory, which is the url page, then extract the data the required data
	#depend on the method. Method will determine which file to open
	if method == "outgoing":
		filein = open(os.path.join(os.getcwd(), data_dir_name, directory, "outgoing_url.txt"))
	else:
		filein = open(os.path.join(os.getcwd(), data_dir_name, directory, "incoming_url.txt"))
	result_arr = []
	line = filein.readline()
	while(line != ""):
		line = line.strip()
		result_arr.append(line)
		line = filein.readline()
	filein.close()
	return result_arr
	
def get_outgoing_links(url):
	#Get outgoing links
	get_data() #Time complexity worst case O(N), almost O(1) every time
	if(url not in url_map_folder):
		return None
	return get_outgoing_incoming_data(str(url_map_folder[url]), "outgoing")	#Time complexity O(N), N is the number of url

def get_incoming_links(url):
	#Get incoming links
	get_data()	
	if(url not in url_map_folder):
		return None
	return get_outgoing_incoming_data(str(url_map_folder[url]), "incoming")	#Time complexity O(N), N is the number of url

def get_page_rank(url):
	get_data()
	if(url not in url_map_folder):
		return -1
	return page_rank[url_map_folder[url]]	

def get_idf(word):
	get_data()
	if word in idf_data:
		return idf_data[word]
	return 0

def get_tf(url, word):
	get_data()
	if(url not in url_map_folder):
		return 0
	return tf_data[url_map_folder[url]].get(word, 0)

def get_tf_idf(url, word):
	get_data()
	tf_value = get_tf(url, word)
	idf_value = get_idf(word)
	return math.log2(1 + tf_value) * idf_value