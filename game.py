from sys import argv
script,file1,file2 = argv
txt1 = open(file1)
txt2 = open(file2)
player1 = [[0 for x in range(10)]for y in range(10)]
player2 = [[0 for x in range(10)]for y in range(10)]
ship_player1=[[0 for x in range(10)]for y in range(10)]
ship_player2=[[0 for x in range(10)]for y in range(10)]
ship1 = [1,1,1,1,1]
ship2 = [1,1,1,1,1]
ships = ['C','B','R','S','D']
matrix1=[[0 for x in range(10)]for y in range(10)]
matrix2=[[0 for x in range(10)]for y in range(10)]
for i in range(10):
	for j in range(10):
		matrix1[i][j]='0'
		player1[i][j] = txt1.read(1)
		char = txt1.read(1)

for i in range(10):
	for j in range(10):
		matrix2[i][j]='0'
		player2[i][j] = txt2.read(1)
		char = txt2.read(1)

for i in range(10):
	for j in range(10):
		ship_player1[i][j]=player1[i][j]
		ship_player2[i][j]=player2[i][j]
#when a ship is completely destroyed update the matrix
def update_ship_matrix(player,ch):
	for i in range(0,10):
		for j in range(0,10):
			if(player==2):
				if ship_player2[i][j]==ch:
					matrix1[i][j]=ch
			else:
				if ship_player1[i][j]==ch:
					matrix2[i][j]=ch		



def print_matrix(matrix):
	print "  |",
	for i in range(0,10):
		print "%d "%(i),
	print "\n------------------------------------"
	for i in range(0,10):
		print "%d |"%(i),
		for j in range(0,10):
			if j==9:
				print "%c\n"%matrix[i][j],
			else:
				print "%c "%matrix[i][j],
	print "\n\n"		

def destroyed(ch,player):
	if ch =='C':
		print("You have destroyed the Carrier")
	if ch =='B':
		print("You have destroyed the Battleship")
	if ch == 'R':
		print("You have destroyed the Crusier")
	if ch == 'S':
		print("You have destroyed the Submarine")
	if ch == 'D':
		print("You have destroyed the Destroyer")

	update_ship_matrix(player,ch)	

#searches if a particular ship has completely been destroyed or if all the ships have been destroyed
def search(player,matrix):
	for ch in ships:
		count=0
		if (player==1 and ship1[ships.index(ch)]==1) or (player==2 and ship2[ships.index(ch)]==1):
			for i in range(10):
				for j in range(10):
					if matrix[i][j]==ch:
						count=count+1
			if count==0:
				if player ==1:
					ship1[ships.index(ch)]=0
					destroyed(ch,player)
				if player ==2:
					ship2[ships.index(ch)]=0
					destroyed(ch,player)

	if player==1:
		flag = 0
		for i in range(5):
			if ship1[i]==1:
				flag=1
				break
		if flag==0:
			print("You have destroyed all ships.\nYou won!")
			return 1

	if player==2:
		flag=0
		for i in range(5):
			if ship2[i]==1:
				flag=1
				break
		if flag==0:
			print("You have destroyed all ships.\nYou won!")
			return 1
	return 0

while(True):				
	print("Player1: Enter the coordinates:")		
	x = int(input())
	y = int(input())
	#test if it is a hit
	if(player2[x][y]=='C' or player2[x][y]=='B' or player2[x][y]=='R' or player2[x][y]=='S' or player2[x][y]=='D'):
		print("Hit")
		player2[x][y]='X'
		matrix1[x][y]='H'
		#check if the game is over or if a ship is completely destroyed
		if search(2,player2)==1:
			break
	else:
		print("Miss")
		matrix1[x][y]='M'
	#do same for second player	
	print("Player2: Enter the coordinates:")		
	i = int(input())
	j = int(input())
	if(player1[i][j]=='C' or player1[i][j]=='B' or player1[i][j]=='R' or player1[i][j]=='S' or player1[i][j]=='D'):
		print("Hit")
		player1[i][j]='X'
		matrix2[i][j]='H'
		if search(1,player1)==1:
			break
	else:
		print("Miss")
		matrix2[i][j]='M'	
	print_matrix(matrix1)
	print_matrix(matrix2)											
