import os
import pygame, sys
from pygame.locals import*
import setting_ships
import probability
import machine_learning
import time

ShipState1 = [1,1,1,1,1]
ShipState2=[1,1,1,1,1]
Ships = ['C','B','R','S','D']
movePlayer1 = 0
movePlayer2 = 0

FPS = 100
WINDOW_SIZEX = 1366
WINDOW_SIZEY = 768
BOX_SIZE = 30
GAP_SIZE = 10
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 30
BIG_GAP = 50
BOARD_SIZE = 10
XMARGIN = int((WINDOW_SIZEX- BOARD_SIZE*(BOX_SIZE+GAP_SIZE)*2 - BIG_GAP)/2)
YMARGIN = int((WINDOW_SIZEY - BOARD_SIZE*(BOX_SIZE+GAP_SIZE))/2)

WHITE = (255,255,255)
NAVYBLUE = (60,60,100)
RED = (255,0,0)
LIGHTRED = (200,0,0)
GREEN = (0,255,0)
LIGHTGREEN = (0,100,0)
GRAY = (100,100,100)
BLUE = ( 0,0,255)
YELLOW = (100,100,0)
LIGHT_YELLOW = (255,255,0)
BLACK = (0,0,0)
BROWN = (205,133,63)
VIOLET = (177, 120, 211)
PLACE = BROWN
ORANGE = (255,165,0)

occupied=[[0 for i in range(0,10)]for j in range(0,10)]
already_occupied = [[0 for i in range(0,10)]for j in range(0,10)]

BackgroundImage = pygame.image.load('background.png')
BackgroundImage = pygame.transform.smoothscale(BackgroundImage, (WINDOW_SIZEX,WINDOW_SIZEY))

pygame.mixer.init(44100, -16, 2, 2048)
ClickSound = pygame.mixer.Sound('Click.wav')

def main():
	global movePlayer1,movePlayer2
	movePlayer1 = -1
	movePlayer2 = -1

	global mode

	setting_ships.main()
	global FPS, DISPLAYSURF
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
	global mainboardPlayer1,mainboardPlayer1Copy
	mainboardPlayer1 = [['0' for i in range(BOARD_SIZE)]for j in range(BOARD_SIZE)]
	mainboardPlayer1Copy = [['0' for i in range(BOARD_SIZE)]for j in range(BOARD_SIZE)]
	global mainboardPlayer2,mainboardPlayer2Copy
	mainboardPlayer2 = getRandomizedBoard()
	mainboardPlayer2Copy = copyBoard(mainboardPlayer2)

	mousex = 0
	mousey = 0
	pygame.display.set_caption('Battleship Game')

	DISPLAYSURF.fill(WHITE)
	mode = drawStartBoard1()
	drawStartBoard2()

	#placing the ships
	placing_ships_vertical(None,5)
	getTheBoard('C')
	placing_ships_vertical(None,4)
	getTheBoard('B')
	placing_ships_vertical(None,3)
	getTheBoard('R')
	placing_ships_vertical(None,3)
	getTheBoard('S')
	placing_ships_vertical(None,2)
	getTheBoard('D')

	writeBoardToFile()

	if mode == 1:
		probability.main()
	elif mode == 2:
		machine_learning.main()

	global txt
	txt = open('moves.txt')	

	global Turn
	Turn = 1
	while True:

		DISPLAYSURF.fill(WHITE)
		drawboard()

		mouseclicked = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONUP:
				mousex,mousey = event.pos
				mouseclicked = True
			elif event.type == MOUSEMOTION:
				mousex,mousey = event.pos
		boxx,boxy,number = getBoxAtPixel(mousex,mousey)
		if boxx!=None and boxy!=None:
			drawHighlightBox(boxx,boxy,number)

		if Turn == 2:
			y = int(txt.read(1))
			x = int(txt.read(1))
			if onClick(x,y,mainboardPlayer1,1):
				Turn = 1 
				
		if mouseclicked:
			if clickedExit(mousex,mousey):
				pygame.quit()
				sys.exit()

			if boxx!=None and boxy!=None and number==2 and Turn==1:
				if onClick(boxx,boxy,mainboardPlayer2,number):
					playClickSound()
					Turn = 2
		pygame.display.update()
		FPSCLOCK.tick(FPS)	

def clickedExit(mousex,mousey):
	if EXITX < mousex < EXITX + BUTTON_WIDTH and EXITY < mousey < EXITY + BUTTON_WIDTH:
		drawButtonPush(EXITX,EXITY,BUTTON_WIDTH,BUTTON_HEIGHT,YELLOW,LIGHT_YELLOW,"Exit",BLACK)
		return True
	return False	

def writeBoardToFile():
	txt = open('player1.txt','w')
	ship = ""
	for x in range(BOARD_SIZE):
		for y in range(BOARD_SIZE):
			if y!=BOARD_SIZE-1:
				ship+=mainboardPlayer1[x][y]+" "
			else:
				ship+=mainboardPlayer1[x][y]+"\n"
	txt.write(ship)				

