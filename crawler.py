#Library importing
import os
import webdev
import math
import matmult
#Queue Implementing part
queue = []

def add(queue, value):
	queue.append(value)
	
def pop(queue):
	if len(queue) != 0:
		return queue.pop(0)

#Global variables

data_dir_name = "crawling_data"	
url_checking = {}
crawling_url_arr = {} 	#key will be the url and value will be the url folder
incoming_url_arr = {}	#key will be the url of the page, and the value will be the list of url the come to that url
word_crawled = {} #Key will be the word and value would be the number of page that word is in
number_map_url = []
total_page = 0
#Crawling part
#File operating

#This part of the code will reponsible for writing data to file or deleting file, creating new file, directory.

#Time complexity O(N), N is the number of file and directory
def directory_delete(dir_name, current_dir):	
	#Deleting the dir_name directory in the current_dir
	if(os.path.isdir(dir_name)):
		files = os.listdir(dir_name)
		for file in files:
			if(os.path.isfile(os.path.join(dir_name, file))):
				os.remove(os.path.join(dir_name, file))
			else:
				#Change to the sub directory
				os.chdir(os.path.join(current_dir, dir_name))

				#Call recursion to delete the sub directory
				directory_delete(file, os.getcwd())

				 #Move back to the parrent directory
				os.chdir("..")
		os.rmdir(dir_name)

#Time complexity O(N) in the worst case, N is the number of file in the directory dir_name
#Time complexity O(1) in the best case, which is the case that no directory name dir_name has been create
def data_reset(dir_name, current_dir):
	#Reset the dir_name directory in the current_dir, and create the new one
	directory_delete(dir_name, current_dir)
	os.makedirs(dir_name)

#Time complexity O(1), because when we create the new page data, we have already reset, so there must be no directory that has been created previous
def create_page_storage(folder):
	#Creating the new directory to store the page data in the data_dir_name
	#Go inside the directory data_dir_name
	os.chdir(os.path.join(os.getcwd(), data_dir_name))

	#Creating the new directory in the data_dir_name directory
	data_reset(folder, os.getcwd())

	#Return to the main directory
	os.chdir("..")

#Time complexity O(N), N is the total word on the page
def write_word_data(dictionary_word, total_word, folder):
	#Each dictionary_word data will take two line, first line is the word
	#second line is the frequency of that word

	#Write tf_data
	#First line is the word, and second line will be tf data of that word
	fileout = open(os.path.join(os.getcwd(), data_dir_name, folder, "tf_data.txt"), "w")
	for word in dictionary_word:
		value = dictionary_word[word] / total_word
		fileout.write(word + "\n" + str(value) + "\n")
	fileout.close()

#Time complexity O(N), N is the total url that connect to the page with folder
def write_url_data(url_arr, folder):
	#Writing all the url_arr, which is the outgoing url of that page into a file name "outgoing_url.txt"
	#Writing the total outgoing url to the "total_outgoing_url.txt" file
	fileout = open(os.path.join(os.getcwd(), data_dir_name, folder, "outgoing_url.txt"), "w")
	for url in url_arr:
		fileout.write(url + "\n")
	fileout.close()

#Time complexity O(N), N is the total crawled url  
def write_crawling_url_data(crawling_url_arr):
	#Write all the url that has been crawled to the file in data_dir_name directory
	#"crawling_url.txt" file will contain multiple data set
	#Each data set will contain two line
	#First line will be the url
	#Second line will be the folder of that url
	fileout = open(os.path.join(os.getcwd(), data_dir_name, "crawling_url.txt"), "w")
	for url in crawling_url_arr:
		fileout.write(url + "\n")
		fileout.write(crawling_url_arr[url] + "\n")
	fileout.close()

#Time complexity O(N * M), in which N is the total crawled url, M is the number of url conect to that url, Worst case O(N^2),each url will conect to the remain
def write_incoming_url_data():
	#Write the incoming url of each page
	global crawling_url_arr, incoming_url_arr
	for url in crawling_url_arr:
		directory = crawling_url_arr[url]

		fileout = open(os.path.join(os.getcwd(), data_dir_name, directory, "incoming_url.txt"), "w")
		for incoming_url in incoming_url_arr[url]:
			fileout.write(incoming_url + "\n")
		fileout.close()

