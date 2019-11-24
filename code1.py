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
    def __init__(self,canvas,propertydictionary,position,money,mortgagedProperties,unmortgagedProperties,name,image,turn,socket):
        self.socket=socket
        self.turn=turn
        self.canvas=canvas
        self.propertydictionary=propertydictionary
        self.position=position
        self.money=money
        self.mortgagedProperties=mortgagedProperties
        self.unmortgagedProperties=unmortgagedProperties
        self.name=name
        self.image=image
        load=Image.open(self.image)
        load=load.resize((15,15),Image.ANTIALIAS)
        render=ImageTk.PhotoImage(load)
        self.token=Label(self.canvas, image=render)
        self.token.image=render
        print('pos+turn',self.position,self.turn)
        self.token.place(x=self.propertydictionary[self.position%39]['X'],y=self.propertydictionary[self.position%39]['Y']+(self.turn*20))
        self.msglist=[]  #this list is for usernames and messages
        self.canvas.after(1000,self.getMail)

    def getMail(self):
        self.socket.send(b'@rxmsg\n')
        msg=self.socket.recv(6)
        byte=int(msg[1:])
        newmsg=self.socket.recv(byte)
        newmsg=str(newmsg,'utf-8')
        newmsg1=newmsg.split('@')
        for i in range(len(newmsg1)):  #loop over the mewmsg1 list
            if newmsg1[i]=='msg':   #where ever msg is present append the username after it and the message to the list 1
                self.msglist.append((newmsg1[i+1],newmsg1[i+2]))  
            if newmsg1[i]=='file':    #whereever the word file is present append the username and the filename following it 
                list2.append((newmsg1[i+1],newmsg1[i+2]))
                with open(newmsg1[i+2],'a') as file:
                    file.write(newmsg1[i+3])
        print(self.msglist)
        self.canvas.after(1000,self.getMail)

    def afterRoll(self,a,whoseturn,listofusers):
        self.whoseturn=whoseturn
        self.listofusers=listofusers
        self.position+=a
        self.position=self.position%39
        self.token.place(x=self.propertydictionary[self.position]['X'],y=self.propertydictionary[self.position]['Y'])
        if self.propertydictionary[self.position]['Card'] != None:
            card=self.propertydictionary[self.position]['Card']
            load=Image.open(card)
            render=ImageTk.PhotoImage(load)
            self.cardImage=Label(self.canvas, image=render)
            self.cardImage.image=render
            self.cardImage.place(x=120,y=270)
        message={'Position':self.position,'Player':self.name,'Turn':self.whoseturn}
        message=json.dumps(message)
        sendMessageAll(socket,self.listofusers[1:],message)

    def afterturn(self):
        self.canvas.after(1000,self.getMail)
        if self.getMail()!=[]:
            self.msgrecv=self.getMail()
            self.msgrecv=self.msgrecv[0][1]
            self.msgrecv=json.loads(self.msgrecv)
            self.playerturn=self.msgrecv['fts']



     