def drawStartBoard2():
	DISPLAYSURF.blit(BackgroundImage,(0,0))
	x = XMARGIN
	y = int(YMARGIN/3)
	fontObj = pygame.font.Font('freesansbold.ttf',16)
	textSurfaceObj = fontObj.render('Place your ships',True,WHITE)
	DISPLAYSURF.blit(textSurfaceObj,(x,y))
	x1  = x
	y1 =  y + 30
	x2 = x1 + BUTTON_WIDTH + 20
	y2 = y1

	x5 = XMARGIN + BOARD_SIZE*(BOX_SIZE+GAP_SIZE) + BIG_GAP + 2*BUTTON_WIDTH + 40
	y5 = y1 - 50

	drawButton(x1,y1,BUTTON_WIDTH,BUTTON_HEIGHT,LIGHTGREEN,LIGHTGREEN,"Turn(T)")
	drawButton(x2,y2,BUTTON_WIDTH,BUTTON_HEIGHT,LIGHTGREEN,LIGHTGREEN,"Place(Enter)")
	drawButton(x5,y5,BUTTON_WIDTH,BUTTON_HEIGHT,YELLOW,LIGHT_YELLOW,"Instructions")
	drawButton(EXITX,EXITY,BUTTON_WIDTH,BUTTON_HEIGHT,YELLOW,LIGHT_YELLOW,"Exit")

	BORDERSIZE = BOARD_SIZE*(BOX_SIZE+GAP_SIZE) -GAP_SIZE +10

	pygame.draw.rect(DISPLAYSURF,ORANGE,(XMARGIN-5,YMARGIN-5,BORDERSIZE,BORDERSIZE),3)
	pygame.draw.rect(DISPLAYSURF,ORANGE,(XMARGIN+BOARD_SIZE*(BOX_SIZE+GAP_SIZE)+BIG_GAP-5,YMARGIN-5,BORDERSIZE,BORDERSIZE),3)

	for boxx in range(BOARD_SIZE):
		for boxy in range(BOARD_SIZE):
			box_rect = leftcordsofbox(boxx,boxy,1)
			pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)

	for boxx in range(BOARD_SIZE):
		for boxy in range(BOARD_SIZE):
			box_rect = leftcordsofbox(boxx,boxy,2)
			pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)


def drawStartBoard1():
	while True:
		DISPLAYSURF.blit(BackgroundImage,(0,0))

		y = int(YMARGIN/3)
		y1 = y+30
		
		x3 = XMARGIN+ BOARD_SIZE*(BOX_SIZE+GAP_SIZE) + BIG_GAP
		y3 = y1
		x4 = x3 + BUTTON_WIDTH + 20
		y4 = y1

		x5 = XMARGIN + BOARD_SIZE*(BOX_SIZE+GAP_SIZE) + BIG_GAP + 2*BUTTON_WIDTH + 40
		y5 = y1 - 50


		global EXITX,EXITY
		EXITX = WINDOW_SIZEX - int(XMARGIN/3) - BUTTON_WIDTH
		EXITY = WINDOW_SIZEY - int(YMARGIN/3) - BUTTON_HEIGHT

		fontObj = pygame.font.Font('freesansbold.ttf',16)
		textSurfaceObj = fontObj.render('Select the Mode',True,WHITE)
		DISPLAYSURF.blit(textSurfaceObj,(x3,y))	

		drawButton(x3,y3,BUTTON_WIDTH,BUTTON_HEIGHT,YELLOW,LIGHT_YELLOW,"Probability")
		drawButton(x4,y4,BUTTON_WIDTH,BUTTON_HEIGHT,YELLOW,LIGHT_YELLOW,"Learning")
		drawButton(x5,y5,BUTTON_WIDTH,BUTTON_HEIGHT,YELLOW,LIGHT_YELLOW,"Instructions")
		drawButton(EXITX,EXITY,BUTTON_WIDTH,BUTTON_HEIGHT,YELLOW,LIGHT_YELLOW,"Exit")

		BORDERSIZE = BOARD_SIZE*(BOX_SIZE+GAP_SIZE) -GAP_SIZE +10

		pygame.draw.rect(DISPLAYSURF,ORANGE,(XMARGIN-5,YMARGIN-5,BORDERSIZE,BORDERSIZE),3)
		pygame.draw.rect(DISPLAYSURF,ORANGE,(XMARGIN+BOARD_SIZE*(BOX_SIZE+GAP_SIZE)+BIG_GAP-5,YMARGIN-5,BORDERSIZE,BORDERSIZE),3)


		for boxx in range(BOARD_SIZE):
			for boxy in range(BOARD_SIZE):
				box_rect = leftcordsofbox(boxx,boxy,1)
				pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)

		for boxx in range(BOARD_SIZE):
			for boxy in range(BOARD_SIZE):
				box_rect = leftcordsofbox(boxx,boxy,2)
				pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)


		for event in pygame.event.get():
			if event.type == MOUSEBUTTONUP:
				x,y = event.pos
				if x3 < x < x3+BUTTON_WIDTH and y3 < y < y3+BUTTON_HEIGHT:
					drawButtonPush(x3,y3,BUTTON_WIDTH,BUTTON_HEIGHT,YELLOW,LIGHT_YELLOW,"Probability",BLACK)
					return 1
				elif x4 < x < x4+BUTTON_WIDTH and y4 < y < y4+BUTTON_HEIGHT:
					drawButtonPush(x4,y4,BUTTON_WIDTH,BUTTON_HEIGHT,YELLOW,LIGHT_YELLOW,"Learning",BLACK)
					return 2
				elif x5 < x < x5 + BUTTON_WIDTH and y5 < y < y5 + BUTTON_HEIGHT:
					drawButtonPush(x5,y5,BUTTON_WIDTH,BUTTON_HEIGHT,YELLOW,LIGHT_YELLOW,"Instructions",BLACK)
					ShowInstructions()
					DISPLAYSURF.fill(WHITE)
				elif EXITX < x < EXITX+BUTTON_WIDTH and EXITY < y < EXITY + BUTTON_HEIGHT:
					drawButtonPush(EXITX,EXITY,BUTTON_WIDTH,BUTTON_HEIGHT,YELLOW,LIGHT_YELLOW,"Exit",BLACK)
					pygame.quit()
					sys.exit()
			elif event.type == QUIT:
				pygame.quit()
				sys.exit()

		pygame.display.update()


def playClickSound():
	ClickSound.play()
	time.sleep(0.15)
	ClickSound.stop()