#Time complexity O(N), in which N is the number of crawled word
def write_idf_data(): 
	#Write the idf value to the "idf_data.txt" file
	total_page = len(crawling_url_arr)
	fileout = open(os.path.join(os.getcwd(), data_dir_name, "idf_data.txt"), "w")

	for word in word_crawled:
		value = math.log2(total_page / (1 + word_crawled[word]))
		fileout.write(word + "\n" + str(value) + "\n")
	fileout.close()

#Time complexity O(N), in which N is the number of crawled URL
def write_matrix_data(matrix):
	fileout = open(os.path.join(os.getcwd(), data_dir_name, "matrix_data.txt"), "w")
	for value in matrix[0]:
		fileout.write(str(value) + "\n")
	fileout.close()

def write_page_title_data(title, folder):
	fileout = open(os.path.join(os.getcwd(), data_dir_name, folder, "page_title.txt"), "w")
	fileout.write(title)
	fileout.close()

#Data operating
#Time complexity O(N), in which N is the length of the line contain the title
def get_page_title(page_content):
	#Getting the page title
	index = 0
	while(index < len(page_content)):
		line = page_content[index]	#The first line of the page_content will contain the tittle
		index += 1
		if(line.find("<title>") > 0):
			index_of_title = line.find("<title>") #Finding the opening tag for the title
			index_of_end_title = line.find("</title>") #Finding the closing tag for the title
			title = line[index_of_title + 7: index_of_end_title]
			return title

#Time complexity O(N*M), in which N is the total line that page, M is the length of the line
def extracting_page_word(page, folder):
	#Extracting the page word and write all necessary data into a file:
	index = 0
	dictionary_word = {}
	total_word = 0
	page_content = page.split("<p")
	
	while index < len(page_content): 
		while index < len(page_content) and page_content[index].find("</p>") < 0:
			index += 1
		#Find the block of of word
		start_index = page_content[index].find(">")
		end_index = page_content[index].find("</p>")
		line = page_content[index][start_index + 1:end_index]
		words = line.split()
		for word in words:
			total_word += 1
			dictionary_word[word] = dictionary_word.get(word, 0) + 1
				
		index += 1

	for word in dictionary_word:
		word_crawled[word] = word_crawled.get(word, 0) + 1 
	write_word_data(dictionary_word, total_word, folder)			#Time complexity O(N)

#Time complexity O(N), N is the length of the url
def find_relative_url(url):
	#Find the substring before relative url
	index = len(url) -1
	while url[index] != "/":
		index -= 1

	if(url[index - 1] == "."):
		return None
	index += 1
	return url[:index]

#Time complexity O(N), N is the number of url that has been found on that page
def push_url_to_queue(url_arr):
	#Push all the url of page to the queue
	global url_checking, crawling_url_arr
	for url in url_arr:
		if(url not in url_checking):
			add(queue, url)
			url_checking[url] = 1

#Time complexity O(N^2), N is the number of total crawled page
def get_matrix():
	total_page = len(crawling_url_arr)
	matrix =  []
	alpha = 0.1

	#Time complexity O(N ^ 2) where N is the number of crawled page
	for index in range(total_page):
		matrix.append([0.0] * total_page)

	#Time complexity O(N ^ 2) in worst case, every page will connect to each other
	for url in crawling_url_arr:
		for incoming_url in incoming_url_arr[url]:
			number_url = int(crawling_url_arr[url])
			number_incoming_url = int(crawling_url_arr[incoming_url])
			matrix[number_url][number_incoming_url] = 1.0
			matrix[number_incoming_url][number_url] = 1.0

	#Time complexity O(N ^ 2), where N is the number of crawled page
	for index_row in range(len(matrix)):
		count_1 = 0.0
		for index_col in range(len(matrix[index_row])):
			if(matrix[index_row][index_col] == 1.0):
				count_1 += 1.0

		for index_col in range(len(matrix[index_row])):
			if(matrix[index_row][index_col] == 1.0):
				matrix[index_row][index_col] /= count_1

	matrix = matmult.mult_scalar(matrix, 1.0 - alpha)

	#Time complexity O(N ^ 2)
	for index_row in range(len(matrix)):
		for index_col in range(len(matrix[index_row])):
			matrix[index_row][index_col] += alpha / float(total_page)

	current_matrix = [[1.0 / float(total_page)]]
	for index in range(total_page - 1):
		current_matrix[0].append(1.0 / float(total_page))

	while True:
		prev_matrix = current_matrix
		current_matrix = matmult.mult_matrix(current_matrix, matrix)
		if(matmult.euclidean_dist(prev_matrix, current_matrix) <= 0.0001):
			break
	
	write_matrix_data(current_matrix)	#Time complexity: O(N)


