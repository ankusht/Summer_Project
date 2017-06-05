from sys import argv
from random import randint
script,file = argv
txt = open(file)
matrix = [[0 for x in range(10)]for y in range(10)]
for i in range(10):
	for j in range(10):
		matrix[i][j] = txt.read(1)
		char = txt.read(1)
'''for i in range(10):
	for j in range(10):
		print("%r "%matrix[i][j]),
	print "\n"'''

ships = [5,4,3,3,2]
sunk = [0,0,0,0,0]
probability = [[0 for x in range(10)]for y in range(10)]
#calculate and fill the probability matrix given the state of ship: whether a cell has been checked or not
def hunt_begin():
	for x in range(5):
		if sunk[x]==0:
			length = ships[x]
			for i in range(10):
				count = 0
				initial = 0
				for j in range(10):
					if not (matrix[i][j]=='M' or matrix[i][j]=='H'):
						count=count+1
					if (matrix[i][j]=='M' or matrix[i][j]=='H') or j==9:
						if count>=length:
							max_value = count-length+1
							if max_value>length:
								max_value=length
							value=1
							start = initial
							end = initial+count-1
							while start<=end:
								if(value>max_value):
									value = max_value
								if start!=end:
									probability[i][start]=probability[i][start]+value
									probability[i][end]=probability[i][end]+value
								else:
									probability[i][start]=probability[i][start]+value
								start+=1
								end-=1
								value+=1			

						initial = j+1
						count=0
			for i in range(10):
				count = 0
				initial = 0
				for j in range(10):
					if not (matrix[j][i]=='M' or matrix[j][i]=='H'):
						count=count+1
					if (matrix[j][i]=='M' or matrix[j][i]=='H') or j==9:
						if count>=length:
							max_value = count-length+1
							if max_value>length:
								max_value=length
							value=1
							start = initial
							end = initial+count-1
							while start<=end:
								if(value>max_value):
									value=max_value
								if start!=end:
									probability[start][i]=probability[start][i]+value
									probability[end][i]=probability[end][i]+value
								else:
									probability[start][i]=probability[start][i]+value	
								start+=1
								end-=1
								value+=1			
						initial = j+1
						count=0
	print_prob()

def print_prob():
	for i in range(10):
		for j in range(10):
			print("%d "%probability[i][j]),
		print "\n"

hunt_begin()
#find the cell with maximum probability
def calc_max_prob():
	max_val = 0
	max_index = [0,0]
	for i in range(10):
		for j in range(10):
			if probability[i][j]>max_val:
				max_val = probability[i][j]
				max_index = [i,j]
	print("max_index = %d %d\n"%(max_index[0],max_index[1]))
	return max_index			


def hunt():	
	max_index = calc_max_prob()
	#if the cell was a miss update the probability in the row and column containing the cell and call the function again
	if matrix[max_index[0]][max_index[1]] =='0':
		matrix[max_index[0]][max_index[1]]='M'
		probability[max_index[0]][max_index[1]]=0
		for x in range(5):
			if sunk[x] ==0:
				length = ships[x]
				count1=0
				count2=0
				for i in range(max_index[1]+1,min(max_index[1]+length,10)):
					if not(matrix[max_index[0]][i] =='M' or matrix[max_index[0]][i] =='H'):
						count1 = count1+1
					else:
						break	
				for i in range(max(max_index[1]-length+1,0),max_index[1]):
					if not(matrix[max_index[0]][i] =='M' or matrix[max_index[0]][i] =='H'):
						count2 = count2+1
					else:
						break
				value = 1
				for i in xrange(max_index[1]+count1,max_index[1],-1):
					probability[max_index[0]][i] = probability[max_index[0]][i] - value
					value = value+1
				value=1	
				for i in range(max_index[1]-count2,max_index[1]):
					probability[max_index[0]][i] = probability[max_index[0]][i] - value
					value = value+1	

				count1=0
				count2=0
				for i in range(max_index[0]+1,min(max_index[0]+length,10)):
					if not(matrix[i][max_index[1]] =='M' or matrix[i][max_index[1]] =='H'):
						count1 = count1+1
					else:
						break	
				for i in range(max(max_index[0]-length+1,0),max_index[0]):
					if not(matrix[i][max_index[1]] =='M' or matrix[i][max_index[1]] =='H'):
						count2 = count2+1
					else:
						break
				value = 1
				for i in xrange(max_index[0]+count1,max_index[0],-1):
					probability[i][max_index[1]] = probability[i][max_index[1]] - value
					value = value+1
				value=1	
				for i in range(max_index[0]-count2,max_index[0]):
					probability[i][max_index[1]] = probability[i][max_index[1]] - value
					value = value+1
		print "\n"
		print_prob()
		hunt()


hunt()					

	



		
						