def ShowInstructions():
	while True:
		DISPLAYSURF.fill(WHITE)

		img = pygame.image.load('instructions.png')
		DISPLAYSURF.blit(img,(XMARGIN,YMARGIN))

		x1 = XMARGIN
		y1 = YMARGIN + 400

		drawButton(x1,y1,BUTTON_WIDTH,BUTTON_HEIGHT,LIGHTGREEN,GREEN,"Go back")

		for event in pygame.event.get():
			if event.type == MOUSEBUTTONUP:
				x,y = event.pos
				if x1 < x < x1+BUTTON_WIDTH and y1 < y < y1+BUTTON_HEIGHT:
					drawButtonPush(x1,y1,BUTTON_WIDTH,BUTTON_HEIGHT,LIGHTGREEN,GREEN,"Go back",WHITE)
					return
		pygame.display.update()			


def copyBoard(board):
	newBoard = [['0' for x in range(BOARD_SIZE)]for y in range(BOARD_SIZE)]
	for x in range(BOARD_SIZE):
		for y in range(BOARD_SIZE):
			newBoard[x][y] = board[x][y]
	return newBoard		

def getTheBoard(ship):
	for x in range(BOARD_SIZE):
		for y in range(BOARD_SIZE):
			if occupied[x][y]==1 and already_occupied[x][y]!=1:
				mainboardPlayer1[y][x] = ship
				mainboardPlayer1Copy[y][x]=ship
				already_occupied[x][y]=1

def leftcordsofbox(boxx,boxy,number):
	if number==1:
		left = 	XMARGIN + boxx*(BOX_SIZE+GAP_SIZE)
		top = YMARGIN + boxy*(BOX_SIZE+GAP_SIZE)
	else:
		left = XMARGIN+BOARD_SIZE*(BOX_SIZE+GAP_SIZE) + BIG_GAP + boxx*(BOX_SIZE+GAP_SIZE)
		top = YMARGIN+boxy*(BOX_SIZE+GAP_SIZE)	
	box_rect = pygame.Rect(left,top,BOX_SIZE,BOX_SIZE)
	return box_rect

def drawboard():

	DISPLAYSURF.blit(BackgroundImage,(0,0))

	Turnx1 = XMARGIN
	Turny1 = YMARGIN - 30

	Turnx2 = XMARGIN + BOARD_SIZE*(BOX_SIZE+GAP_SIZE) + BIG_GAP
	Turny2 = YMARGIN - 30


	BORDERSIZE = BOARD_SIZE*(BOX_SIZE+GAP_SIZE) -GAP_SIZE +10

	pygame.draw.rect(DISPLAYSURF,ORANGE,(XMARGIN-5,YMARGIN-5,BORDERSIZE,BORDERSIZE),3)
	pygame.draw.rect(DISPLAYSURF,ORANGE,(XMARGIN+BOARD_SIZE*(BOX_SIZE+GAP_SIZE)+BIG_GAP-5,YMARGIN-5,BORDERSIZE,BORDERSIZE),3)
	

	for boxx in range(BOARD_SIZE):
		for boxy in range(BOARD_SIZE):
			box_rect = leftcordsofbox(boxx,boxy,1)
			if mainboardPlayer1[boxy][boxx] == '0':
				pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)
			elif mainboardPlayer1[boxy][boxx] == 'H':
				pygame.draw.rect(DISPLAYSURF,GREEN,box_rect)
			elif mainboardPlayer1[boxy][boxx] == 'M':
				pygame.draw.rect(DISPLAYSURF,RED,box_rect)
			elif mainboardPlayer1[boxy][boxx] == 'X':
				pygame.draw.rect(DISPLAYSURF,LIGHTGREEN,box_rect)
			elif mainboardPlayer1[boxy][boxx] in Ships:	
				pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)

	for boxx in range(BOARD_SIZE):
		for boxy in range(BOARD_SIZE):
			box_rect = leftcordsofbox(boxx,boxy,2)
			if mainboardPlayer2[boxy][boxx] == '0' or mainboardPlayer2[boxy][boxx] in Ships :
				pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)
			elif mainboardPlayer2[boxy][boxx] == 'H':
				pygame.draw.rect(DISPLAYSURF,GREEN,box_rect)
			elif mainboardPlayer2[boxy][boxx] == 'M':
				pygame.draw.rect(DISPLAYSURF,RED,box_rect)
			elif mainboardPlayer2[boxy][boxx] == 'X':
				pygame.draw.rect(DISPLAYSURF,LIGHTGREEN,box_rect)

	writeMove(1)
	writeMove(2)		

	index = 0
	for x in ShipState1:
		if x == 0:
			writePlayer(Ships[index],getMessage(Ships[index],2),2)
		index+=1
	index = 0
	for x in ShipState2:
		if x == 0:
			writePlayer(Ships[index],getMessage(Ships[index],1),1)
		index+=1

	drawButton(EXITX,EXITY,BUTTON_WIDTH,BUTTON_HEIGHT,YELLOW,LIGHT_YELLOW ,"Exit")

	if Turn == 1:
		fontObj = pygame.font.SysFont('Arial',16)
		textSurfaceObj = fontObj.render('Your Turn',True,WHITE)
		DISPLAYSURF.blit(textSurfaceObj,(Turnx2,Turny2))
	else:
		fontObj = pygame.font.SysFont('Arial',16)
		textSurfaceObj = fontObj.render('AI\'s Turn',True,WHITE)
		DISPLAYSURF.blit(textSurfaceObj,(Turnx1,Turny1))
		pygame.display.update()
		pygame.time.delay(500)
	

def drawButton(x,y,width,height,inactive_colour,active_colour,text):
	cur = pygame.mouse.get_pos()
	pygame.draw.rect(DISPLAYSURF,active_colour,(x,y,width,height))
	pygame.draw.rect(DISPLAYSURF,inactive_colour,(x,y+height,width,int(height/4)))
	text_to_button(x,y,width,height,text)

