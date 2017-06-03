from sys import argv
from random import randint
from sys import exit
script,file1,file2 = argv
txt1=open(file1)
txt2=open(file2)
matrix = [[0 for x in range(10)]for y in range(10)]
ship_matrix=[[0 for i in range(0,10)]for i in range(0,10)]
# this list will only store whether a cell is a miss('M') or it is unknown('0')
for i in range(10):
	for j in range(10):
		matrix[i][j] = txt1.read(1)
		char = txt1.read(1)

print "Print the input matrix\n"
for i in range(0,10):
	for j in range(0,10):
		print "%c "%matrix[i][j],
	print "\n"	

print "\n\n"
# making a list for storing the states of the five ships and a list to store their lenghts
"""   name         index    symbol   size

	  Carrier		0		C   	5  
	  Battleship	1 		B   	4
	  Cruiser	    2   	R   	3
	  Submarine     3   	S   	3
	  Destroyer     4   	D   	2
"""
for i in range(0,10):
	for j in range(0,10):
		ship_matrix[i][j]=txt2.read(1)
		char=txt2.read(1)

for i in range(0,10):
	for j in range(0,10):
		print "%c "%ship_matrix[i][j],
	print "\n"		


ship_size= [5,4,3,3,2]
shipstate= [1,1,1,1,1]
count_moves=0
#checks whether a given cell lies within the grid and not already tried
def is_valid(i,j):
	if i>-1 and i<10 and j>-1 and j<10 and matrix[i][j]!='M':
		return True
	else:
		return False


# finds the maximum of four values coressopnding to the probabilities of the four neighbour cells once a ship is hit
def maximum():
	#print count
	max_value=count[0]
	max_index=0
	for i in range(1,4):
		if count[i]>max_value:
			max_index=i
			max_value=count[i]

	return max_index	

# matrix that stores the probability distribution of cells on the grid
probability = [[0 for x in range(10)]for y in range(10)]
# this will update the probability of all cells of the matrix which have not been already tried
def hunt_begin():
	for i in range(0,10):
		for j in range(0,10):
			probability[i][j]=0
	for x in range(5):
		if shipstate[x]==1:
			length = ship_size[x]
			for i in range(10):
				count = 0
				initial = 0
				for j in range(10):
					if not (matrix[i][j]=='M'):
						count=count+1
					if (matrix[i][j]=='M') or j==9:
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
					if not (matrix[j][i]=='M'):
						count=count+1
					if (matrix[j][i]=='M') or j==9:
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

# prints the probability matrix
def print_prob():
	for i in range(10):
		for j in range(10):
			print("%d "%probability[i][j]),
		print "\n"


# returns the cell with max probability among all possible(not tried) cells of the matrix
def calc_max_prob():
	max_val = 0
	max_index = [0,0]
	for i in range(0,10):
		for j in range(0,10):
			if probability[i][j]>max_val:
				max_val = probability[i][j]
				max_index = [i,j]
	print("max_index = (%d,%d)"%(max_index[0],max_index[1]))
	return max_index			

# it checks whether a cell given by hunt_begin() contains a ship or not.
# if it does not then updates the values of the row and coloumn and recursively calls again
# if yes, then calls target_mode()
def hunt():	
	max_index = calc_max_prob()
	global count_moves
	if ship_matrix[max_index[0]][max_index[1]] =='0':
		print "Missed,hunt again"	
		count_moves+=1
		matrix[max_index[0]][max_index[1]]='M'
		probability[max_index[0]][max_index[1]]=0
		for x in range(5):
			if shipstate[x] ==1:
				length = ship_size[x]
				count1=0
				count2=0
				for i in range(max_index[1]+1,min(max_index[1]+length,10)):
					if not(matrix[max_index[0]][i] =='M'):
						count1 = count1+1
					else:
						break	
				for i in range(max(max_index[1]-length+1,0),max_index[1]):
					if not(matrix[max_index[0]][i] =='M'):
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
					if not(matrix[i][max_index[1]] =='M'):
						count1 = count1+1
					else:
						break	
				for i in range(max(max_index[0]-length+1,0),max_index[0]):
					if not(matrix[i][max_index[1]] =='M'):
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
		print_prob()
		hunt()
	elif ship_matrix[max_index[0]][max_index[1]] !='0':
		count_moves+=1
		print "Hit- go to target mode"
		char=ship_matrix[max_index[0]][max_index[1]]
		target_mode(max_index[0],max_index[1],char)
		if(all_destroyed()==True):
			print "Game Over"
			print "No. of Moves to finish the game= %d" %(count_moves)
			exit(1)
		else:
			hunt_begin()
			hunt()
			
