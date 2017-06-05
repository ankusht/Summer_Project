from sys import argv
script,key=argv
key=int(key)
array = [2,5,8,13,25,36,44,58,64]
def binary_search(s,e):
	if s>e:
		print("Key not found")
		return
	m = (s+e)/2
	if array[m]==key:
		print("Key found")
	elif array[m]<key:
		binary_search(m+1,e)
	else:
		binary_search(s,m-1)

binary_search(0,8)