def drawButtonPush(x,y,width,height,inactive_colour,active_colour,text,back_colour):
	pygame.draw.rect(DISPLAYSURF,back_colour,(x,y,width,int(height/4)))
	pygame.draw.rect(DISPLAYSURF,active_colour,(x,y+int(height/4),width,height))
	text_to_button(x,y,width,height,text)
	pygame.display.update()
	playClickSound()
	time.sleep(0.1)
	drawButton(x,y,width,height,inactive_colour,active_colour,text)
	pygame.display.update()
	time.sleep(0.1)

def text_to_button(x,y,width,height,text):
	fontObj = pygame.font.SysFont('Comic Sans MS',16)
	textSurfaceObj = fontObj.render(text,True,BLACK)
	DISPLAYSURF.blit(textSurfaceObj,(x+7,y+7))

def drawHighlightBox(boxx,boxy,number):
	if number == 2:
		box_rect = leftcordsofbox(boxx,boxy,number)
		left = box_rect.left
		top = box_rect.top
		pygame.draw.rect(DISPLAYSURF,BLUE,(left-4,top-4,BOX_SIZE+8,BOX_SIZE+8),3)

def getBoxAtPixel(x,y):
	number = 1
	if x>=XMARGIN+BOARD_SIZE*(BOX_SIZE+GAP_SIZE)+BIG_GAP:
		number=2
	for boxx in range(BOARD_SIZE):
		for boxy in range(BOARD_SIZE):
			box_rect = leftcordsofbox(boxx,boxy,number)
			if box_rect.collidepoint(x,y):
				return (boxx,boxy,number)
	return (None,None,number)	

def DestroyBox(boxx,boxy,number):
	box_rect = leftcordsofbox(boxx,boxy,number)
	pygame.draw.rect(DISPLAYSURF,LIGHTGREEN,box_rect)

def AllDestroyed(number):
	updateStats(number)
	displayRemaining()
	if number == 1:
		text = "You have lost."
	else:
		text = "You Won!"
	txt.close()	
	while True:
		x = XMARGIN
		y = WINDOW_SIZEY - YMARGIN + 20
		pygame.draw.rect(DISPLAYSURF,YELLOW,(x,y,WINDOW_SIZEX-2*XMARGIN,100))
		fontObj = pygame.font.Font('freesansbold.ttf',16)
		textSurfaceObj = fontObj.render(text,True,WHITE)
		DISPLAYSURF.blit(textSurfaceObj,(x+10,y+10))
		x1 = x +10
		y1 = y + 50 
		x2 = x1 + BUTTON_WIDTH + 20
		y2 = y1
		drawButton(x1,y1,BUTTON_WIDTH,BUTTON_HEIGHT,LIGHTRED,RED,"Play Again")
		drawButton(x2,y2,BUTTON_WIDTH,BUTTON_HEIGHT,LIGHTRED,RED,"Exit")

		for event in pygame.event.get():
			if event.type == MOUSEBUTTONUP:
				x,y = event.pos
				if x1 < x < x1 + BUTTON_WIDTH and y1 < y < y1 + BUTTON_HEIGHT:
					drawButtonPush(x1,y1,BUTTON_WIDTH,BUTTON_HEIGHT,LIGHTRED,RED,"Play Again",YELLOW)
					initializeEverything()
					main()
				elif x2 < x < x2+BUTTON_WIDTH and y2 < y < y2+BUTTON_HEIGHT:
					drawButtonPush(x2,y2,BUTTON_WIDTH,BUTTON_HEIGHT,LIGHTRED,RED,"Exit",YELLOW)
					pygame.quit()
					sys.exit()
		pygame.display.update()
		time.sleep(1)			


def displayRemaining():

	DISPLAYSURF.blit(BackgroundImage,(0,0))

	Turnx1 = XMARGIN
	Turny1 = YMARGIN - 30

	Turnx2 = XMARGIN + BOARD_SIZE*(BOX_SIZE+GAP_SIZE) + BIG_GAP
	Turny2 = YMARGIN - 30


	BORDERSIZE = BOARD_SIZE*(BOX_SIZE+GAP_SIZE) -GAP_SIZE +10

	pygame.draw.rect(DISPLAYSURF,ORANGE,(XMARGIN-5,YMARGIN-5,BORDERSIZE,BORDERSIZE),3)
	pygame.draw.rect(DISPLAYSURF,ORANGE,(XMARGIN+BOARD_SIZE*(BOX_SIZE+GAP_SIZE)+BIG_GAP-5,YMARGIN-5,BORDERSIZE,BORDERSIZE),3)
	

	for boxx in range(BOARD_SIZE):
		for boxy in range(BOARD_SIZE):
			box_rect = leftcordsofbox(boxx,boxy,1)
			if mainboardPlayer1[boxy][boxx] == '0':
				pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)
			elif mainboardPlayer1[boxy][boxx] == 'H':
				pygame.draw.rect(DISPLAYSURF,GREEN,box_rect)
			elif mainboardPlayer1[boxy][boxx] == 'M':
				pygame.draw.rect(DISPLAYSURF,RED,box_rect)
			elif mainboardPlayer1[boxy][boxx] == 'X':
				pygame.draw.rect(DISPLAYSURF,LIGHTGREEN,box_rect)
			elif mainboardPlayer1[boxy][boxx] in Ships:	
				pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)

	for boxx in range(BOARD_SIZE):
		for boxy in range(BOARD_SIZE):
			box_rect = leftcordsofbox(boxx,boxy,2)
			if mainboardPlayer2[boxy][boxx] == '0':
				pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)
			elif mainboardPlayer2[boxy][boxx] == 'H':
				pygame.draw.rect(DISPLAYSURF,GREEN,box_rect)
			elif mainboardPlayer2[boxy][boxx] == 'M':
				pygame.draw.rect(DISPLAYSURF,RED,box_rect)
			elif mainboardPlayer2[boxy][boxx] == 'X':
				pygame.draw.rect(DISPLAYSURF,LIGHTGREEN,box_rect)
			elif mainboardPlayer2[boxy][boxx] in Ships:
				pygame.draw.rect(DISPLAYSURF,LIGHT_YELLOW,box_rect)	

	pygame.display.update()			

