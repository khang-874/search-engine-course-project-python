import searchdata
import math
import os

url_map_title = {}
folder_map_url = {}

#Time complexity O(N), N is the number of word in a phrase
#This function take a list of words as an argument then caculate the tf value.
#Return the dictionary contain distinct word, in which key is the word and value is the tf value.
def phrase_tf_data(words):
	dictionary = {}
	total_word = 0
	for word in words:
		dictionary[word] = dictionary.get(word, 0.0) + 1.0
		total_word += 1
	for word in dictionary:
		dictionary[word] = dictionary[word] / float(total_word)
	return dictionary

#Time complexity O(N), N is the length of words
#This function take a list of distinct words as an argument to get the idf value from the crawling data
#Return a dictionary contains distinct word, in which key is the word and value is the idf value.
def phrase_idf_data(words):
	dictionary = {}
	for word in words:
		dictionary[word] = searchdata.get_idf(word)
	return dictionary

#Time complexity O(N), N is the length of the vector
#Taking two vector as parameter, this function will compute the cosin similarity between it.
def get_cosin_similarity(document_vector, phrase_vector):
	numerator = 0.0
	for index in range(len(document_vector)):
		numerator += float(document_vector[index] * phrase_vector[index])
	if numerator == 0.0:
		return 0.0
	left_denumerator = 0.0
	for index in range(len(document_vector)):
		left_denumerator += float(document_vector[index] * document_vector[index])
	left_denumerator = math.sqrt(left_denumerator)
	right_denumerator = 0.0
	for index in range(len(phrase_vector)):
		right_denumerator += float(phrase_vector[index] * phrase_vector[index])
	right_denumerator = math.sqrt(right_denumerator)

	return numerator / (left_denumerator * right_denumerator)

#Time complexity O(N), N is the number of crawled page
#This function will take the data of crawled URL and its title from the crawling data, then store it in the appropriate dictionary.
def get_url_data():
	filein = open(os.path.join(os.getcwd(), "crawling_data", "crawling_url.txt"), "r")
	url = filein.readline().strip()
	while url != "":
		folder = filein.readline().strip()
		folder_map_url[folder] = url
		url = filein.readline().strip()
	filein.close()

#Time complexity O(N * M), in which N is the number of page, and M is the number of distinct word in phrase
def search(phrase, boost):
	words = phrase.strip().split()
	tf_data = phrase_tf_data(words)
	idf_data = phrase_idf_data(tf_data)
	check_word = {}
	phrase_vector = []
	#Time complexity O(N), N is the length of tf_data dictionary
	for word in tf_data:
		phrase_vector.append(float(math.log2(tf_data[word] + 1)) * idf_data[word])

	get_url_data()

	cosin_list = []

	#Time complexity O(N * M), where M is the number of distinct word in phrase, and N is the number of page
	for folder in folder_map_url:
		document_vector = []

		for word in tf_data:
			document_vector.append(searchdata.get_tf_idf(folder_map_url[folder], word))
		#Time complexity O(M), in which M is the number of crawled vector
		value = get_cosin_similarity(document_vector, phrase_vector) #Time complexity of this funciton is O(M)
		if(boost == True):
			value *= searchdata.get_page_rank(folder_map_url[folder])

		filein = open(os.path.join(os.getcwd(), "crawling_data", folder, "page_title.txt"), "r")
		page_title = filein.readline().strip()
		filein.close()

		cosin_list.append({'url' : folder_map_url[folder], 'title' : page_title, 'score' : value})

	#Time complexity O(10 *N), where N is the number of page
	result = []
	index = 0
	while index < 10:
		max_score = -1.0
		max_value = {}
		for value in cosin_list:
			value_score = value['score']
			if(value_score> max_score):
				max_score = value_score
				max_value = value

		result.append(max_value)
		cosin_list.remove(max_value)
		index += 1
	return result
