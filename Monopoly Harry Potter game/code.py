class startscreen:
	def __init__(self,width,height,title,image):
		self.width=width
		self.height=height
		self.title=title
		self.image=image

	def createWindow(self):
		global wn
		wn=pygame.display.set_mode((self.width,self.height))
		wn.fill((255,255,255))
		pygame.display.set_caption(self.title)
		if self.image !=None:
			bgimage=pygame.image.load(self.image).convert()
			bgimage=pygame.transform.scale(bgimage,(self.width,self.height))
			wn.blit(bgimage,(0,0))


class Buttons:
	def __init__(self,text,color,x,y,width,height,window,action,mainscreen):
		self.text=text
		self.color=color
		self.x=x
		self.y=y
		self.width=width
		self.height=height
		self.window=window
		self.font = pygame.font.SysFont('Arial', 25)
		self.btncenter=((self.x+(self.width//2)),(self.y+(self.height//2)))
		self.action=action
	def drawButton(self):
		pygame.draw.rect(self.window,self.color,(self.x,self.y,self.width,self.height))
	def addText(self):
		text=self.font.render(self.text, True, (255,0,0))
		text_rect=text.get_rect()
		self.window.blit(self.font.render(self.text, True, (0,0,255)), (self.btncenter[0]-(text_rect[2]//2),self.btncenter[1]-(text_rect[3]//2)))
	def pressstart(self):
		gp=gameplay(1366,700,'./Pictures/gameboard.jpg','Monopoly: Harry Potter Edition')
		gp.createGameplay()

	def buttonClick(self):
		pos=pygame.mouse.get_pos()
		click=pygame.mouse.get_pressed()
		if self.x<pos[0]<self.x+self.width and self.y<pos[1]<self.y+self.height:
			if click[0]==1 and self.action!=None:
				if self.action=='Start':
					self.pressstart()
				if self.action=='Instructions':
					self.pressinstr()

class gameplay:
	def __init__(self,width,height,gameboard,title):
		self.width=width
		self.height=height
		self.gameboard=gameboard
		self.title=title

	def createGameplay(self):
		wn=pygame.display.set_mode((self.width,self.height))
		wn.fill((255,255,255))
		pygame.display.set_caption(self.title)
		if self.gameboard !=None:
			bgimage=pygame.image.load(self.gameboard).convert()
			bgimage=pygame.transform.scale(bgimage,(self.width-500,self.height))
			wn.blit(bgimage,(0,0))
		for i in range(4):
			pygame.draw.rect(wn,(255,255,255),(self.width-500,0,50,50))


					
import pygame
pygame.init()
mainscreen=startscreen(1366,700,'Monopoly: Harry Potter Edition','./Pictures/mainscreenimage.png')
mainscreen.createWindow()
startbtn=Buttons('Start',[0,255,0],100,100,100,100,wn,'Start',mainscreen)
startbtn.drawButton()
startbtn.addText()
instr=Buttons('Instructions',[255,0,0],300,100,100,100,wn,'Instructions',mainscreen)
instr.drawButton()
instr.addText()
a=True
while a:
	startbtn.buttonClick()
	instr.buttonClick()
	pygame.display.update()
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			a=False
pygame.quit()
quit()