def updateStats(number):
	stats = open('Stats.txt')
	CurrStats = stats.read()
	mode1Win = 0
	index1 = 0
	while CurrStats[index1]!=' ':
		index1+=1
	mode1Win = int(CurrStats[:index1])
	index2 = index1
	while CurrStats[index2]!='\n':
		index2+=1
	mode1Lose = int(CurrStats[index1+1:index2])
	stats.close()
	if number == 1:
		mode1Lose+=1
	else:
		mode1Win+=1	
	NewStats = str(mode1Win)+" "+str(mode1Lose)+"\n"
	newstats = open('Stats.txt','w')
	newstats.write(NewStats)
	newstats.close()



def getMessage(ship,number):
	s = ""
	name = ""
	if number == 1:
		name = "You "
	else:
		name = "AI "	
	if ship == 'C':
		s =  name + "sunk the Carrier."
	elif ship == 'B':
		s = name + "sunk the Battleship."
	elif ship == 'R':
		s = name + "sunk the Cruiser."
	elif ship == 'S':
		s = name + "sunk the Submarine."
	elif ship == 'D':
		s = name + "sunk the Destroyer."
	return s			

def DestroyMessage(ship,number):
	message = getMessage(ship)
	if number==1:
		messagePlayer2 = message
	else:
		messagePlayer1 = message

def writePlayer(ship,message,number):
	if number == 1:
		x = XMARGIN + BOARD_SIZE*(BOX_SIZE+GAP_SIZE)+BIG_GAP
		y = YMARGIN + BOARD_SIZE*(BOX_SIZE+GAP_SIZE) + 30
	else:	
		x = XMARGIN
		y = YMARGIN + BOARD_SIZE*(BOX_SIZE+GAP_SIZE) + 30
	fontObj = pygame.font.Font('freesansbold.ttf',16)
	textSurfaceObj = fontObj.render(message,True,WHITE)
	if ship == 'C':
		DISPLAYSURF.blit(textSurfaceObj,(x,y+20))
	elif ship == 'B':
		DISPLAYSURF.blit(textSurfaceObj,(x,y+40))
	elif ship == 'R':
		DISPLAYSURF.blit(textSurfaceObj,(x,y+60))
	elif ship == 'S':
		DISPLAYSURF.blit(textSurfaceObj,(x,y+80))
	elif ship == 'D':
		DISPLAYSURF.blit(textSurfaceObj,(x,y+100))				

def getMoveMessage(move):
	message = ""
	if move == 1:
		message = "Hit"
	elif move == 0:			
		message = "Miss"
	return message		

def writeMove(number):
	message = ""
	if number == 1:
		x = XMARGIN
		y = YMARGIN + BOARD_SIZE*(BOX_SIZE+GAP_SIZE) + 10
		message = getMoveMessage(movePlayer1)		
		fontObj = pygame.font.Font('freesansbold.ttf',16)
		textSurfaceObj = fontObj.render(message,True,WHITE)
		DISPLAYSURF.blit(textSurfaceObj,(x,y))	

	else:
		x = XMARGIN + BOARD_SIZE*(BOX_SIZE+GAP_SIZE)+BIG_GAP
		y = YMARGIN + BOARD_SIZE*(BOX_SIZE+GAP_SIZE) + 10
		message = getMoveMessage(movePlayer2)		
		fontObj = pygame.font.Font('freesansbold.ttf',16)
		textSurfaceObj = fontObj.render(message,True,WHITE)
		DISPLAYSURF.blit(textSurfaceObj,(x,y))
		

def Destroyed(number,ship):
	if number==1:
		for boxx in range(BOARD_SIZE):
			for boxy in range(BOARD_SIZE):
				if mainboardPlayer1Copy[boxy][boxx] == ship:
					DestroyBox(boxx,boxy,number)
					mainboardPlayer1[boxy][boxx] = 'X'
	else:
		for boxx in range(BOARD_SIZE):
			for boxy in range(BOARD_SIZE):
				if mainboardPlayer2Copy[boxy][boxx] == ship:
					DestroyBox(boxx,boxy,number)
					mainboardPlayer2[boxy][boxx] = 'X'
							

def checkIfDestroyed(number):
	if number == 1:
		flag = 0
		index = 0
		for ship in Ships:
			if ShipState1[index] == 1:
				count = 0
				for boxx in range(BOARD_SIZE):
					for boxy in range(BOARD_SIZE):
						if mainboardPlayer1[boxy][boxx] == ship:
							count = count +1			
				if count == 0:
					ShipState1[index] =0
					Destroyed(number,ship)
				else:
					flag = 1
			index+= 1		
		if flag == 0:
			AllDestroyed(number)
	else:
		flag = 0
		index = 0
		for ship in Ships:
			if ShipState2[index] == 1:
				count = 0
				for boxx in range(BOARD_SIZE):
					for boxy in range(BOARD_SIZE):
						if mainboardPlayer2[boxy][boxx] == ship:
							count = count +1
				if count == 0:
					ShipState2[index] = 0
					Destroyed(number,ship)
				else:
					flag = 1
			index+=1		
		if flag == 0:
			AllDestroyed(number)								

def updateBoard(number,boxx,boxy,hit):
	global movePlayer1,movePlayer2 

	if number ==1:
		if hit:
			mainboardPlayer1[boxy][boxx] = 'H'
			movePlayer1 = 1						
		else:
			mainboardPlayer1[boxy][boxx] = 'M'
			movePlayer1 = 0						

	else:
		if hit:
			mainboardPlayer2[boxy][boxx] = 'H'
			movePlayer2 = 1						
		else:
			mainboardPlayer2[boxy][boxx] = 'M'
			movePlayer2 = 0						

