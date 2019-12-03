#All the pictures and sprites are taken from the website www.nowthatsthrifty.com
########## USE THIS SPACE TO WRITE YOUR HELPER FUNCTIONS ##########
def leftrotate(x,c):
    return ((x << c)&0xFFFFFFFF) | (x >> (32-c)&0x7FFFFFFF>>(32-c))

########## FILL IN THE FUNCTIONS TO IMPLEMENT THE CLIENT ##########
def StartConnection (IPAddress, PortNumber):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)    #creates the variable s
    s.connect((IPAddress,PortNumber))  #connects the variable s to the server
    return s

def login (s,username, password):
    S=[7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
    K=[0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501, 0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821, 0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8, 0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a, 0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70, 0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665, 0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1, 0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391]
    s.send(b'LOGIN '+ username.encode()+b'\n')
    msg=s.recv(512) 
    msg=str(msg,'utf-8')
    challenge=msg.split()[2]
    n=len(password)
    m=len(challenge)
    message=password+challenge 
    zeroes=512-(len(message)+len(str(n+m))+1)    #this calculates the number of zeroes that need to be present in the block
    block=message+str(1*(10**(zeroes)))+str(n+m)  #this creates the block with required number of zeroes
    M=[]
    for i in range(16):      #this loop goes through 32 element chunks of the block 16 times
        segment=block[(i*32):((i+1)*32)]
        asciSum=0
        for j in segment: #this loop calculates the sum of ascii values of the characters in each chunk and adds them to list M
            asciSum=asciSum+ord(j)
        M.append(asciSum)
    a0=0x67452301
    b0=0xefcdab89
    c0=0x98badcfe
    d0=0x10325476
    A=a0
    B=b0
    C=c0
    D=d0
    for i in range(0,64):
        if 0<=i<=15:
            F=(B & C) | ((~ B) & D)
            F=F&0xFFFFFFFF
            g=i
        elif 16<=i<=31:
            F=(D&B) | ((~ D) & C)
            F=F&0xFFFFFFFF
            g=((5*i)+1)%16
        elif 32<=i<=47:
            F=B^C^D
            F=F&0xFFFFFFFF
            g=((3*i)+5)%16
        elif 48<=i<=63:
            F=C^(B | (~ D))
            F=F&0xFFFFFFFF
            g=(7*i)%16
        dTemp=D
        D=C
        C=B
        B=B+leftrotate((A+F+K[i]+M[g]),S[i])
        B=B&0xFFFFFFFF
        A=dTemp
    a0=(a0+A)&0xFFFFFFFF
    b0=(b0+B)&0xFFFFFFFF
    c0=(c0+C)&0xFFFFFFFF
    d0=(d0+D)&0xFFFFFFFF
    result=str(a0)+str(b0)+str(c0)+str(d0)
    s.send(b'LOGIN '+username.encode()+b' '+result.encode()+b'\n')
    returnmsg=s.recv(1024)
    returnmsg=str(returnmsg,'utf-8')
    if returnmsg.split()[-1]=='Successful':
        return True
    else:
        return False

def getUsers(s):
    s.send(b'@users\n')
    msg=s.recv(6)   #this receives the first 6 bytes that includes the size only
    byte=int(msg[1:])#this is the size of the entire string
    newmsg=s.recv(byte)   #this recieves the full message
    newmsg=str(newmsg,'utf-8')
    list1=newmsg.split('@')[3:] #the message received is split on the basis of @ character and is returned from the third character onwards
    return list1

def getFriends(s):
    s.send(b'@friends\n')
    msg=s.recv(6)   #this recieves the first six bytes of the message
    byte=int(msg[1:])    #this is the size of the string converted into an integer
    newmsg=s.recv(byte)   #this recieves the new message with the required number of bytes
    newmsg=str(newmsg,'utf-8')
    list1=newmsg.split('@')[3:]   #the message is split on the basis of @ character
    return list1

def sendFriendRequest(s,username):
    size=str(len(('@request@friend@')+username)+6)   #this calculates the size of the string excluding the size 
    if len(size)<=5:
        zeroes=5-len(size)
        for i in range(zeroes):   #this adds appropriate number of zeroes to size to make it equal to 5
            size='0'+size
        msg='@'+size+'@request@friend@'+username
        s.send(msg.encode())
        reply=s.recv(512)
        reply=str(reply,'utf-8')
        reply=reply.split('@')
        if 'ok' in reply:
            return True
        else:
            return False
        

def acceptFriendRequest(s,friend):
    size=str(len(('@accept@friend@')+friend)+6)   #this calculates length of the string excluding the size 
    if len(size)<=5:
        zeroes=5-len(size)
        for i in range(zeroes):   #this adds appropriate number of zeroes to size to make it equal to size 5
            size='0'+size
        msg='@'+size+'@accept@friend@'+friend
        s.send(msg.encode())
        reply=s.recv(512)
        reply=str(reply,'utf-8')
        if 'not found' in reply:
            return False
        elif 'ok' in reply:
            return True

        
def sendMessage(s,friend,message):
    size=str(len(('@sendmsg@')+friend+'@'+message)+6)  #this calculates the length of the message sent to server excluding the @size slice
    if len(size)<=5:
        zeroes=5-len(size)
        for i in range(zeroes):   #this adds appropriate number of zeroes to size to make it equal to five characters long
            size='0'+size
        msg='@'+size+'@sendmsg@'+friend+'@'+message
        s.send(msg.encode())
        reply=s.recv(512)
        reply=str(reply,'utf-8')
        if 'ok' in reply:   #if the operation is carried out successfully 'ok' is present in the reply and True is returned
            return True
        else:
            return False
        
    

def sendFile(s,friend,filename):
    with open(filename,'r') as file:
        file1=file.read()
        size=str(len(('@sendfile@')+friend+'@'+filename+'@'+file1)+6)
        if len(size)<=5:
            zeroes=5-len(size)
            for i in range(zeroes):
                size='0'+size
            msg='@'+size+'@sendfile@'+friend+'@'+filename+'@'+file1
            s.send(msg.encode())
            reply=s.recv(512)
            reply=str(reply,'utf-8')
            if '@ok' in reply:
                return True
            else:
                return False

def getRequests(s):
    s.send(b'@rxrqst\n')
    msg=s.recv(6)
    byte=int(msg[1:])
    newmsg=s.recv(byte)
    newmsg=str(newmsg,'utf-8')
    list1=newmsg.split('@')[3:] 
    return list1

def getMail(s):
    list1=[]  #this list is for usernames and messages
    list2=[]   #this list is for usernames and files
    s.send(b'@rxmsg\n')
    msg=s.recv(6)
    byte=int(msg[1:])
    newmsg=s.recv(byte)
    newmsg=str(newmsg,'utf-8')
    newmsg1=newmsg.split('@')
    for i in range(len(newmsg1)):  #loop over the mewmsg1 list
        if newmsg1[i]=='msg':   #where ever msg is present append the username after it and the message to the list 1
            list1.append((newmsg1[i+1],newmsg1[i+2]))  
        if newmsg1[i]=='file':    #whereever the word file is present append the username and the filename following it 
            list2.append((newmsg1[i+1],newmsg1[i+2]))
            with open(newmsg1[i+2],'a') as file:
                file.write(newmsg1[i+3])
    return (list1)


def sendMessageAll(socket,listofusers,message):
    for i in listofusers:
        sendMessage(socket,i,message)


class Player:
    def __init__(self,gameplay,position,money,mortgagedProperties,unmortgagedProperties,allProperties,playername,image):
        self.cardImage=0
        self.huts=0         #no of huts the player owns
        self.manors=0    #no of manors the player owns
        self.jailcards=0   #no of jail cards a player has
        self.gameplay=gameplay   #the entire gameplay class
        self.position=position   #current player postion
        self.money=money
        self.mortgagedProperties=mortgagedProperties     #list of mortgaged properties(properties stored as dictionaries in a list)
        self.unmortgagedProperties=unmortgagedProperties #list of unmortgaged properties
        self.allProperties=allProperties       #list of all properties
        self.playername=playername    #player name
        self.image=image
        self.turn=self.gameplay.listofusers.index(self.playername)   #turn no of user
        load=Image.open(self.image)                      #the token image is loaded for each player
        load=load.resize((15,15),Image.ANTIALIAS)
        render=ImageTk.PhotoImage(load)
        self.token=Label(self.gameplay.canvas, image=render)
        self.token.image=render
        self.token.place(x=self.gameplay.propertydictionary[self.position%40]['X'],y=self.gameplay.propertydictionary[self.position%40]['Y']+(self.turn*20))    #token placed at starting position
        self.gameplay.canvas.after(1000,self.getMail)   #get mail function called after every 1000 ms.
  
    def displaydailyprophetCard(self,number):       #function for displaying a daily prophet card
        card=self.gameplay.dailyProphetCards[number]
        load=Image.open(card)
        render=ImageTk.PhotoImage(load)
        self.cardImage=Label(self.gameplay.canvas, image=render)
        global cardImage
        self.cardImage.image=render
        self.cardImage.place(x=120,y=270)

    def displayquibblerCard(self,number):          #function for displaying a quibbler card on board
        card=self.gameplay.quibblerCards[number]
        load=Image.open(card)
        render=ImageTk.PhotoImage(load)
        self.cardImage=Label(self.gameplay.canvas, image=render)
        global cardImage
        self.cardImage.image=render
        self.cardImage.place(x=120,y=270)

    def getMail(self):      #the get mail function modififed for this class
        msglist=[]
        self.gameplay.socket.send(b'@rxmsg\n')
        msg=self.gameplay.socket.recv(6)
        byte=int(msg[1:])
        newmsg=self.gameplay.socket.recv(byte)
        newmsg=str(newmsg,'utf-8')
        newmsg1=newmsg.split('@')
        for i in range(len(newmsg1)):  #loop over the mewmsg1 list
            if newmsg1[i]=='msg':   #where ever msg is present append the username after it and the message to the list 1
                msglist.append((newmsg1[i+1],newmsg1[i+2]))  
            if newmsg1[i]=='file':    #whereever the word file is present append the username and the filename following it 
                list2.append((newmsg1[i+1],newmsg1[i+2]))
                with open(newmsg1[i+2],'a') as file:
                    file.write(newmsg1[i+3])
        if msglist!=[]:
            self.gameplay.processMsg(msglist)
        self.gameplay.canvas.after(1000,self.getMail)




    def afterRoll(self,a,whoseturn,listofusers):   #this function is called when the player rolls the die
        self.whoseturn=whoseturn
        self.listofusers=listofusers
        self.position+=a      #position incremented by number on the die
        if self.position>=40:   #is postion becomes the starting position or greater than that after increment so 200 money added
            self.money+=200

        self.position=self.position%40     #since 40 places so we mod it by 40 
        
        if self.position==30:   #this is the position for going to jail
            self.position=10    #position set to jail 
            if self.jailcards>=1: #if the player has some jail cards
                tempwn=Tk()
                tempwn.withdraw()
                a=messagebox.askyesno('You have been sent to Azkaban. You can use a jail card to get out of jail. Press OK to use the jail card. Otherwise 50 Galleons will be deducted from your Gringotts Account')
                if a==True:       #either the jail card is used or 50 galleons are deducted
                    self.jailcards-=1
                else:
                    self.money-=50
            else:
                messagebox.showinfo(self.gameplay.canvas,'You have been sent to Azkaban.')
                self.money-=50

        if self.position==4:        #if the player landed on ministry of magic tax
            self.money-=200
            self.gameplay.l1.config(text=self.playername+str(self.money))
            tempwn=Tk()
            tempwn.withdraw()
            messagebox.showinfo(self.gameplay.canvas,'You paid 200 Galleons in Ministry of Magic Tax')

        if self.position==38:       #if the player landed on paying the gringotts bank fee
            self.money-=100
            self.gameplay.l1.config(text=self.playername+str(self.money))
            tempwn=Tk()
            tempwn.withdraw()
            messagebox.showinfo(self.gameplay.canvas,'You paid 100 Galleons as Gringotts Bank Fee')

        if self.position==2 or self.position==17 or self.position==33:    #if the player landed on daily prophet position
            self.dailyProphet=True
            cardno=random.randint(1,16)  
            if cardno==1:         #for each card what should happen is hardcoded
                self.displayprophetCard(cardno)
                self.cardImage.place_forget()
                self.position=0
            
            if cardno==2:
                self.displaydailyprophetCard(cardno)     
                self.cardImage.place_forget()
                self.money+=50
                self.gameplay.l1.config(text=self.playername+str(self.money))
                self.gameplay.player2.money-=50
                self.gameplay.l2.config(text=self.gameplay.player2.playername+str(self.gameplay.player2.money))
                
            if cardno==3:
                self.displaydailyprophetCard(cardno)
                self.cardImage.place_forget()
                self.money-=(40*self.huts)+(115*self.manors)
                self.gameplay.l1.config(text=self.playername+str(self.money))

            if cardno==4:
                self.displaydailyprophetCard(cardno)
                self.cardImage.place_forget()
                self.money+=10
                self.gameplay.l1.config(text=self.playername+str(self.money))
                
            if cardno==5:
                self.displaydailyprophetCard(cardno)
                self.cardImage.place_forget()
                self.jailcards+=1
                
            if cardno==6:
                self.displaydailyprophetCard(cardno)
                self.cardImage.place_forget()
                self.position=10
                
            if cardno==7:
                self.displaydailyprophetCard(cardno)
                self.cardImage.place_forget()
                self.money+=200
                self.gameplay.l1.config(text=self.playername+str(self.money))
                    
                
            if cardno==8:
                self.displaydailyprophetCard(cardno)
                self.cardImage.place_forget()
                self.money-=150
                self.gameplay.l1.config(text=self.playername+str(self.money))
            if cardno==9:
                self.displaydailyprophetCard(cardno)
                self.cardImage.place_forget()
                self.money+=100
                self.gameplay.l1.config(text=self.playername+str(self.money))
                
            if cardno==10:
                self.displaydailyprophetCard(cardno)
                self.cardImage.place_forget()
                self.money+=100
                self.gameplay.l1.config(text=self.playername+str(self.money))
                
            if cardno==11:
                self.displaydailyprophetCard(cardno)
                self.cardImage.place_forget()
                self.money-=50
                self.gameplay.l1.config(text=self.playername+str(self.money))
                
            if cardno==12:
                self.displaydailyprophetCard(cardno)
                self.cardImage.place_forget()
                self.money+=20
                self.gameplay.l1.config(text=self.playername+str(self.money))
                
            if cardno==13:
                self.displaydailyprophetCard(cardno)
                self.cardImage.place_forget()
                self.money+=45
                self.gameplay.l1.config(text=self.playername+str(self.money))
                
            if cardno==14:
                self.displaydailyprophetCard(cardno)
                self.cardImage.place_forget()
                self.money-=100
                self.gameplay.l1.config(text=self.playername+str(self.money))
                
            if cardno==15:
                self.displaydailyprophetCard(cardno)
                self.cardImage.place_forget()
                self.money+=100
                self.gameplay.l1.config(text=self.playername+str(self.money))
                
            if cardno==16:
                self.displaydailyprophetCard(cardno)
                self.cardImage.place_forget()
                self.money+=25
                self.gameplay.l1.config(text=self.playername+str(self.money))


        if self.position==7 or self.position==22 or self.position==36:
            cardno=random.randint(1,16)
            if cardno==1:
                self.displayquibblerCard(cardno)
                self.cardImage.place_forget()
                if self.position<24:
                    self.position=24
                else:
                    self.position=24
                    self.money+=200    
                    self.gameplay.l1.config(text=self.playername+str(self.money))
                
            if cardno==2:
                self.displayquibblerCard(cardno)
                self.cardImage.place_forget()
                self.position=39
                
            if cardno==3:
                self.displayquibblerCard(cardno)
                self.cardImage.place_forget()
                self.position=0
                
            if cardno==4:
                self.displayquibblerCard(cardno)
                self.cardImage.place_forget()
                if self.position<11:
                    self.position=11
                else:
                    self.position=11
                    self.money+=200
                    self.gameplay.l1.config(text=self.playername+str(self.money))

            if cardno==5:
                self.displayquibblerCard(cardno)
                self.cardImage.place_forget()
                if self.position>12 and self.position<28:
                    self.position=28
                else:
                    self.position=12
                
            if cardno==6:
                self.displayquibblerCard(cardno)
                self.cardImage.place_forget()
                self.money-=(25*self.huts)+(100*self.manors)
                self.gameplay.l1.config(text=self.playername+str(self.money))
                
            if cardno==7:
                self.displayquibblerCard(cardno)
                self.cardImage.place_forget()
                self.jailcards+=1
                
            if cardno==8:
                self.displayquibblerCard(cardno)
                self.cardImage.place_forget()
                self.money+=150
                self.gameplay.l1.config(text=self.playername+str(self.money))
                
            if cardno==9:
                self.displayquibblerCard(cardno)
                self.cardImage.place_forget()
                self.position=10
                
            if cardno==10:
                self.displayquibblerCard(cardno)
                self.cardImage.place_forget()
                self.money+=50
                self.gameplay.l1.config(text=self.playername+str(self.money))
                
            if cardno==11:
                self.displayquibblerCard(cardno)
                self.cardImage.place_forget()
                if self.position>5 and self.position<15:
                    self.position=15
                elif self.postion>15 and self.position<25:
                    self.position=25
                elif self.position>25 and self.position<35:
                    self.position=35
                else:
                    self.position=5
                
            if cardno==12:
                self.displayquibblerCard(cardno)
                self.cardImage.place_forget()
                if self.position>5 and self.position<15:
                    self.position=15
                elif self.postion>15 and self.position<25:
                    self.position=25
                elif self.position>25 and self.position<35:
                    self.position=35
                else:
                    self.position=5
                
            if cardno==13:
                self.displayquibblerCard(cardno)
                self.cardImage.place_forget()
                self.money-=15
                self.gameplay.l1.config(text=self.playername+str(self.money))
                
            if cardno==14:
                self.displayquibblerCard(cardno)
                self.cardImage.place_forget()
                self.money-=50
                self.gameplay.l1.config(text=self.playername+str(self.money))
                self.gameplay.player2.money+=50
                self.gameplay.l2.config(text=self.gameplay.player2.playername+str(self.gameplay.player2.money))
                
            if cardno==15:
                self.displayquibblerCard(cardno)
                self.cardImage.place_forget()
                self.position-=3
                
            if cardno==16:
                self.displayquibblerCard(cardno)
                self.cardImage.place_forget()
                if self.position<5:
                    self.position=5
                else:
                    self.money+=200
                    self.gameplay.l1.config(text=self.playername+str(self.money))
                    self.position=5
                

        self.token.place(x=self.gameplay.propertydictionary[self.position]['X'],y=self.gameplay.propertydictionary[self.position]['Y'])     #in the end the token is placed based on the new location
        if self.money==0 and self.huts==0 and self.manors==0 and self.unmortgagedProperties==[]:   #is this is the condition the player becomes bankrupt
            tempwn=Tk()
            tempwn.withdraw()
            messagebox.showinfo('','You went Bankrupt. Player 2 Wins')
            message='You won the game!!!'
            sendMessageAll(self.gameplay.socket,self.gameplay.listofusers[:self.turn]+self.gameplay.listofusers[self.turn+1:],message)


        if self.gameplay.propertydictionary[self.position] in self.gameplay.player2.unmortgagedProperties:    #if the current position property is in the second person's unmortgaged properties so rent is deducted
            
            rent=self.gameplay.propertydictionary[self.position].get('Rent',0)     
            if self.money<rent:
                if self.huts==0 and self.manors==0 and self.unmortgagedProperties==[]:
                    tempwn=Tk()
                    tempwn.withdraw()
                    messagebox.showinfo('','You went Bankrupt. Player 2 Wins')
                    message='You won the game!!!'
                    sendMessageAll(self.gameplay.socket,self.gameplay.listofusers[:self.turn]+self.gameplay.listofusers[self.turn+1:],message)
                
                else:
                    tempwn=Tk()
                    tempwn.withdraw()
                    if messagebox.showinfo(self.gameplay.canvas,'You do not have sufficient money to pay rent. You have to mortgage/sell one of your properties')==True:
                        self.gameplay.disableall()
                        self.gameplay.sellbtn.config(state=NORMAL)
                        self.gameplay.mortbtn.config(state=NORMAL)
            else:
                self.gameplay.player1.money-=self.gameplay.propertydictionary[self.position].get('Rent',0)
                self.gameplay.player2.money+=self.gameplay.propertydictionary[self.position].get('Rent',0)
                self.gameplay.l1.config(text=self.gameplay.player1name+str(self.gameplay.player1.money))
                self.gameplay.l2.config(text=self.gameplay.player2.playername+str(self.gameplay.player2.money))
                tempwn=Tk()
                tempwn.withdraw()
                messagebox.showinfo(self.gameplay.canvas,'This property is owned by '+self.gameplay.player2.playername+' You paid him '+str(rent)+' Galleons as Rent.')

        elif self.gameplay.propertydictionary[self.position]['Card'] != None:      #if the property is not owned by anyone the card is displayed
            card=self.gameplay.propertydictionary[self.position]['Card']
            load=Image.open(card)
            render=ImageTk.PhotoImage(load)
            self.cardImage=Label(self.gameplay.canvas, image=render)
            self.cardImage.image=render
            self.cardImage.place(x=120,y=270)


    def afterturn(self):    #this happens when the user presses the endturn button
        if self.cardImage:
            self.cardImage.place_forget()
        message={'Position':self.position,'Player':self.playername,'Turn':self.whoseturn,'Money':self.money,'Jail Cards':self.jailcards,'Mortgaged Properties':self.mortgagedProperties,'Un Mortgaged Properties':self.unmortgagedProperties,'All Properties':self.allProperties}
        message=json.dumps(message)
        sendMessageAll(socket,self.gameplay.listofusers[:self.turn]+self.gameplay.listofusers[self.turn+1:],message)
        self.gameplay.disableall()




  
class gameplay:    #this is the gameplay class
    def __init__(self,geometry,image,title,propertydictionary,quibblerCards,dailyProphetCards,socket,listofusers,propertygroups):
        self.propertygroups=propertygroups  
        self.player1name=M[0]     #this is the name of the player who logs in 
        self.listofusers=listofusers   #this is the list of users
        self.socket=socket         
        self.whoseturn=0    #this variable is updated
        self.geometry=geometry
        self.image=image
        self.title=title
        self.propertydictionary=propertydictionary
        self.quibblerCards=quibblerCards
        self.dailyProphetCards=dailyProphetCards
        self.gp=Toplevel()
        self.gp.title(self.title)
        self.gp.geometry(self.geometry)
        self.canvas=Canvas(self.gp) 
        self.canvas.pack(expand=YES, fill=BOTH)
        load=Image.open(self.image)
        load=load.resize((866,700),Image.ANTIALIAS)
        render=ImageTk.PhotoImage(load)
        img=Label(self.canvas, image=render)
        img.image=render
        img.place(x=0, y=0)
        self.dice1=Button(self.canvas,text=0,width=5,height=2)     #this block creates the buttons
        self.dice1.place(x=1250,y=613)
        self.dice2=Button(self.canvas,text=0,width=5,height=2)
        self.dice2.place(x=1300,y=613)
        self.rollbtn=Button(self.canvas,text='Roll',width=10,height=2)
        self.rollbtn.bind('<Button-1>',self.rolldie)
        self.rollbtn.place(x=881,y=555)
        self.endturnbtn=Button(self.canvas,text='End Turn',width=10,height=2)
        self.endturnbtn.bind('<Button-1>',self.endturn)
        self.endturnbtn.place(x=970,y=555)
        self.viewbtn=Button(self.canvas,text='View',width=10,height=2,command=self.viewbtnpress)
        self.viewbtn.place(x=1059,y=555)
        self.sellbtn=Button(self.canvas,text='Sell',width=10,height=2,command=self.sellproperty)
        self.sellbtn.place(x=1148,y=555)
        self.mortbtn=Button(self.canvas,text='Mortgage',width=10,height=2,command=self.mortgageproperty)
        self.mortbtn.place(x=1237,y=555)
        self.unmortbtn=Button(self.canvas,text='Un-Mortgage',width=10,height=2,command=self.unmortgageproperty)
        self.unmortbtn.place(x=881,y=613)
        self.buybtn=Button(self.canvas,text='Buy',width=10,height=2)
        self.buybtn.bind('<Button-1>',self.buyProperty)
        self.buybtn.place(x=970,y=613)
        self.listofusers1=[]
        for i in self.listofusers:
            self.listofusers1.append(i)
        self.listofusers1.remove(self.player1name)
        self.player1=Player(self,0,1500,[],[],[],self.player1name,'./Pictures/redsquare.jpg')
        self.player2=Player(self,0,1500,[],[],[],self.listofusers1[0],'./Pictures/redsquare.jpg')
        self.l1=Label(self.canvas,text=self.player1name+str(self.player1.money))
        self.l1.place(x=(965+(0*240)),y=5)
        self.t1=Listbox(self.canvas,height=15,width=35,relief=SUNKEN)
        self.t1.place(x=(881+(0*240)),y=30)
        self.l2=Label(self.canvas,text=self.player2.playername+str(self.player2.money))
        self.l2.place(x=(965+(1*240)),y=5)
        self.t2=Listbox(self.canvas,height=15,width=35,relief=SUNKEN)
        self.t2.place(x=(881+(1*240)),y=30)

    def sellproperty(self):     #function for selling property
        index=self.t1.curselection()     
        propertyname=self.t1.get(index)
        propertyname=propertyname[:len(propertyname)]
        for i in self.player1.unmortgagedProperties:
            if i['Name']==propertyname:
                propertyindex=self.player1.unmortgagedProperties.index(i)
                self.player1.money+=self.player1.unmortgagedProperties[propertyindex]['Price']
                self.l1.config(text=self.player1name+' '+str(self.player1.money))
                del self.player1.unmortgagedProperties[propertyindex]
                self.player1.allProperties.remove(i)
                self.t1.delete(index)

    def unmortgageproperty(self):       #this function is for unmortgaging property
        index=self.t1.curselection()
        propertyname=self.t1.get(index)
        propertyname=propertyname[:len(propertyname)-1]
        for i in self.player1.mortgagedProperties:
            if i['Name']==propertyname:
                propertyindex=self.player1.mortgagedProperties.index(i)
                if self.player1.money>=self.player1.mortgagedProperties[propertyindex]['Mortgage Value']:
                    self.player1.money-=self.player1.mortgagedProperties[propertyindex]['Mortgage Value']
                    self.player1.unmortgagedProperties.append(i)
                    self.l1.config(text=self.player1name+' '+str(self.player1.money))
                    del self.player1.mortgagedProperties[propertyindex]
                    self.t1.delete(0,'end')
                    for i in self.player1.unmortgagedProperties:    #the list of requests is inserted in the listbox
                        self.t1.insert(END,i['Name'])
                    for j in self.player1.mortgagedProperties:
                        self.t1.insert(END,j['Name']+'M')
                else:
                    tempwn=Tk()
                    tempwn.withdraw()
                    messagebox.showinfo('','You have insufficient money to Un-Mortgage this property')

    def mortgageproperty(self):    #this function is for mortgaging properties
        index=self.t1.curselection()
        propertyname=self.t1.get(index)
        for i in self.player1.unmortgagedProperties:
            if i['Name']==propertyname:
                propertyindex=self.player1.unmortgagedProperties.index(i)
                self.player1.mortgagedProperties.append(i)
                self.player1.money+=self.player1.unmortgagedProperties[propertyindex]['Mortgage Value']
                self.l1.config(text=self.player1name+' '+str(self.player1.money))
                del self.player1.unmortgagedProperties[propertyindex]
                self.t1.delete(0,'end')
                for i in self.player1.unmortgagedProperties:    #the list of requests is inserted in the listbox
                    self.t1.insert(END,i['Name'])
                for j in self.player1.mortgagedProperties:
                    self.t1.insert(END,j['Name']+'M')

    def viewbtnpress(self):            #this happens when the user presses the view button 
        index=self.t1.curselection()
        propertyname=self.t1.get(index)
        for i in self.player1.unmortgagedProperties:
            if i['Name']==propertyname:
                propertyindex=self.player1.unmortgagedProperties.index(i)
        card=self.player1.unmortgagedProperties[propertyindex]['Card']
        load=Image.open(card)
        render=ImageTk.PhotoImage(load)
        cardImage=Label(self.canvas, image=render)
        cardImage.image=render
        cardImage.place(x=120,y=270)
        pricebtn=Button(self.canvas,text='Price: '+str(self.player1.unmortgagedProperties[propertyindex]['Price']),width=10,height=2)
        pricebtn.place(x=320,y=270)
 
    def disableall(self):         #this function diables all the buttons
        self.rollbtn.config(state=DISABLED)
        self.endturnbtn.config(state=DISABLED)
        self.sellbtn.config(state=DISABLED)
        self.mortbtn.config(state=DISABLED)
        self.unmortbtn.config(state=DISABLED)
        self.buybtn.config(state=DISABLED)
        self.viewbtn.config(state=DISABLED)

    def enableall(self):              #this function is for enabling all properties
        self.rollbtn.config(state=ACTIVE)
        self.endturnbtn.config(state=ACTIVE)
        self.sellbtn.config(state=ACTIVE)
        self.mortbtn.config(state=ACTIVE)
        self.unmortbtn.config(state=ACTIVE)
        self.buybtn.config(state=ACTIVE)
        self.viewbtn.config(state=ACTIVE)



    def rolldie(self,event):    #function for when i press roll button
        if (self.whoseturn)==self.player1.turn:
            self.enableall()
            num1=random.randint(1,6)
            num2=random.randint(1,6)
            self.dice1.config(text=num1)     #this block creates the buttons
            self.dice2.config(text=num2)
            self.whoseturn+=1
            self.whoseturn=self.whoseturn%2
            self.player1.afterRoll(num1+num2,self.whoseturn,self.listofusers)

    def buyProperty(self,event):            #function for buying property
        if self.player1.money>=self.propertydictionary[self.player1.position]['Price']:
            if self.propertydictionary[self.player1.position] not in self.player2.allProperties and self.propertydictionary[self.player1.position] not in self.player1.allProperties:
                if self.propertydictionary[self.player1.position]['Price']!=None:
                    self.t1.insert(END,self.propertydictionary[self.player1.position]['Name'])
                    self.player1.unmortgagedProperties.append(self.propertydictionary[self.player1.position])
                    self.player1.allProperties.append(self.propertydictionary[self.player1.position])
                    self.player1.money-=self.propertydictionary[self.player1.position]['Price']
                    self.l1.config(text=self.player1name+str(self.player1.money))
        else:
            tempwn=Tk()
            tempwn.withdraw()
            messagebox.showinfo('','You do not have enough money to buy this property.')
        
    def endturn(self,event):
        self.player1.afterturn()

    def processMsg(self,msglist):     #function for processing msg which is a dictionary
        msg=msglist[0][1]
        if msg=='You won the game!!!':
            tempwn=Tk()
            tempwn.withdraw()
            messagebox.showinfo('','Congratulations! You won the game!')

        else:
            msg=json.loads(msg)
            self.whoseturn=msg['Turn']
            if msg['Player']==self.player2.playername:
                self.player2.token.place(x=self.propertydictionary[msg['Position']]['X'],y=self.propertydictionary[msg['Position']]['Y'])
                self.player2.jailcards=msg['Jail Cards']
                self.player2.money=msg['Money']
                self.l2.config(text=self.player2.playername+str(self.player2.money))
                self.player2.unmortgagedProperties=msg['Un Mortgaged Properties']
                self.player2.mortgagedProperties=msg['Mortgaged Properties']
                self.player2.allProperties=msg['All Properties']

                if self.propertydictionary[msg['Position']] in self.player1.unmortgagedProperties:
                    self.player1.money+=self.propertydictionary[msg['Position']].get('Rent',0)
                    self.l1.config(text=self.player1name+str(self.player1.money))

                self.t2.delete(0,'end')
                for i in self.player2.unmortgagedProperties:    #the list of requests is inserted in the listbox
                    self.t2.insert(END,i['Name'])
                for j in self.player2.mortgagedProperties:
                    self.t2.insert(END,j['Name']+'    M')

class connectusers:         
    def __init__(self,socket):
        self.socket=socket
        if M[0]=='mshaheer':
            self.wn1=Tk()   #the attributes for chat window are set
            self.wn1.title('Monopoly: Harry Potter Edition')
            self.wn1.geometry('500x500')
            self.canvas=Canvas(self.wn1)
            self.canvas.grid(sticky=N+S+E+W)
            self.lb1=Label(self.canvas,text='Your Friends').grid(row=0,column=0)
            self.lb2=Label(self.canvas,text='Selected Users').grid(row=0,column=1)
            self.l1=Listbox(self.canvas,height=20,width=40,relief=SUNKEN)
            self.l1.grid(row=1,column=0)
            self.friends=getFriends(self.socket)# we get the list of friends and insert it in the respective listbox
            self.l2=Listbox(self.canvas,height=20,width=40,relief=SUNKEN)
            self.l2.grid(row=1,column=1)
            for i in range(len(self.friends)):
                self.l1.insert(END,self.friends[i])
            self.addbtn=Button(self.canvas,text='Add Players',width=10,height=2,command=self.addbtnpress)
            self.addbtn.grid(row=2,column=0)
            self.startbtn=Button(self.canvas,text='Start Game',width=10,height=2)
            self.startbtn.grid(row=2,column=2)
            self.sndrqstbtn=Button(self.canvas,text='Send Request',width=10,height=2,command=self.sendrequest)
            self.sndrqstbtn.grid(row=2,column=1)
            self.listofusers=['mshaheer']
            self.accepts=0
            self.canvas.after(1000,self.getMail)


        else:
            self.msgrecv=getMail(self.socket)
            msgfrom=self.msgrecv[0][0]
            self.msgrecv=self.msgrecv[0][1]
            self.listofusers=json.loads(self.msgrecv)
            tempwn=Tk()
            tempwn.withdraw()
            if messagebox.askyesno('Request to Play',msgfrom+'wants to play Monopoly with you. Your turn number is '+str(self.listofusers.index(M[0]))+' Press OK button to play')==True: 
                gameplay('1366x700','./Pictures/gameboard.jpg','Monopoly: Harry Potter Edition',propertydictionary,quibblerCards,dailyProphetCards,self.socket,self.listofusers,propertyGroups)
                sendMessage(self.socket,msgfrom,'Y')


    def addbtnpress(self):
        index=self.l1.curselection()
        user=self.l1.get(index)
        self.l2.insert(END,user)
        self.listofusers.append(user)


    def sendrequest(self):
        for i in self.listofusers[1:]:
            message=self.listofusers
            message=json.dumps(message)
            sendMessage(self.socket,i,message)
        messagebox.showinfo('','Waiting for response.....')


   
    def getMail(self):
        msglist=[]
        self.socket.send(b'@rxmsg\n')
        msg=self.socket.recv(6)
        byte=int(msg[1:])
        newmsg=self.socket.recv(byte)
        newmsg=str(newmsg,'utf-8')
        newmsg1=newmsg.split('@')
        for i in range(len(newmsg1)):  #loop over the mewmsg1 list
            if newmsg1[i]=='msg':   #where ever msg is present append the username after it and the message to the list 1
                msglist.append((newmsg1[i+1],newmsg1[i+2]))  
            if newmsg1[i]=='file':    #whereever the word file is present append the username and the filename following it 
                list2.append((newmsg1[i+1],newmsg1[i+2]))
                with open(newmsg1[i+2],'a') as file:
                    file.write(newmsg1[i+3])
        if msglist!=[]:
            if msglist[0][0] in self.listofusers and msglist[0][1]=='Y':
                self.accepts+=1
                if self.accepts==1:
                	messagebox.showinfo('','The selected players accepted your game request')
                	gameplay('1366x700','./Pictures/gameboard.jpg','Monopoly: Harry Potter Edition',propertydictionary,quibblerCards,dailyProphetCards,self.socket,self.listofusers,propertyGroups)
        self.canvas.after(1000,self.getMail)

    
class loginpage:   #this is the class for login page
    def __init__(self,wn,socket):
        self.lb1=Label(wn,text='Username').pack()
        self.e1=Entry(wn)
        self.e1.pack()
        self.lb2=Label(wn,text='Password').pack()
        self.e2=Entry(wn,show='*')
        self.e2.pack()
        self.b1=Button(wn,text='OK',command=self.okpress)
        self.b1.pack()
        
    def okpress(self):   #this function is executed when the ok button is pressed
        M.append(self.e1.get())
        M.append(self.e2.get())
        u=M[0]
        p=M[1]
        a=login(socket,u,p)
        if a==True:
            wn.destroy()   #login window is destroyed
            connectusers(socket)
        elif a==False:
            tempwn=Tk()
            tempwn.withdraw()
            messagebox.showerror('Error','Incorrect Username/Password Entered')


from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import random
import socket
import json
socket = StartConnection("86.36.46.10", 15112)   #connection is started
propertydictionary=[{'Name': 'Go','X':809,'Y':603,'Price':None,'Card':None},{'Name':'4 Privet Drive','X':717,'Y':603,'Price':60,'Card':'./Pictures/4privetdrive.png','Rent': 2,'Rent 1 Hut':10,'Rent 2 Huts':30,'Rent 3 Huts':90,'Rent 4 Huts':160,'Rent Manor': 250,'Mortgage Value':30},{'Name':'The Daily Prophet','X':645,'Y':603,'Price':None,'Card':None},{'Name':'The Leaky Cauldron','X':574,'Y':603,'Price':60,'Card':'./Pictures/leakycauldron.png','Rent': 4,'Rent 1 Hut':20,'Rent 2 Huts':60,'Rent 3 Huts':90,'Rent 4 Huts':180,'Rent Manor': 450,'Mortgage Value':30},{'Name':'Ministry Tax','X':503,'Y':603,'Price':200,'Card':None},{'Name':'Slytherin Common Room','X':431,'Y':603,'Price':200,'Card':'./Pictures/slytherinhouse.png','Rent': 25,'Rent 2 Houses':50,'Rent 3 Houses':100,'Rent 4 Houses':200,'Mortgage Value':100},{'Name':'Flourish and Blotts','X':360,'Y':603,'Price':100,'Card':'./Pictures/flourish.png','Rent': 6,'Rent 1 Hut':30,'Rent 2 Huts':90,'Rent 3 Huts':270,'Rent 4 Huts':400,'Rent Manor': 550,'Mortgage Value':50},{'Name':'Quibbler','X':289,'Y':603,'Price':None,'Card':None},{'Name':'Weasleys Wizard Wheezes','X':217,'Y':603,'Price':100,'Card':'./Pictures/weasleywizard.png','Rent': 6,'Rent 1 Hut':30,'Rent 2 Huts':90,'Rent 3 Huts':270,'Rent 4 Huts':400,'Rent Manor': 550,'Mortgage Value':50},{'Name':'Ollivanders','X':146,'Y':603,'Price':120,'Card':'./Pictures/ollivanders.png','Rent': 8,'Rent 1 Hut':40,'Rent 2 Huts':100,'Rent 3 Huts':300,'Rent 4 Huts':450,'Rent Manor':600,'Mortgage Value':60},{'Name':'Azkaban','X':55,'Y':603,'Card':None},{'Name':'Hagrids Hut','X':20,'Y':575,'Price':140,'Card':'./Pictures/hagridshut.png','Rent': 10,'Rent 1 Hut':50,'Rent 2 Huts':150,'Rent 3 Huts':450,'Rent 4 Huts':625,'Rent Manor':750,'Mortgage Value':70},{'Name':'The Floo Network','X':20,'Y':519,'Price':150,'Card':'./Pictures/floonetwork.png','Mortgage Value':75},{'Name':'Forbidden Forest','X':20,'Y':463,'Price':140,'Card':'./Pictures/forbiddenforest.png','Rent':10,'Rent 1 Hut':50,'Rent 2 Huts':150,'Rent 3 Huts':450,'Rent 4 Huts':625,'Rent Manor':750,'Mortgage Value':70},{'Name':'Quidditch Pitch','X':20,'Y':407,'Price':160,'Card':'./Pictures/quidditchpitch.png','Rent':12,'Rent 1 Hut':60,'Rent 2 Huts':180,'Rent 3 Huts':500,'Rent 4 Huts':700,'Rent Manor':900,'Mortgage Value':80},{'Name':'Hufflepuff common room','X':20,'Y':351,'Price':200,'Card':'./Pictures/hufflepuffhouse.png','Rent':25,'Rent 2 Houses':50,'Rent 3 Houses':100,'Rent 4 Houses':200,'Mortgage Value':100},{'Name':'Godrics Hollow','X':20,'Y':295,'Price':180,'Card':'./Pictures/godricshollow.png','Rent':14,'Rent 1 Hut':70,'Rent 2 Huts':200,'Rent 3 Huts':550,'Rent 4 Huts':750,'Rent Manor':950,'Mortgage Value':90},{'Name':'The Daily Prophet','X':20,'Y':239,'Card':None},{'Name':'The Burrow','X':20,'Y':183,'Price':180,'Card':'./Pictures/theburrow.png','Rent':14,'Rent 1 Hut':70,'Rent 2 Huts':200,'Rent 3 Huts':550,'Rent 4 Huts':750,'Rent Manor':950,'Mortgage Value':90},{'Name':'12 Grimmauld Place','X':20,'Y':127,'Price':200,'Card':'./Pictures/12grimmualdplace.png','Rent':16,'Rent 1 Hut':80,'Rent 2 Huts':220,'Rent 3 Huts':600,'Rent 4 Huts':800,'Rent Manor':1000,'Mortgage Value':100},{'Name':'Free Parking','X':55,'Y':20,'Card':None,'Rent':None},{'Name':'Shrieking Shack','X':146,'Y':20,'Price':220,'Card':'./Pictures/shriekingshack.png','Rent':18,'Rent 1 Hut':90,'Rent 2 Huts':250,'Rent 3 Huts':700,'Rent 4 Huts':875,'Rent Manor':1050,'Mortgage Value':110},{'Name':'The Quibbler','X':217,'Y':20,'Card':None},{'Name':'Honeydukes Sweetshop','X':289,'Y':20,'Price':220,'Card':'./Pictures/honeydukes.png','Rent':18,'Rent 1 Hut':90,'Rent 2 Huts':250,'Rent 3 Huts':700,'Rent 4 Huts':875,'Rent Manor':1050,'Mortgage Value':110},{'Name':'The Three Broomsticks','X':360,'Y':20,'Price':240,'Card':'./Pictures/3broomsticks.png','Rent':20,'Rent 1 Hut':100,'Rent 2 Huts':300,'Rent 3 Huts':750,'Rent 4 Huts':925,'Rent Manor':1100,'Mortgage Value':120},{'Name':'Ravenclaw Common Room','X':431,'Y':20,'Price':200,'Card':'./Pictures/ravenclawhouse.png','Rent':25,'Rent 2 Houses':50,'Rent 3 Houses':100,'Rent 4 Houses':200,'Mortgage Value':100},{'Name':'Kings Cross Station','X':503,'Y':20,'Price':260,'Card':'./Pictures/kingscross.png','Rent':22,'Rent 1 Hut':110,'Rent 2 Huts':330,'Rent 3 Huts':800,'Rent 4 Huts':975,'Rent Manor':1150,'Mortgage Value':130},{'Name':'Gringotts','X':574,'Y':20,'Price':250,'Card':'./Pictures/gringotts.png','Rent':22,'Rent 1 Hut':110,'Rent 2 Huts':330,'Rent 3 Huts':800,'Rent 4 Huts':975,'Rent Manor':1150,'Mortgage Value':130},{'Name':'Owl Post','X':645,'Y':20,'Price':150,'Card':'./Pictures/owlpost.png','Rent':None,'Mortgage Value':75},{'Name':'Ministry of Magic','X':717,'Y':20,'Price':280,'Card':'./Pictures/ministryofmagic.png','Rent':24,'Rent 1 Hut':120,'Rent 2 Huts':360,'Rent 3 Huts':850,'Rent 4 Huts':1025,'Rent Manor':1200,'Mortgage Value':140},{'Name':'Go To Azkaban','X':809,'Y':20,'Rent':None,'Card':None},{'Name':'Little Hangleton Graveyard','X':747,'Y':127,'Price':300,'Card':'./Pictures/littlehangletongraveyard.png','Rent':26,'Rent 1 Hut':130,'Rent 2 Huts':390,'Rent 3 Huts':900,'Rent 4 Huts':1100,'Rent Manor':1275,'Mortgage Value':150},{'Name':'The Chamber of Secrets','X':747,'Y':183,'Price':300,'Card':'./Pictures/chamberofsecrets.png','Rent':26,'Rent 1 Hut':130,'Rent 2 Huts':390,'Rent 3 Huts':900,'Rent 4 Huts':1100,'Rent Manor':1275,'Mortgage Value':150},{'Name':'The Daily Prophet','X':747,'Y':239,'Rent':None,'Card':None},{'Name':'Malfoy Manor','X':747,'Y':295,'Price':320,'Card':'./Pictures/malfoymanor.png','Rent':28,'Rent 1 Hut':150,'Rent 2 Huts':450,'Rent 3 Huts':1000,'Rent 4 Huts':1200,'Rent Manor':1400,'Mortgage Value':160},{'Name':'Gryffindor Common Room','X':747,'Y':351,'Price':200,'Card':'./Pictures/gryffindorhouse.png','Rent':25,'Rent 2 Houses':50,'Rent 3 Houses':100,'Rent 4 Houses':200,'Mortgage Value':100},{'Name':'The Quibbler','X':747,'Y':407,'Rent':None,'Card':None},{'Name':'Room of Requirement','X':747,'Y':463,'Price':350,'Card':'./Pictures/roomofrequirement.png','Rent':35,'Rent 1 Hut':175,'Rent 2 Huts':500,'Rent 3 Huts':1100,'Rent 4 Huts':1300,'Rent Manor':1500,'Mortgage Value':175},{'Name':'Gringotts Bank Fee','X':747,'Y':519,'Price':100,'Rent':None,'Card':None},{'Name':'Dumbledores Office','X':747,'Y':575,'Price':400,'Card':'./Pictures/dumbledoreoffice.png','Rent':50,'Rent 1 Hut':200,'Rent 2 Huts':600,'Rent 3 Huts':1400,'Rent 4 Huts':1700,'Rent Manor':2000,'Mortgage Value':200}]
quibblerCards={1:'./Pictures/Quibbler Cards/advanceto3broomsticks.png',2:'./Pictures/Quibbler Cards/advancetodumbledoreoffice.png',3:'./Pictures/Quibbler Cards/advancetogo1.png',4:'./Pictures/Quibbler Cards/advancetohagridhut.png',5:'./Pictures/Quibbler Cards/advancetoutility.png',6:'./Pictures/Quibbler Cards/dementors.png',7:'./Pictures/Quibbler Cards/getoutofazkaban1.png',8:'./Pictures/Quibbler Cards/goldensnitch.png',9:'./Pictures/Quibbler Cards/gotoazkaban1.png',10:'./Pictures/Quibbler Cards/gringottsdividend.png',11:'./Pictures/Quibbler Cards/housecommonroom.png',12:'./Pictures/Quibbler Cards/housecommonroom1.png',13:'./Pictures/Quibbler Cards/howler.png',14:'./Pictures/Quibbler Cards/imperiuscurse.png',15:'./Pictures/Quibbler Cards/pukingpastilles.png',16:'./Pictures/Quibbler Cards/slytherinhousecommonroom.png'}
dailyProphetCards={1:'./Pictures/Daily Prophet Cards/advancetogo.png',2:'./Pictures/Daily Prophet Cards/betonquidditch.png',3:'./Pictures/Daily Prophet Cards/cornishpixie.png',4:'./Pictures/Daily Prophet Cards/correctanspotion.png',5:'./Pictures/Daily Prophet Cards/getoutofazkaban.png',6:'./Pictures/Daily Prophet Cards/gotoazkaban.png',7:'./Pictures/Daily Prophet Cards/gringottserror.png',8:'./Pictures/Daily Prophet Cards/hogwartsfee.png',9:'./Pictures/Daily Prophet Cards/horcruxdestroy.png',10:'./Pictures/Daily Prophet Cards/houseelf.png',11:'./Pictures/Daily Prophet Cards/madampomfrey.png',12:'./Pictures/Daily Prophet Cards/ministryofmagicrefund.png',13:'./Pictures/Daily Prophet Cards/patronuscharm.png',14:'./Pictures/Daily Prophet Cards/saintmungo.png',15:'./Pictures/Daily Prophet Cards/trolldefeat.png',16:'./Pictures/Daily Prophet Cards/yuleballdate.png'}
propertyGroups={'Violet':[propertydictionary[1],propertydictionary[3]],'Sky Blue':[propertydictionary[6],propertydictionary[8],propertydictionary[9]],'Purple':[propertydictionary[11],propertydictionary[13],propertydictionary[14]],'Orange':[propertydictionary[16],propertydictionary[18],[19]],'Red':[propertydictionary[21],propertydictionary[23],propertydictionary[24]],'Yellow':[propertydictionary[26],propertydictionary[27],propertydictionary[29]],'Green':[propertydictionary[31],propertydictionary[32],propertydictionary[34]],'Blue':[propertydictionary[37],propertydictionary[39]]}
wn=Tk()  
wn.title('Login')
wn.geometry('200x200')
M=[]
loginpage(wn,socket)
mainloop()