# the main function which is called once a cell which contains a ship is hit
def target_mode(i,j,char):
	#print "(%d,%d)" %(i,j)
	ship_matrix[i][j]='X'
	probability[i][j]=0
	global count
	global count_moves
	count=[0,0,0,0]
	# to count the possible options for the four neighbours once a cell is hit
	count_horizontal(i,j-1,0)
	count_vertical(i,j-1,0)
	count_horizontal(i-1,j,1)
	count_vertical(i-1,j,1)
	count_horizontal(i,j+1,2)
	count_vertical(i,j+1,2)
	count_horizontal(i+1,j,3)
	count_vertical(i+1,j,3)
	max_index=maximum()
	# deciding the next target
	if max_index==0:
		next_target=[i,j-1]
	elif max_index==1:
		next_target=[i-1,j]
	elif max_index==2:
		next_target=[i,j+1]
	else:
		next_target=[i+1,j]
	print "(%d,%d)" %(next_target[0],next_target[1])
	# if the next target turns a miss recursivevly call the function again
	if ship_matrix[next_target[0]][next_target[1]]=='0':
		count_moves+=1
		print "Missed"
		matrix[next_target[0]][next_target[1]]='M'
		target_mode(i,j,char)
	else:
		count_moves+=1
		print "Hit"
		# update the values of the matrix
		ship_matrix[next_target[0]][next_target[1]]='X'
		matrix[i][j]='M'
		matrix[next_target[0]][next_target[1]]='M'
		probability[next_target[0]][next_target[1]]=0
		# decide the direction
		direction=""
		if max_index==0:
			direction="left"
		elif max_index==1:
			direction="up"
		elif max_index==2:
			direction="right"
		else:
			direction="down"
		#print direction
		if ship_destroyed(i,j,char)==False:
		# call the function to completely destroy the ship
			destroy_ship(direction,next_target[0],next_target[1],i,j,char,0)
			update_shipstate(char)
		else:
			print "the ship %c is completely destroyed,go to hunt mode again" %char
			update_shipstate(char)	
		#print matrix
		#print ship_matrix
# checks whether there are any live ships left	
def all_destroyed():
	flag=1
	for i in shipstate:
		if(i==1):
			flag=0

	if flag==1:
		return True
	else:
		return False

# updates the state of the ships	
def update_shipstate(char):
	if char=='C':
		shipstate[0]=0
	elif char=='B':
		shipstate[1]=0
	elif char=='R':
		shipstate[2]=0
	elif char=='S':
		shipstate[3]=0
	elif char=='D':
		shipstate[4]=0