def onClick(boxx,boxy,board,number):
	if board[boxy][boxx]!='H' and board[boxy][boxx]!='M' and board[boxy][boxx]!='X':
		box_rect = leftcordsofbox(boxx,boxy,number)
		if isShip(board[boxy][boxx]):
			pygame.draw.rect(DISPLAYSURF,GREEN,box_rect)
			updateBoard(number,boxx,boxy,True)
			checkIfDestroyed(number)		

		else:
			updateBoard(number,boxx,boxy,False)
			pygame.draw.rect(DISPLAYSURF,RED,box_rect)
		return True
	return False		

def initializeEverything():
	for x in range(BOARD_SIZE):
		for y in range(BOARD_SIZE):
			occupied[x][y]=0
			already_occupied[x][y]=0
			mainboardPlayer1[x][y]='0'
			mainboardPlayer2[x][y]='0'
	for x in range(0,5):
		ShipState1[x]=1
		ShipState2[x]=1



def getRandomizedBoard():
	txt = open('ships.txt')
	board = [['0' for i in range(10)]for j in range(10)]
	for x in range(BOARD_SIZE):
		for y in range(BOARD_SIZE):
			board[x][y] = txt.read(1)
			char = txt.read(1)

	txt.close()		
	return board

def isShip(ship):
	ships = ['C','B','R','S','D']
	if ship in ships:
		return True
	return False	

# functions for placing the ships

def is_free(boxx,boxy):
	if occupied[boxx][boxy]==1:
		return 0
	else:
		return 1	



def placing_ships_vertical(ship,size):
	flag=1
	if ship!=None:
		if ship[0][1]+size-1<=9:
			for i in range(size):
				if occupied[ship[0][0]][ship[0][1]+i]==1:
					flag=0
						
			if flag==1:
				ship1=[]		
				for i in range(size):
					box_rect=leftcordsofbox(ship[i][0],ship[i][1],1)
					pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)
					box_rect=leftcordsofbox(ship[0][0],ship[0][1]+i,1)
					pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)
					occupied[ship[i][0]][ship[i][1]]=0
					occupied[ship[0][0]][ship[0][1]+i]=1
					ship1.append((ship[0][0],ship[0][1]+i))
				ship=ship1
		else:
			flag=0

	if ship==None or flag==0:
			ship=[]
			count=0
			flag1=0
			for boxx in range(BOARD_SIZE):
				for boxy in range(BOARD_SIZE):
					box_rect = leftcordsofbox(boxx,boxy,1)
					if is_free(boxx,boxy)==1 and boxy+size<=10:
						flag2=1
						for j in range(size):
							if occupied[boxx][boxy+j]==1:
								flag2=0
						if flag2==1:		
							for j in range(boxy,boxy+size,1):
								box_rect = leftcordsofbox(boxx,j,1)
								occupied[boxx][j]=1
								ship.append((boxx,j))
								pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)
							pygame.display.update()
							flag1=1	
							break	
				if flag1==1:
					break			
					break			
	while True:
		for event in pygame.event.get():
				if event.type==QUIT:
					pygame.quit()
					sys.exit()
				elif event.type==KEYUP:
						if event.key==K_LEFT:
							ship=move_left_vertical(ship,size)
						elif event.key==K_RIGHT:
							ship=move_right_vertical(ship,size)
						elif event.key==K_DOWN:
							ship=move_down_vertical(ship,size)
						elif event.key==K_UP:
							ship=move_up_vertical(ship,size)
						elif event.key==K_t:
							for i in range(size):
								box_rect = leftcordsofbox(ship[i][0],ship[i][1],1)
								pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)
								occupied[ship[i][0]][ship[i][1]]=0

							pygame.display.update()	
							q=placing_ships_horizontal(ship,size)
							if q==1:
								return 1
						elif event.key==K_RETURN:
							playClickSound()
							return 1	
		pygame.display.update()						


def placing_ships_horizontal(ship,size):
	flag=1
	if ship!=None:
		if ship[0][0]+size-1<=9:
			for i in range(size):
				if occupied[ship[0][0]+i][ship[0][1]]==1:
					flag=0
			if flag==1:	
				ship1=[]	
				for i in range(size):
					box_rect=leftcordsofbox(ship[i][0],ship[i][1],1)
					pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)
					box_rect=leftcordsofbox(ship[0][0]+i,ship[0][1],1)
					pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)
					occupied[ship[i][0]][ship[i][1]]=0
					occupied[ship[0][0]+i][ship[0][1]]=1
					ship1.append((ship[0][0]+i,ship[0][1]))
				ship=ship1
		else:
			flag=0

	if ship==None or flag==0:
		ship=[]
		count=0
		flag1=0
		for boxy in range(BOARD_SIZE):
			for boxx in range(BOARD_SIZE):
				box_rect = leftcordsofbox(boxx,boxy,1)
				if is_free(boxx,boxy)==1 and boxx+size<=10:
					flag2=1
					for j in range(size):
						if occupied[boxx+j][boxy]==1:
							flag2=0
					if flag2==1:		
						for j in range(boxx,boxx+size,1):
							box_rect = leftcordsofbox(j,boxy,1)
							occupied[j][boxy]=1
							ship.append((j,boxy))
							pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)
						pygame.display.update()
						flag1=1	
						break
			if flag1==1:
				break			

	while True:
		for event in pygame.event.get():
				if event.type==QUIT:
					pygame.quit()
					sys.exit()
				elif event.type==KEYUP:
						if event.key==K_LEFT:
							ship=move_left_horizontal(ship,size)
						elif event.key==K_RIGHT:
							ship=move_right_horizontal(ship,size)
						elif event.key==K_DOWN:
							ship=move_down_horizontal(ship,size)
						elif event.key==K_UP:
							ship=move_up_horizontal(ship,size)
						elif event.key==K_t:
							for i in range(size):
								box_rect = leftcordsofbox(ship[i][0],ship[i][1],1)
								pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)
								occupied[ship[i][0]][ship[i][1]]=0
							pygame.display.update()
							q=placing_ships_vertical(ship,size)
							if q==1:
								return 1
						elif event.key==K_RETURN:
							playClickSound()
							return 1							
		pygame.display.update()											