class gameplay:
    def __init__(self,geometry,image,title,propertydictionary,socket,listofusers,myturn):
        if myturn==0:
            self.player1name='mshaheer'
            self.myturn=myturn
        else:
            self.player1name=myturn[0]
            self.myturn=myturn[1]
        self.listofusers=listofusers
        self.socket=socket
        self.whoseturn=0
        self.geometry=geometry
        self.image=image
        self.title=title
        self.propertydictionary=propertydictionary
        self.gp=Tk()
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
        for i in range(2):
            self.l=Label(self.canvas,text='Player '+str(i+1))
            self.l.place(x=(965+(i*240)),y=5)
            self.t=Listbox(self.canvas,height=15,width=35,relief=SUNKEN)
            self.t.place(x=(881+(i*240)),y=30)
        for y in range(2):
            self.l=Label(self.canvas,text='Player '+str(y+3))
            self.l.place(x=(965+(y*240)),y=275)
            self.t=Listbox(self.canvas,height=15,width=35,relief=SUNKEN)
            self.t.place(x=(881+(y*240)),y=300)
        self.dice1=Button(self.canvas,text=0,width=5,height=2)     #this block creates the buttons
        self.dice1.place(x=1200,y=613)
        self.dice2=Button(self.canvas,text=0,width=5,height=2)
        self.dice2.place(x=1250,y=613)
        self.rollbtn=Button(self.canvas,text='Roll',width=10,height=2)
        self.rollbtn.bind('<Button-1>',self.rolldie)
        self.rollbtn.place(x=881,y=555)
        self.endturnbtn=Button(self.canvas,text='End Turn',width=10,height=2)
        self.endturnbtn.place(x=970,y=555)
        self.buildbtn=Button(self.canvas,text='Build',width=10,height=2)
        self.buildbtn.place(x=1059,y=555)
        self.sellbtn=Button(self.canvas,text='Sell',width=10,height=2)
        self.sellbtn.place(x=1148,y=555)
        self.mortbtn=Button(self.canvas,text='Mortgage',width=10,height=2)
        self.mortbtn.place(x=1237,y=555)
        self.unmortbtn=Button(self.canvas,text='Un-Mortgage',width=10,height=2)
        self.unmortbtn.place(x=881,y=613)
        self.trdbtn=Button(self.canvas,text='Trade',width=10,height=2)
        self.trdbtn.place(x=970,y=613)
        self.player1=Player(self.canvas,self.propertydictionary,0,1500,0,0,self.player1name,'./Pictures/redsquare.jpg',self.myturn,self.socket)
        self.listofusers1=self.listofusers
        self.listofusers1.remove(self.player1name)
        print('users',self.listofusers1)
        print('users',self.listofusers)
        self.player2=Player(self.canvas,self.propertydictionary,0,1500,0,0,self.listofusers1[0],'./Pictures/redsquare.jpg',self.listofusers.index(self.listofusers1[0]),self.socket)
        self.player3=Player(self.canvas,self.propertydictionary,0,1500,0,0,self.listofusers1[1],'./Pictures/redsquare.jpg',self.listofusers.index(self.listofusers1[1]),self.socket)
        self.player4=Player(self.canvas,self.propertydictionary,0,1500,0,0,self.listofusers1[2],'./Pictures/redsquare.jpg',self.listofusers.index(self.listofusers1[2]),self.socket)

    def rolldie(self,event):    #function for when i press roll button
        if (self.whoseturn%2)==self.player1.turn:
            num1=random.randint(1,6)
            num2=random.randint(1,6)
            self.dice1.config(text=num1)     #this block creates the buttons
            self.dice2.config(text=num2)
            self.whoseturn+=1
            self.whoseturn=self.whoseturn%2
            self.player1.afterRoll(num1+num2,self.whoseturn,self.listofusers)

    def endturn(self):
        self.player1.afterturn()

class connectusers:
    def __init__(self,socket):
        self.socket=socket
        self.wn1=Tk()   #the attributes for chat window are set
        self.wn1.title('Monopoly: Harry Potter Edition')
        self.wn1.geometry('500x500')
        self.canvas=Canvas(self.wn1)
        self.canvas.grid(sticky=N+S+E+W)
        self.lb2=Label(self.canvas,text='Your Friends').grid(row=0,column=0)
        self.friends=getFriends(self.socket)# we get the list of friends and insert it in the respective listbox
        for i in range(len(self.friends)):
            var = BooleanVar()
            r=Checkbutton(self.canvas,text=self.friends[i],variable=var)
            r.grid(column=0,row=i+1)
        self.startbtn=Button(self.canvas,text='Start Game',width=10,height=2,command=self.startbtnpress)
        self.startbtn.grid(column=10,row=1)
        self.listofusers=['mshaheer','fts','iahmad','mansar']
        if M[0]=='mshaheer':
            for i in range (len(self.listofusers[1:])):
                message={self.listofusers[i+1]:i+1}
                message=json.dumps(message)
                sendMessage(self.socket,self.listofusers[i+1],message)
        else:
            self.msgrecv=getMail(self.socket)
            self.msgrecv=self.msgrecv[0][1]
            self.msgrecv=json.loads(self.msgrecv)
            for x,y in self.msgrecv.items():
                self.msgrecv=(x,y)
                print(self.msgrecv)


    def startbtnpress(self):
        self.wn1.destroy()
        if M[0]=='mshaheer':
            gameplay('1366x700','./Pictures/gameboard.jpg','Monopoly: Harry Potter Edition',propertydictionary,self.socket,self.listofusers,0)
        else:
            gameplay('1366x700','./Pictures/gameboard.jpg','Monopoly: Harry Potter Edition',propertydictionary,self.socket,self.listofusers,self.msgrecv)




class loginpage:   #this is the class for login page
    def __init__(self,wn,propertydictionary,socket):
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
            messagebox.showerror('Error','Incorrect Username/Password Entered')


