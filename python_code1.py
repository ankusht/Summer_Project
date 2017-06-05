from sys import argv
script,num = argv
num=int(num)
flag=0
for i in range(2,num/2):
	if num%i==0:
		flag=1
		break
if flag==0:
	print("Prime Number")
else:
	print("Composite Number")			