# to destroy the rest of the ship			
def destroy_ship(direction,i,j,start_i,start_j,char,flag):      # the flag helps us to deal the case of adjacent ships
	global count_moves 
	if direction=="up":
		if(is_valid(i-1,j)):
			if try_cell(i-1,j)==True:
				count_moves+=1
				print "(%d,%d)"%(i-1,j)
				print "Hit"
				ship_matrix[i-1][j]='X'
				matrix[i-1][j]='M'
				probability[i-1][j]=0
				if ship_destroyed(start_i,start_j,char)==False:
					destroy_ship("up",i-1,j,start_i,start_j,char,flag)
				else:
					print "The ship %c is completely destroyed,go to hunt mode again" %char
					return 	
			else:
				count_moves+=1
				print "reverse direction-down"
				destroy_ship("down",start_i,start_j,start_i,start_j,char,1)
		else:
			flag=1
			print "reverse direction-down"
			destroy_ship("down",start_i,start_j,start_i,start_j,char,1)
	elif direction=="left":
		if(is_valid(i,j-1)):
			if try_cell(i,j-1)==True:
				count_moves+=1
				print "(%d,%d)" %(i,j-1)
				print "Hit"
				ship_matrix[i][j-1]='X'
				matrix[i][j-1]='M'
				probability[i][j-1]=0
				if ship_destroyed(start_i,start_j,char)==False:
					destroy_ship("left",i,j-1,start_i,start_j,char,flag)
				else:
					print "The ship %c is completely destroyed,go to hunt mode again" %char
					return
			else:
				flag=1
				count_moves+=1
				print "reverse direction-right"
				destroy_ship("right",start_i,start_j,start_i,start_j,char,1)
		else:
			flag=1
			print "reverse direction-right"
			destroy_ship("right",start_i,start_j,start_i,start_j,char,1)
	elif direction=="down":
		if(is_valid(i+1,j)):
			if try_cell(i+1,j)==True:
				count_moves+=1
				print "(%d,%d)" %(i+1,j)
				print "Hit"
				ship_matrix[i+1][j]='X'
				matrix[i+1][j]='M'
				probability[i+1][j]=0
				if ship_destroyed(start_i,start_j,char)==False:
					destroy_ship("down",i+1,j,start_i,start_j,char,flag)
				else:
					print "The ship %c is completely destroyed,go to hunt mode again" %char
					return	
			else:
				flag=1
				count_moves+=1
				print "reverse direction-up"
				destroy_ship("up",start_i,start_j,start_i,start_j,char,1)
		else:
			flag=1
			print "reverse direction-up"
			destroy_ship("right",start_i,start_j,start_i,start_j,char,1)
			
	else:
		if(is_valid(i,j+1)):
			if try_cell(i,j+1)==True:
				count_moves+=1
				print "(%d,%d)" %(i,j+1)
				print "Hit"
				ship_matrix[i][j+1]='X'
				matrix[i][j+1]='M'
				probability[i][j+1]=0
				print ship_destroyed(start_i,start_j,char)
				if ship_destroyed(start_i,start_j,char)==False:
					destroy_ship("right",i,j+1,start_i,start_j,char,flag)
				else:
					print "The ship %c is completely destroyed,go to hunt mode again" %char
					return	
			else:
				flag=1
				count_moves+=1
				print "reverse direction-left"
				destroy_ship("left",start_i,start_j,start_i,start_j,char,1)
		else:
			flag=1
			print "reverse direction-left"
			destroy_ship("left",start_i,start_j,start_i,start_j,char,1)
# checks whether a cell contains a ship or not
# can use a parameter char to check for a particular ship
def try_cell(i,j):
	if ship_matrix[i][j]!='0':  # check this
		return True
	else:
		return False	
# checks whether the ship has been completely destroyed
def ship_destroyed(i,j,char):
	flag=1
	for k in range(0,10):
		if ship_matrix[i][k]==char:
			flag=0

	for k in range(0,10):
		if ship_matrix[k][j]==char:
			flag=0

	if flag==0:
		return False
	else:
		return True					


# counts the number of ways to place all(alive) ships horizontally such that they pass through (i,j)
def count_horizontal(i,j,index):
	idx=0
	for size in ship_size:
		if shipstate[idx]==0:
			idx+=1
			continue

		if is_valid(i,j)==True:
			for k in range(j-(size-1),j+1):
				if is_valid(i,k)==True:
					for m in range(0,size):
						flag=1
						if(is_valid(i,k+m)==False):
							flag=0
							break

					if flag==1:
						count[index]+=1
	idx+=1
			
# counts the number of ways to place all(alive) ships vertically such that they pass through (i,j)
def count_vertical(i,j,index):
	idx=0
	for size in ship_size:
		if shipstate[idx]==0:
			idx+=1
			continue

		if is_valid(i,j)==True:
			for k in range(i-(size-1),i+1):
				if is_valid(k,j):
					for m in range(0,size):
						flag=1
						if(is_valid(k+m,j)==False):
							flag=0
							break

					if flag==1:
						count[index]+=1
	idx+=1


hunt_begin()
hunt()			

	



		
						
