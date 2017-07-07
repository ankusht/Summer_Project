
#place the ship horizontally
def write_at_x(a,b,x,l):
	for i in range(b,b+l):
		matrix[a][i]=x
		
#place the ship vertically
def write_at_y(a,b,x,l):
	for i in range(a,a+l):
		matrix[i][b] = x

#checks if placed ship is adjecent with previously placed ship.
def checkIfAdjecent(a,b,d,l):
	if d==0:
		for i in range(b,b+l):
			if (a-1>=0 and matrix[a-1][i] in ships) or (a+1<=9 and matrix[a+1][i] in ships):
				return False
	else:
		for i in range(a,a+l):
			if (b-1>=0 and matrix[i][b-1] in ships) or (b+1<=9 and matrix[i][b+1] in ships):
				return False

	return True						

#check if the ship can be placed at the random coordinates
def check(a,b,d,l):
	flag=0
	if d==0:
		if b+l>10:
			return False
		for i in range(b,b+l):
			if (matrix[a][i] in ships) or (b+l<=9 and matrix[a][b+l] in ships) or (b-1>=0 and matrix[a][b-1] in ships):
				flag=1
				break
		if flag==1 or not(checkIfAdjecent(a,b,d,l)):
			return False
		else:
			return True
	else:
		if a+l>10:
			return False
		for i in range(a,a+l):
			if (matrix[i][b] in ships) or (a+l<=9 and matrix[a+l][b] in ships) or (a-1>=0 and matrix[a-1][b] in ships):
				flag=1
				break
		if flag==1 or not(checkIfAdjecent(a,b,d,l)):
			return False
		else:
			return True
										

#place all the ships
def main():
	from random import randint
	global matrix,ships,length
	matrix = [['0' for x in range(10)]for y in range(10)]
	ships = ['C','B','R','S','D']
	length = [5,4,3,3,2]		

	txt = open('ships.txt','w')
	ship =""
	idx=0
	for x in ships:
		while(True):
			a = randint(0,9)
			b = randint(0,9)
			direction = randint(0,1)
			if(direction==0):
				if not(check(a,b,direction,length[idx])):
					continue
				else:
					write_at_x(a,b,x,length[idx])
					break
			else:
				if not(check(a,b,direction,length[idx])):
					continue
				else:
					write_at_y(a,b,x,length[idx])
					break			
		idx=idx+1			

	for i in range(10):
		for j in range(10):
			if j!=9:
				ship+=matrix[i][j]+" "
			else:
				ship+=matrix[i][j]+"\n"			

	txt.write(ship)
	txt.close()			