def move_left_vertical(ship,size):
	flag=1
	flag1=0
	j=0
	i=0
	ship1=[]
	for i in range(size):
		if ship[i][0]<=0:
			flag=0
			return ship
	for i in range(size):		
		if occupied[ship[i][0]-1][ship[i][1]]==1:
			flag=0
			for i in range(ship[0][0]-2,-1,-1):
				flag1=1
				for j in range(0,size):
					if occupied[i][ship[0][1]+j]==1:
						flag1=0
						break
				if flag1==1:
					for j in range(size):
						box_rect=leftcordsofbox(i,ship[j][1],1)
						pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)
						occupied[i][ship[j][1]]=1
						ship1.append((i,ship[j][1]))
					for j in range(size):
						box_rect=leftcordsofbox(ship[j][0],ship[j][1],1)
						pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)
						occupied[ship[j][0]][ship[j][1]]=0
					return ship1
			if flag1==0:
				return ship

	if flag==1:
		for i in range(size):
			box_rect = leftcordsofbox(ship[i][0]-1,ship[i][1],1)
			pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)
			occupied[ship[i][0]-1][ship[i][1]]=1
		for i in range(size):
			box_rect =leftcordsofbox(ship[i][0],ship[i][1],1)
			pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)	
			occupied[ship[i][0]][ship[i][1]]=0
			ship1.append((ship[i][0]-1,ship[i][1]))
	return ship1		

def move_right_vertical(ship,size):
	flag=1
	flag1=0
	ship1=[]
	for i in range(size):
		if ship[i][0]>=9:
			flag=0
			return ship
	for i in range(size):		
		if occupied[ship[i][0]+1][ship[i][1]]==1:
			flag=0
			for i in range(ship[0][0]+2,10,1):
				flag1=1
				for j in range(0,size):
					if occupied[i][ship[0][1]+j]==1:
						flag1=0
						break
				if flag1==1:
					for j in range(size):
						box_rect=leftcordsofbox(i,ship[j][1],1)
						pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)
						occupied[i][ship[j][1]]=1
						ship1.append((i,ship[j][1]))
					for j in range(size):
						box_rect=leftcordsofbox(ship[j][0],ship[j][1],1)
						pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)
						occupied[ship[j][0]][ship[j][1]]=0
					return ship1
			if flag1==0:
				return ship
			
	if flag==1:
		for i in range(size):
			box_rect = leftcordsofbox(ship[i][0]+1,ship[i][1],1)
			pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)
			occupied[ship[i][0]+1][ship[i][1]]=1
		for i in range(size):
			box_rect =leftcordsofbox(ship[i][0],ship[i][1],1)
			pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)	
			occupied[ship[i][0]][ship[i][1]]=0
			ship1.append((ship[i][0]+1,ship[i][1]))

	return ship1
def move_up_horizontal(ship,size):
	flag=1
	flag1=0
	ship1=[]
	for i in range(size):
		if ship[i][1]<=0:
			flag=0
			return ship
	for i in range(size):		
		if occupied[ship[i][0]][ship[i][1]-1]==1:
			flag=0
			#return ship
			for i in range(ship[0][1]-2,-1,-1):
				flag1=1
				for j in range(0,size):
					if occupied[ship[0][0]+j][i]==1:
						flag1=0
						break
				if flag1==1:
					for j in range(size):
						box_rect=leftcordsofbox(ship[j][0],i,1)
						pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)
						occupied[ship[j][0]][i]=1
						ship1.append((ship[j][0],i))
					for j in range(size):
						box_rect=leftcordsofbox(ship[j][0],ship[j][1],1)
						pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)
						occupied[ship[j][0]][ship[j][1]]=0
					return ship1
			if flag1==0:
				return ship		
	if flag==1:
		for i in range(size):
			box_rect = leftcordsofbox(ship[i][0],ship[i][1]-1,1)
			pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)
			occupied[ship[i][0]][ship[i][1]-1]=1

		for i in range(size):
			box_rect =leftcordsofbox(ship[i][0],ship[i][1],1)
			pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)	
			occupied[ship[i][0]][ship[i][1]]=0
			ship1.append((ship[i][0],ship[i][1]-1))
			
	return ship1		

def move_down_horizontal(ship,size):
	flag1=0
	flag=1
	ship1=[]
	for i in range(size):
		if ship[i][1]>=9: 
			flag=0
			return ship

	for i in range(size):		
		if occupied[ship[i][0]][ship[i][1]+1]==1:
			flag=0
			for i in range(ship[0][1]+2,10,+1):
				flag1=1
				for j in range(0,size):
					if occupied[ship[0][0]+j][i]==1:
						flag1=0
						break
				if flag1==1:
					for j in range(size):
						box_rect=leftcordsofbox(ship[j][0],i,1)
						pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)
						occupied[ship[j][0]][i]=1
						ship1.append((ship[j][0],i))
					for j in range(size):
						box_rect=leftcordsofbox(ship[j][0],ship[j][1],1)
						pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)
						occupied[ship[j][0]][ship[j][1]]=0
					return ship1
			if flag1==0:
				return ship

	if flag==1:
		for i in range(size):
			box_rect = leftcordsofbox(ship[i][0],ship[i][1]+1,1)
			pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)
			occupied[ship[i][0]][ship[i][1]+1]=1
		for i in range(size):
			box_rect =leftcordsofbox(ship[i][0],ship[i][1],1)
			pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)	
			occupied[ship[i][0]][ship[i][1]]=0
			ship1.append((ship[i][0],ship[i][1]+1))

	return ship1			