#Time complexity O(N), N is the total number of page that current_url can reach to
def incoming_url(url_arr, current_url):
	#This function will take all the create the relationship between the current_url and the url in url_arr, which is the list of url that 
	#current_url can reach to
	global incoming_url_arr
	for url in url_arr:	
		if url not in incoming_url_arr:	#Time complexity O(1)
			incoming_url_arr[url] = {}
		if current_url not in incoming_url_arr[url]: #Time complexity O(1)
			incoming_url_arr[url][current_url] = 1

#Time complexity O(N * M), N is the number of line on that page, M is the length of the line
def extracting_page_url(page, current_url, folder, current_relative_url):
	#Time complexity O(N), N is the number of line on that page
	page_content = page.split("<a")
	url_arr = []
	for index in range(len(page_content)):
		line = page_content[index]
		if(line.find("href") < 0):
			continue
		line = line[line.find("href"):]
		# print(line)
		if(line.find("http://") < 0):
			pushing_index = line.find('./') + 2
			tmp = ''
			while line[pushing_index] != '"':
				tmp += line[pushing_index]
				pushing_index += 1
			url_arr.append(current_relative_url + tmp)
		else:
			start = line.find("href")
			temp = ""
			while(line[start] != '"'):
				start += 1
			start += 1
			while(line[start] != '"'):
				temp += line[start]
				start += 1
			url_arr.append(temp)
	incoming_url(url_arr, current_url)	#Time complexity O(N), N is the total number of page that current_url can reach to
	write_url_data(url_arr, folder)		#Time complexity O(N), N is the total url that connect to the page with title
	push_url_to_queue(url_arr)		#Time complexity O(N), N is the number of url that has been found on that page

#Time complexity O(N*M), in which N is the total line that page, M is the length of the line
def extracting_page_data(page, page_content, url, current_relative_url):
	#Extracting page data
	global total_page
	title = get_page_title(page_content)	#Time complexity O(N), in which N is the length of the line contain the title
	crawling_url_arr[url] = str(total_page)
	number_map_url.append(url)
	create_page_storage(str(total_page)) 			#Time complexity O(1), because when we create the new page data, we have already reset, so there must be no directory that has been created previous
	write_page_title_data(title, str(total_page))	
	extracting_page_word(page, str(total_page))	#Time complexity O(N*M), in which N is the total line that page, M is the length of the line
	extracting_page_url(page, url, str(total_page), current_relative_url)	#Time complexity O(N), N is the number of line on that page
	total_page += 1

#Crawl Processs

#Time complexity O(max(N^2, N * M)), N is the number of crawled URL
def crawl(seed):
	data_reset(data_dir_name, os.getcwd())
	global url_checking, crawling_url_arr
	add(queue, seed)	#Time complexity O(1)
	current_seed = seed
	url_checking[seed] = 1
	current_relative_url = ""
	page = webdev.read_url(seed)

	# Time complexity O(N*M), N is the number of crawled url
	while len(queue) != 0:
		current = pop(queue)
		page = webdev.read_url(current)
		page_content = page.split("\n")
		if find_relative_url(current) != None:
			current_relative_url = find_relative_url(current)
		extracting_page_data(page, page_content, current, current_relative_url) #Time complexity O(M), M is the number of line on the page

	write_crawling_url_data(crawling_url_arr)
	write_incoming_url_data()
	write_idf_data()
	get_matrix()