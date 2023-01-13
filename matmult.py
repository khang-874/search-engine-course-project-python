import math
#Part 1
def mult_scalar(matrix, scale):
	result_matrix = []
	#Go through each row of the matrix
	for row in range(len(matrix)):
		temp_matrix = []
		#Go through the whole row and time it with the scale
		for column in range(len(matrix[row])):
			temp_matrix.append(matrix[row][column] * scale)
		result_matrix.append(temp_matrix)
	return result_matrix

#Part 2
def mult_matrix(a, b):
	number_of_row_a = len(a)
	number_of_column_a = len(a[0])
	number_of_column_b = len(b[0])
	number_of_row_b = len(b)
	if(number_of_column_a != number_of_row_b):
		return None


	result_matrix = []

	for row_a in range(number_of_row_a):
		temp_matrix = []
		#Calculating the dot product between each column of matrix b with the current row_a row
		for column_b in range(number_of_column_b):
			sum = 0
			#Matching each pair number
			#The column of matrix A will match with the row of matrix B
			for column_a in range(number_of_column_a):
				sum += a[row_a][column_a] * b[column_a][column_b]
			temp_matrix.append(sum)

		result_matrix.append(temp_matrix)
	return result_matrix

#Part 3
def euclidean_dist(a,b):
	result = 0.0
	for index in range(len(a[0])):
		result += (a[0][index] - b[0][index])**2
	return math.sqrt(result)