def move_up_vertical(ship,size):
	flag=1
	ship1=[]
	for i in range(size):
		if ship[i][1]<=0:
			flag=0
			return ship
	if occupied[ship[0][0]][ship[0][1]-1]==1:
			
		for i in range(ship[0][1]-2,0,-1):
			if(occupied[ship[0][0]][i]==0 and i>=size-1):
				flag1=1
				for j in range(size):
					if occupied[ship[0][0]][i-j]==1:
						flag1=0
				if flag1==1:	
					for j in range(size):
						box_rect=leftcordsofbox(ship[0][0],i-j,1)
						pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)
						occupied[ship[0][0]][i-j]=1
						ship1.append((ship[0][0],i-j))
					for j in range(size):
						box_rect=leftcordsofbox(ship[j][0],ship[j][1],1)
						pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)
						occupied[ship[j][0]][ship[j][1]]=0
					ship1.reverse()
					return ship1

		return ship

	if flag==1:
		box_rect=leftcordsofbox(ship[0][0],ship[0][1]-1,1)
		
		pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)
		box_rect=leftcordsofbox(ship[size-1][0],ship[size-1][1],1)
		pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)
		occupied[ship[0][0]][ship[0][1]-1]=1
		occupied[ship[size-1][0]][ship[size-1][1]]=0
		for i in range(size):
			ship1.append((ship[i][0],ship[i][1]-1))

	return ship1

def move_down_vertical(ship,size):
	flag=1
	ship1=[]

	for i in range(size):
		if ship[i][1]>=9:
			flag=0
			return ship
	if occupied[ship[size-1][0]][ship[size-1][1]+1]==1:
		
		for i in range(ship[size-1][1]+2,9,1):
			if(occupied[ship[size-1][0]][i]==0 and 9-i>=size-1):
				flag1=1
				for j in range(size):
					if occupied[ship[size-1][0]][i+j]==1:
						flag1=0
				if flag1==1:	
					for j in range(size):
						box_rect=leftcordsofbox(ship[size-1][0],i+j,1)
						pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)
						occupied[ship[size-1][0]][i+j]=1
						ship1.append((ship[size-1][0],i+j))
					for j in range(size):
						box_rect=leftcordsofbox(ship[j][0],ship[j][1],1)
						pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)
						occupied[ship[j][0]][ship[j][1]]=0
					return ship1

		return ship


	if flag==1:
		box_rect = leftcordsofbox(ship[size-1][0],ship[size-1][1]+1,1)
		pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)
		box_rect=leftcordsofbox(ship[0][0],ship[0][1],1)
		pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)
		occupied[ship[size-1][0]][ship[size-1][1]+1]=1
		occupied[ship[0][0]][ship[0][1]]=0
		for i in range(size):
			ship1.append((ship[i][0],ship[i][1]+1))
			

	return ship1		

def move_left_horizontal(ship,size):
	flag=1
	ship1=[]
	for i in range(size):
		if ship[i][0]<=0:
			flag=0
			return ship
	if occupied[ship[0][0]-1][ship[0][1]]==1:
		
		for i in range(ship[0][0]-2,0,-1):
			if(occupied[i][ship[0][1]]==0 and i>=size-1):
				flag1=1
				for j in range(size):
					if occupied[i-j][ship[0][1]]==1:
						flag1=0
				if flag1==1:	
					for j in range(size):
						box_rect=leftcordsofbox(i-j,ship[0][1],1)
						pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)
						occupied[i-j][ship[0][1]]=1
						ship1.append((i-j,ship[0][1]))
					for j in range(size):
						box_rect=leftcordsofbox(ship[j][0],ship[j][1],1)
						pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)
						occupied[ship[j][0]][ship[j][1]]=0
					ship1.reverse()	
					return ship1

		return ship

	if flag==1:
		box_rect = leftcordsofbox(ship[0][0]-1,ship[0][1],1)
		pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)
		box_rect=leftcordsofbox(ship[size-1][0],ship[size-1][1],1)
		pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)
		occupied[ship[0][0]-1][ship[0][1]]=1
		occupied[ship[size-1][0]][ship[size-1][1]]=0
		for i in range(size):
			ship1.append((ship[i][0]-1,ship[i][1]))

	return ship1

def move_right_horizontal(ship,size):
	flag=1
	ship1=[]
	for i in range(size):
		if ship[i][0]>=9:
			flag=0
			return ship
	if occupied[ship[size-1][0]+1][ship[size-1][1]]==1:

		for i in range(ship[size-1][0]+2,9,1):
			if(occupied[i][ship[size-1][1]]==0 and 9-i>=size-1):
				flag1=1
				for j in range(size):
					if occupied[i+j][ship[size-1][1]]==1:
						flag1=0
				if flag1==1:	
					for j in range(size):
						box_rect=leftcordsofbox(i+j,ship[size-1][1],1)
						pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)
						occupied[i+j][ship[size-1][1]]=1
						ship1.append((i+j,ship[size-1][1]))
					for j in range(size):
						box_rect=leftcordsofbox(ship[j][0],ship[j][1],1)
						pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)
						occupied[ship[j][0]][ship[j][1]]=0
					return ship1
		return ship			

	if flag==1:
		box_rect = leftcordsofbox(ship[size-1][0]+1,ship[size-1][1],1)
		pygame.draw.rect(DISPLAYSURF,PLACE,box_rect)
		box_rect=leftcordsofbox(ship[0][0],ship[0][1],1)
		pygame.draw.rect(DISPLAYSURF,NAVYBLUE,box_rect)
		occupied[ship[size-1][0]+1][ship[size-1][1]]=1
		occupied[ship[0][0]][ship[0][1]]=0
		for i in range(size):
			ship1.append((ship[i][0]+1,ship[i][1]))

	return ship1

if __name__ == '__main__':
    main()



