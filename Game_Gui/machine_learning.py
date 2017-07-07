
import pickle

def update_x(letter):
	for i in range(100):
		if ship_matrix1[i]==letter:
			x[0][i]=-1


def print_message(letter):
	if letter=='C':
		print "AI sunk your Carrier"
	elif letter=='D':
		print "AI sunk your Destroyer"
	elif letter=='R':
		print "AI sunk your Cruiser"
	elif letter=='B':
		print "AI sunk your Battleship"
	else:
		print "AI sunk your Submarine"

def update_shipstate(letter):
	if letter=='C':
		ship_state[0]=0
	elif letter=='B':
		ship_state[1]=0
	elif letter=='R':
		ship_state[2]=0
	elif letter=='S':
		ship_state[3]=0
	elif letter=='D':
		ship_state[4]=0

def all_destroyed():
	flag=0
	for i in ship_state:
		if i==1:
			flag=1								
	if flag==0:
		return True
	else:
		return False


def game():
	model1=pickle.load(open('1.sav','rb'))	
	model2=pickle.load(open('2.sav','rb'))
	model3=pickle.load(open('3.sav','rb'))
	model4=pickle.load(open('4.sav','rb'))
	model5=pickle.load(open('5.sav','rb'))
	model6=pickle.load(open('6.sav','rb'))
	model7=pickle.load(open('7.sav','rb'))
	model8=pickle.load(open('8.sav','rb'))
	model9=pickle.load(open('9.sav','rb'))
	model10=pickle.load(open('10.sav','rb'))
	model11=pickle.load(open('11.sav','rb'))
	model12=pickle.load(open('12.sav','rb'))
	model13=pickle.load(open('13.sav','rb'))
	model14=pickle.load(open('14.sav','rb'))
	model15=pickle.load(open('15.sav','rb'))
	model16=pickle.load(open('16.sav','rb'))
	model17=pickle.load(open('17.sav','rb'))
	model18=pickle.load(open('18.sav','rb'))
	model19=pickle.load(open('19.sav','rb'))
	model20=pickle.load(open('20.sav','rb'))
	model21=pickle.load(open('21.sav','rb'))
	model22=pickle.load(open('22.sav','rb'))
	model23=pickle.load(open('23.sav','rb'))
	model24=pickle.load(open('24.sav','rb'))
	model25=pickle.load(open('25.sav','rb'))
	model26=pickle.load(open('26.sav','rb'))
	model27=pickle.load(open('27.sav','rb'))
	model28=pickle.load(open('28.sav','rb'))
	model29=pickle.load(open('29.sav','rb'))
	model30=pickle.load(open('30.sav','rb'))
	model31=pickle.load(open('31.sav','rb'))
	model32=pickle.load(open('32.sav','rb'))
	model33=pickle.load(open('33.sav','rb'))
	model34=pickle.load(open('34.sav','rb'))
	model35=pickle.load(open('35.sav','rb'))
	model36=pickle.load(open('36.sav','rb'))
	model37=pickle.load(open('37.sav','rb'))
	model38=pickle.load(open('38.sav','rb'))
	model39=pickle.load(open('39.sav','rb'))
	model40=pickle.load(open('40.sav','rb'))
	model41=pickle.load(open('41.sav','rb'))
	model42=pickle.load(open('42.sav','rb'))
	model43=pickle.load(open('43.sav','rb'))
	model44=pickle.load(open('44.sav','rb'))
	model45=pickle.load(open('45.sav','rb'))
	model46=pickle.load(open('46.sav','rb'))
	model47=pickle.load(open('47.sav','rb'))
	model48=pickle.load(open('48.sav','rb'))
	model49=pickle.load(open('49.sav','rb'))
	model50=pickle.load(open('50.sav','rb'))
	model51=pickle.load(open('51.sav','rb'))
	model52=pickle.load(open('52.sav','rb'))
	model53=pickle.load(open('53.sav','rb'))
	model54=pickle.load(open('54.sav','rb'))
	model55=pickle.load(open('55.sav','rb'))
	model56=pickle.load(open('56.sav','rb'))
	model57=pickle.load(open('57.sav','rb'))
	model58=pickle.load(open('58.sav','rb'))
	model59=pickle.load(open('59.sav','rb'))
	model60=pickle.load(open('60.sav','rb'))
	model61=pickle.load(open('61.sav','rb'))
	model62=pickle.load(open('62.sav','rb'))
	model63=pickle.load(open('63.sav','rb'))
	model64=pickle.load(open('64.sav','rb'))
	model65=pickle.load(open('65.sav','rb'))
	model66=pickle.load(open('66.sav','rb'))
	model67=pickle.load(open('67.sav','rb'))
	model68=pickle.load(open('68.sav','rb'))
	model69=pickle.load(open('69.sav','rb'))
	model70=pickle.load(open('70.sav','rb'))
	model71=pickle.load(open('71.sav','rb'))
	model72=pickle.load(open('72.sav','rb'))
	model73=pickle.load(open('73.sav','rb'))
	model74=pickle.load(open('74.sav','rb'))
	model75=pickle.load(open('75.sav','rb'))
	model76=pickle.load(open('76.sav','rb'))
	model77=pickle.load(open('77.sav','rb'))
	model78=pickle.load(open('78.sav','rb'))
	model79=pickle.load(open('79.sav','rb'))
	model80=pickle.load(open('80.sav','rb'))
	model81=pickle.load(open('81.sav','rb'))
	model82=pickle.load(open('82.sav','rb'))
	model83=pickle.load(open('83.sav','rb'))
	model84=pickle.load(open('84.sav','rb'))
	model85=pickle.load(open('85.sav','rb'))
	model86=pickle.load(open('86.sav','rb'))
	model87=pickle.load(open('87.sav','rb'))
	model88=pickle.load(open('88.sav','rb'))
	model89=pickle.load(open('89.sav','rb'))
	model90=pickle.load(open('90.sav','rb'))
	model91=pickle.load(open('91.sav','rb'))
	model92=pickle.load(open('92.sav','rb'))
	model93=pickle.load(open('93.sav','rb'))
	model94=pickle.load(open('94.sav','rb'))
	model95=pickle.load(open('95.sav','rb'))
	model96=pickle.load(open('96.sav','rb'))
	model97=pickle.load(open('97.sav','rb'))
	model98=pickle.load(open('98.sav','rb'))
	model99=pickle.load(open('99.sav','rb'))
	model100=pickle.load(open('100.sav','rb'))
	count=0
	while True:
		prediction[0]=model1.predict(x)
		prediction[1]=model2.predict(x)
		prediction[2]=model3.predict(x)
		prediction[3]=model4.predict(x)
		prediction[4]=model5.predict(x)
		prediction[5]=model6.predict(x)
		prediction[6]=model7.predict(x)
		prediction[7]=model8.predict(x)
		prediction[8]=model9.predict(x)
		prediction[9]=model10.predict(x)
		prediction[10]=model11.predict(x)
		prediction[11]=model12.predict(x)
		prediction[12]=model13.predict(x)
		prediction[13]=model14.predict(x)
		prediction[14]=model15.predict(x)
		prediction[15]=model16.predict(x)
		prediction[16]=model17.predict(x)
		prediction[17]=model18.predict(x)
		prediction[18]=model19.predict(x)
		prediction[19]=model20.predict(x)
		prediction[20]=model21.predict(x)
		prediction[21]=model22.predict(x)
		prediction[22]=model23.predict(x)
		prediction[23]=model24.predict(x)
		prediction[24]=model25.predict(x)
		prediction[25]=model26.predict(x)
		prediction[26]=model27.predict(x)
		prediction[27]=model28.predict(x)
		prediction[28]=model29.predict(x)
		prediction[29]=model30.predict(x)
		prediction[30]=model31.predict(x)
		prediction[31]=model32.predict(x)
		prediction[32]=model33.predict(x)
		prediction[33]=model34.predict(x)
		prediction[34]=model35.predict(x)
		prediction[35]=model36.predict(x)
		prediction[36]=model37.predict(x)
		prediction[37]=model38.predict(x)
		prediction[38]=model39.predict(x)
		prediction[39]=model40.predict(x)
		prediction[40]=model41.predict(x)
		prediction[41]=model42.predict(x)
		prediction[42]=model43.predict(x)
		prediction[43]=model44.predict(x)
		prediction[44]=model45.predict(x)
		prediction[45]=model46.predict(x)
		prediction[46]=model47.predict(x)
		prediction[47]=model48.predict(x)
		prediction[48]=model49.predict(x)
		prediction[49]=model50.predict(x)
		prediction[50]=model51.predict(x)
		prediction[51]=model52.predict(x)
		prediction[52]=model53.predict(x)
		prediction[53]=model54.predict(x)
		prediction[54]=model55.predict(x)
		prediction[55]=model56.predict(x)
		prediction[56]=model57.predict(x)
		prediction[57]=model58.predict(x)
		prediction[58]=model59.predict(x)
		prediction[59]=model60.predict(x)
		prediction[60]=model61.predict(x)
		prediction[61]=model62.predict(x)
		prediction[62]=model63.predict(x)
		prediction[63]=model64.predict(x)
		prediction[64]=model65.predict(x)
		prediction[65]=model66.predict(x)
		prediction[66]=model67.predict(x)
		prediction[67]=model68.predict(x)
		prediction[68]=model69.predict(x)
		prediction[69]=model70.predict(x)
		prediction[70]=model71.predict(x)
		prediction[71]=model72.predict(x)
		prediction[72]=model73.predict(x)
		prediction[73]=model74.predict(x)
		prediction[74]=model75.predict(x)
		prediction[75]=model76.predict(x)
		prediction[76]=model77.predict(x)
		prediction[77]=model78.predict(x)
		prediction[78]=model79.predict(x)
		prediction[79]=model80.predict(x)
		prediction[80]=model81.predict(x)
		prediction[81]=model82.predict(x)
		prediction[82]=model83.predict(x)
		prediction[83]=model84.predict(x)
		prediction[84]=model85.predict(x)
		prediction[85]=model86.predict(x)
		prediction[86]=model87.predict(x)
		prediction[87]=model88.predict(x)
		prediction[88]=model89.predict(x)
		prediction[89]=model90.predict(x)
		prediction[90]=model91.predict(x)
		prediction[91]=model92.predict(x)
		prediction[92]=model93.predict(x)
		prediction[93]=model94.predict(x)
		prediction[94]=model95.predict(x)
		prediction[95]=model96.predict(x)
		prediction[96]=model97.predict(x)
		prediction[97]=model98.predict(x)
		prediction[98]=model99.predict(x)
		prediction[99]=model100.predict(x)

		m=-1000000000
		max_index=0
		for i in range(0,100):
			if(prediction[i]>m and x[0][i]==0):
				m=prediction[i]
				max_index=i

		boxy = max_index%10
		boxx = max_index/10

		txt3.write(str(boxx))
		txt3.write(str(boxy)) 		

		count+=1		
		

		if ship_matrix[max_index]!='0':
			x[0][max_index]=1
			letter=ship_matrix[max_index]
			ship_matrix[max_index]='0'
			flag=0
			for i in range(100):
				if(ship_matrix[i]==letter):
					flag=1
			if flag==0:
				update_x(letter)
				
				update_shipstate(letter)
				if all_destroyed()==True:
					break	
		else:
			x[0][max_index]=-1
	txt3.close()		


def main():
	import os
	from subprocess import call
	global ship_matrix,ship_matrix1,txt3,x,ship_state,prediction,txt3
	ship_matrix=['0' for x in range(100)]
	ship_matrix1=['0' for x in range(100)]
	txt3 = open('moves.txt','w')

	x=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
	ship_state=[1,1,1,1,1]
	
	prediction=[0 for i in range(0,100)]	

	txt2=open('no_of_moves.txt','a')

	txt=open('player1.txt')
	for j in range(100):
		ship_matrix[j]=txt.read(1)
		char=txt.read(1)
		ship_matrix1[j]=ship_matrix[j]
		

	for j in range(0,100):
		x[0][j]=0
	
	for j in range(0,5):
		ship_state[j]=1	 	
	game()