from tkinter import *
from PIL import Image, ImageTk
import random
import socket
import json
#Dictionaries
socket = StartConnection("86.36.46.10", 15112)   #connection is started
propertydictionary=[{'Name': 'Go','X':809,'Y':603},{'Name':'4 Privet Drive','X':717,'Y':603,'Price':60,'Card':'./Pictures/4privetdrive.png'},{'Name':'The Daily Prophet','X':645,'Y':603,'Card':None},{'Name':'The Leaky Cauldron','X':574,'Y':603,'Price':60,'Card':'./Pictures/leakycauldron.png'},{'Name':'Ministry Tax','X':503,'Y':603,'Price':200,'Card':''},{'Name':'Slytherin Common Room','X':431,'Y':603,'Price':200,'Card':'./Pictures/slytherinhouse.png'},{'Name':'Flourish and Blotts','X':360,'Y':603,'Price':100,'Card':'./Pictures/flourish.png'},{'Name':'Quibbler','X':289,'Y':603,'Card':None},{'Name':'Weasleys Wizard Wheezes','X':217,'Y':603,'Price':100,'Card':'./Pictures/weasleywizard.png'},{'Name':'Ollivanders','X':146,'Y':603,'Price':120,'Card':'./Pictures/ollivanders.png'},{'Name':'Azkaban','X':55,'Y':603,'Card': None},{'Name':'Hagrids Hut','X':20,'Y':575,'Price':140,'Card':'./Pictures/hagridshut.png'},{'Name':'The Floo Network','X':20,'Y':519,'Price':150,'Card':'./Pictures/floonetwork.png'},{'Name':'Forbidden Forest','X':20,'Y':463,'Price':140,'Card':'./Pictures/forbiddenforest.png'},{'Name':'Quidditch Pitch','X':20,'Y':407,'Price':160,'Card':'./Pictures/quidditchpitch.png'},{'Name':'Hufflepuff common room','X':20,'Y':351,'Price':200,'Card':'./Pictures/hufflepuffhouse.png'},{'Name':'Godrics Hollow','X':20,'Y':295,'Price':180,'Card':'./Pictures/godricshollow.png'},{'Name':'The Daily Prophet','X':20,'Y':239,'Card':None},{'Name':'The Burrow','X':20,'Y':183,'Price':180,'Card':'./Pictures/theburrow.png'},{'Name':'12 Grimmauld Place','X':20,'Y':127,'Price':200,'Card':'./Pictures/12grimmauldplace.png'},{'Name':'Free Parking','X':55,'Y':20},{'Name':'Shrieking Shack','X':55,'Y':20,'Price':220,'Card':'./Pictures/shriekingshack.png'},{'Name':'The Quibbler','X':146,'Y':20,'Card':None},{'Name':'Honeydukes Sweetshop','X':217,'Y':20,'Price':220,'Card':'./Pictures/honeydukes.png'},{'Name':'The Three Broomsticks','X':289,'Y':20,'Price':240,'Card':'./Pictures/3broomsticks.png'},{'Name':'Ravenclaw Common Room','X':360,'Y':20,'Price':200,'Card':'./Pictures/ravenclawhouse.png'},{'Name':'Kings Cross Station','X':503,'Y':20,'Price':260,'Card':'./Pictures/kingscross.png'},{'Name':'Gringotts','X':574,'Y':20,'Price':250,'Card':'./Pictures/gringotts.png'},{'Name':'Owl Post','X':645,'Y':20,'Price':150,'Card':'./Pictures/owlpost.png'},{'Name':'Ministry of Magic','X':717,'Y':20,'Price':280,'Card':'./Pictures/ministryofmagic.png'},{'Name':'Go To Azkaban','X':809,'Y':20,'Card':None},{'Name':'Little Hangleton Graveyard','X':747,'Y':127,'Price':300,'Card':'./Pictures/littlehangletongraveyard.png'},{'Name':'The Chamber of Secrets','X':747,'Y':183,'Price':300,'Card':'./Pictures/chamberofsecrets.png'},{'Name':'The Daily Prophet','X':747,'Y':239,'Card':None},{'Name':'Malfoy Manor','X':747,'Y':295,'Price':320,'Card':'./Pictures/malfoymanor.png'},{'Name':'Gryffindor Common Room','X':747,'Y':351,'Price':200,'Card':'./Pictures/gryffindorhouse.png'},{'Name':'The Quibbler','X':747,'Y':407,'Card':None},{'Name':'Room of Requirement','X':747,'Y':463,'Price':350,'Card':'./Pictures/roomofrequirement.png'},{'Name':'Gringotts Bank Fee','X':747,'Y':519,'Price':100},{'Name':'Dumbledores Office','X':747,'Y':575,'Price':400,'Card':'./Pictures/dumbledoreoffice.png'}]
wn=Tk()  
wn.title('Login Chat Client')
wn.geometry('200x200')
M=[]
loginpage(wn,propertydictionary,socket)
mainloop()