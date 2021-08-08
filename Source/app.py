import numpy as np
import cv2
import pickle
import os
import pyqrcode
import png
from pyqrcode import QRCode
from pyzbar.pyzbar import decode
from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
import tkinter as tk
import MySQLdb as mysql
from shutil import copyfile
from datetime import datetime
mydb=mysql.connect(
    host="localhost",
    user="root",
    password="Nrx07CR7.")
mycursor=mydb.cursor()
mycursor.execute("create database if not exists miniprojectpython;")
mycursor.execute("use miniprojectpython;")
mycursor.execute("create table if not exists user(registration_number int(6) primary key,name varchar(50),college_name varchar(50),cgpa decimal(4,2),branch varchar(10),year int(2));")
l=[]
mycursor.execute("select registration_number,name,college_name,branch,year from user;")
res=mycursor.fetchall()
for i in res:
    l.append(i[1]+' , '+i[2]+' , '+i[3]+' , year = '+str(i[4])+'    -    '+str(i[0]))
def getnames():
    mycursor.execute("select registration_number,name,college_name,branch,year from user;")
    res=mycursor.fetchall()
    l=[]
    for i in res:
        l.append(i[1]+','+i[2]+', '+i[3]+', year = '+str(i[4])+'    -    '+str(i[0]))
def insertvalue(data,root):
    query="insert into user (registration_number,name,college_name,cgpa,branch,year) values (%s,%s,%s,%s,%s,%s);"
    val=(str(data[0]),str(data[1]),str(data[2]),str(data[3]),str(data[4]),str(data[5]))
    mycursor.execute (query,val)
    mydb.commit()
    def insdone():
        r.destroy()
        root.destroy()
        searchpage()
    r = Tk()
    r.geometry('215x75')
    r.title("Warning.")
    r.iconbitmap('gui_images/hacker.ico')
    label_1 = Label(r, text="Inserted !",width=20,font=("bold", 10))
    label_1.place(x=10,y=10)
    Button(r, text='Okay.',width=10,bg='brown',fg='white', command=insdone).place(x=125,y=40)
    r.mainloop()
def checkpersondata(number):
    number=int(number)
    mycursor.execute("select registration_number from user;")
    res=mycursor.fetchall()
    flag=False
    for x in res:
        x=int(x[0])
        if x==number:
            flag=True
    return flag
def getdata(number):
    number=str(number)
    mycursor.execute("select * from user where registration_number = "+number+";")
    res=mycursor.fetchall()
    return(res)
class Form:
    def __init__(self,root):
        def funca():
            root.destroy()
        def funcb():
            searchpage()
        self.bg1 = ImageTk.PhotoImage(file='gui_images/black_bg.png')
        self.my_canvas=Canvas(root,height=1700, width=1400)
        self.my_canvas.pack(fill = "both",expand=True)
        self.my_canvas.create_image(0,0, image=self.bg1,anchor="nw")
        self.f1 = LabelFrame (root).place(x=0,y=0)
        self.l1 = Label(self.f1)
        self.l1.configure(width=162,height=35,background='white')
        l1_window = self.my_canvas.create_window(70,100,anchor="nw",window=self.l1)
        self.f2 = LabelFrame (root).place(x=0,y=0)
        self.l2 = Label(self.f2)
        self.l2.configure(width=157,height=33,background='black')
        l2_window = self.my_canvas.create_window(85,115,anchor="nw",window=self.l2)
        self.my_canvas.create_text(155,55, text = "Form:",font=("Times New Roman",50),fill='white')
        self.l3 = Label(self.f2, text = "College Name                      :",font=("Times New Roman",25),fg='white',bg='black').place(x=150,y=205)
        self.l4 = Label(self.f2, text = "Registration Number           :",font=("Times New Roman",25),fg='white',bg='black').place(x=150,y=255)
        self.l5 = Label(self.f2, text = "Branch                                 :",font=("Times New Roman",25),fg='white',bg='black').place(x=150,y=310)
        self.l6 = Label(self.f2, text = "Year                                     :",font=("Times New Roman",25),fg='white',bg='black').place(x=150,y=365)
        self.l7 = Label(self.f2, text = "CGPA                                  :",font=("Times New Roman",25),fg='white',bg='black').place(x=150,y=420)
        self.l8 = Label(self.f2, text = "Name                                    :",font=("Times New Roman",25),fg='white',bg='black').place(x=150,y=150)
        self.e1 = Entry(self.f2,width=50,fg="black",bg="white", font=('Times New Roman',15,"bold"))
        self.e1.place(x=550,y=210)
        self.e2 = Entry(self.f2,width=50,fg="black",bg="white", font=('Times New Roman',15,"bold"))
        self.e2.place(x=550,y=265)
        self.e3 = Entry(self.f2,width=50,fg="black",bg="white", font=('Times New Roman',15,"bold"))
        self.e3.place(x=550,y=320)
        self.e4 = Entry(self.f2,width=50,fg="black",bg="white", font=('Times New Roman',15,"bold"))
        self.e4.place(x=550,y=375)
        self.e5 = Entry(self.f2,width=50,fg="black",bg="white", font=('Times New Roman',15,"bold"))
        self.e5.place(x=550,y=430)
        self.e6 = Entry(self.f2,width=50,fg="black",bg="white", font=('Times New Roman',15,"bold"))
        self.e6.place(x=550,y=160)
        self.b1 = Button(self.f2, text="SUBMIT", font=('Times New Roman',13,"bold"),borderwidth=5, padx=50,pady=1,bg="white",fg="black",activebackground = 'black',command=lambda: self.subclick(root)).place(x=875,y=500)
        self.b2 = Button(self.f2, text="BACK", font=('Times New Roman',13,"bold"),borderwidth=5, 
        width=15,height=1,bg="white",fg="black",activebackground = 'black',command=lambda: [funca(),funcb()]).place(x=1110,y=5)
    def subclick(self,root):
        data=[self.e2.get(),self.e6.get(),self.e1.get(),self.e5.get(),self.e3.get(),self.e4.get()]
        if checkpersondata(data[0]):
            def notexist():
                r.destroy()
                root.destroy()
                formrun()
            r = Tk()
            r.geometry('215x75')
            r.title("Warning.")
            r.iconbitmap('gui_images/hacker.ico')
            label_1 = Label(r, text="User already exists !",width=20,font=("bold", 10))
            label_1.place(x=10,y=10)
            Button(r, text='Okay.',width=10,bg='brown',fg='white', command=notexist).place(x=125,y=40)
            r.mainloop()
        else:
            insertvalue(data,root)
def formrun():
    l=[]
    root = Tk()
    root.title("Frame Tkinter Application") #Giving a title to ba
    root.iconbitmap('gui_images/hacker.ico')
    root.state("zoomed")
    mb=Form(root)
    root.mainloop()
class Printing_page:
    def checkey(self,event,root):
        value = event.widget.get()
        if value == '':
            self.lb.place(x=33444,y=85)
        else:
            data = []
            mycursor.execute("select registration_number,name,college_name,branch,year from user;")
            res=mycursor.fetchall()
            l=[]
            for i in res:
                l.append(i[1]+','+i[2]+', '+i[3]+', year = '+str(i[4])+'    -    '+str(i[0]))
            for item in l:
                if value.lower() in item.lower():
                    data.append(item)	
            self.lb.place(x=33444,y=85)
            self.lb=s= Listbox(self.f2,width=65,height=len(data),fg="black",bg="white", font=('Times New Roman',15,"bold"))
            self.lb.place(x=265,y=89)
            def clickEvent(evt):
                    value=str(self.lb.get(ACTIVE))
                    self.e1.delete(0,'end')
                    value=value[value.find('-')+1+4:len(value)]
                    self.e1.insert(0,value)
            self.lb.bind('<<ListboxSelect>>',clickEvent)		
            # update data in listbox
            self.update(data)
    def update(self,data):
        # clear previous data
        self.lb.delete(0, 'end')
        # put new data
        for item in data:
            self.lb.insert('end', item)
    def __init__(self,root):
        def func111():
            root.destroy()
        def func222():
            dir='qrcode/'
            for f in os.listdir(dir):
                os.remove(os.path.join(dir,f))
            page_2_run()
        def dwld():
            dir1='qrcode/'
            newdir='downloads/'
            for f in os.listdir(dir1):
                copyfile(os.path.join(dir1,f),os.path.join(newdir,f))
        self.bg1 = ImageTk.PhotoImage(file='gui_images/black_bg.png')
        self.my_canvas=Canvas(root,height=1700, width=1400)
        self.my_canvas.pack(fill = "both",expand=True)
        self.my_canvas.create_image(0,0, image=self.bg1,anchor="nw")
        self.f1 = LabelFrame (root).place(x=0,y=0)
        self.l1 = Label(self.f1)
        self.l1.configure(width=100,height=24,background='white')
        l1_window = self.my_canvas.create_window(400,165,anchor="nw",window=self.l1)
        self.f2 = LabelFrame (root).place(x=0,y=0)
        self.l2 = Label(self.f2)
        self.l2.configure(width=96,height=22,background='black')
        l2_window = self.my_canvas.create_window(414,180,anchor="nw",window=self.l2)
        self.f3 = LabelFrame (root).place(x=0,y=0)
        self.l3 = Label(self.f3)
        self.l3.configure(width=30,height=13,background='grey')
        l3_window = self.my_canvas.create_window(100,200,anchor="nw",window=self.l3)
        self.my_canvas.create_text(160,78, text = "Search :",font=("Times New Roman",25,'bold'),fill='white')
        self.b3 = Button(self.f2, text="BACK", font=('Times New Roman',13,"bold"),borderwidth=5, width=15,height=1,bg="white",fg="black",activebackground = 'black',command=lambda: [func111(),func222()]).place(x=1110,y=5)
        self.b1 = Button(self.f2, text="SEARCH", font=('Times New Roman',13,"bold"),borderwidth=5, width=15,height=1,bg="white",fg="black",activebackground = 'black',command=lambda: self.searchclick(root)).place(x=960,y=60)
        self.b4 = Button(self.f2, text="DELETE", font=('Times New Roman',13,"bold"),borderwidth=5, width=15,height=1,bg="white",fg="black",activebackground = 'black',command=lambda: self.delclick(root)).place(x=960,y=100)
        self.b2 = Button(self.f2, text="DOWNLOAD", font=('Times New Roman',13,"bold"),borderwidth=5, padx=50,pady=1,bg="white",fg="black",activebackground = 'black', command=dwld).place(x=100,y=470)
        self.e1 = Entry(self.f2,width=65,fg="black",bg="white", font=('Times New Roman',15,"bold"))
        self.e1.place(x=265,y=65)
        self.e1.bind('<KeyRelease>',lambda event: self.checkey(event,root))
        self.lb = Listbox(self.f2,width=65,height=0,fg="black",bg="white", font=('Times New Roman',15,"bold"))
        self.lb.place(x=11265,y=85)
    def	myclick(self,root,data):            
            self.a = data[1]
            self.b = data[2]
            self.c = data[0]
            self.d = data[4]
            self.f = data[5]
            self.g = data[3]
            self.l4 = Label(self.f2, text = "Name  :"+"  "+ str(self.a),font=("Times New Roman",25),fg='white',bg='black',command = self.b1).place(x=450,y=200)
            self.l5 = Label(self.f2, text = "College Name  :" +"  "+ str(self.b),font=("Times New Roman",25),fg='white',bg='black',command = self.b1).place(x=450,y=250)
            self.l6 = Label(self.f2, text = "Registration Number  :" +"  "+ str(self.c),font=("Times New Roman",25),fg='white',bg='black',command = self.b1).place(x=450,y=300)
            self.l7 = Label(self.f2, text = "Branch  :" +"  "+ str(self.d),font=("Times New Roman",25),fg='white',bg='black',command = self.b1).place(x=450,y=350)
            self.l8 = Label(self.f2, text = "Year  :" +"  "+ str(self.f),font=("Times New Roman",25),fg='white',bg='black',command = self.b1).place(x=450,y=400)
            self.l9 = Label(self.f2, text = "CGPA  :" +"  "+ str(self.g),font=("Times New Roman",25),fg='white',bg='black',command = self.b1).place(x=450,y=450)
            iii=Image.open("qrcode/"+changenamestate(data[1])+".jpg")
            iii=iii.resize((220,220),Image.ANTIALIAS)
            self.bgnaman=ImageTk.PhotoImage(iii)
            self.l10 = Label(self.f3, image = self.bgnaman,height=220,width=220)
            self.l10.image=self.bgnaman
            self.l10.place(x=100,y=200)
    def searchclick(self,root):
        self.lb.place(x=11265,y=85)
        dir='qrcode/'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir,f))
        number=self.e1.get()
        if number.isdigit():
            if checkpersondata(number):
                data=getdata(number)
                data=data[0]
                setqrode(changenamestate(data[1]),data[2],data[0],data[4],data[5],data[3])
                self.myclick(root,data)
            else:
                root.destroy()
                formrun()
        else:
            root.destroy()
            formrun()
    def delclick(self,root):
        number=self.e1.get()
        if checkpersondata(number):
            mycursor.execute("delete from user where registration_number="+number+";")
            mydb.commit()
            def deldone():
                r.destroy()
                root.destroy()
                searchpage()
            r = Tk()
            r.geometry('215x75')
            r.title("Warning.")
            r.iconbitmap('gui_images/hacker.ico')
            label_1 = Label(r, text="Deleted !",width=20,font=("bold", 10))
            label_1.place(x=10,y=10)
            Button(r, text='Okay.',width=10,bg='brown',fg='white', command=deldone).place(x=125,y=40)
            r.mainloop()
        else:
            def notexist():
                r.destroy()
                root.destroy()
                searchpage()
            r = Tk()
            r.geometry('215x75')
            r.title("Warning.")
            r.iconbitmap('gui_images/hacker.ico')
            label_1 = Label(r, text="User does not exist !",width=20,font=("bold", 10))
            label_1.place(x=10,y=10)
            Button(r, text='Okay.',width=10,bg='brown',fg='white', command=notexist).place(x=125,y=40)
            r.mainloop()
def searchpage():
    getnames()
    root = Tk()
    root.title("Printing_page") #Giving a title to ba
    root.iconbitmap('gui_images/hacker.ico')
    root.state("zoomed")
    mb=Printing_page(root)
    root.mainloop()
def facerecognizer():
    facetrain()
    face_cascade=cv2.CascadeClassifier('cascades\data\haarcascade_frontalface_alt2.xml')
    eye_cascade=cv2.CascadeClassifier('cascades\data\haarcascade_eye.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainner.yml")
    labels = {"person_name": 2}
    with open("labels.pickle",'rb') as f:
        og_labels=pickle.load(f)
        labels = {v:k for k,v in og_labels.items()}
    cap= cv2.VideoCapture(0,cv2.CAP_DSHOW)
    while(True):
        #capture frame by frame
        ret,frame=cap.read()
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(gray,scaleFactor=1.5,minNeighbors=5)
        #Axis for faces
        for (x,y,w,h) in faces:
            roi_gray=gray[y:y+h,x:x+w] #ycord-start, ycord-end
            roi_color=frame[y:y+h,x:x+w]
            #recognize? deep learned model predict keras tensorflow pytorch scikit learn
            id_,conf = recognizer.predict(roi_gray)
            if conf>=45:# and conf <=85:
                font=cv2.FONT_HERSHEY_SIMPLEX
                name=labels[id_]
                color=(255,255,255)
                stroke=2
                cv2.putText(frame,name,(x,y),font,1,color,stroke,cv2.LINE_AA)
            color=(255,0,0) #BGR 0-255
            stroke=2
            end_cord_x=x+w
            end_cord_y=y+h
            cv2.rectangle(frame,(x,y),(end_cord_x,end_cord_y),color,stroke)
            eyes=eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        font=cv2.FONT_HERSHEY_SIMPLEX
        now = datetime.now()
        start = now.strftime("%Y-%m-%d %I:%M:%S")
        cv2.putText(frame,"Enter q to exit",(10,70), font, 1,(255,255,255),2,cv2.LINE_AA)
        cv2.putText(frame,start,(10,30), font, 1,(255,255,255),2,cv2.LINE_AA)
        #display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(20)&0xFF==ord('q'):
            break
    # When everything is done , release the capture
    cap.release()
    cv2.destroyWindow('frame')
def facetrain():
    BASE_DIR=os.path.dirname(os.path.abspath(__file__))
    image_dir=os.path.join(BASE_DIR,"images")
    face_cascade=cv2.CascadeClassifier('cascades\data\haarcascade_frontalface_alt2.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    current_id=0
    label_ids={}
    x_train=[]
    y_labels=[]
    for root,dirs,files in os.walk(image_dir):
        for file in files:
            if file.endswith("png") or file.endswith("jpg"):
                path = os.path.join(root,file)
                label=os.path.basename(root).replace(" ",".").lower()
                if not label in label_ids:
                    label_ids[label]=current_id
                    current_id += 1
                id_=label_ids[label]
                pil_image=Image.open(path).convert("L")#grayscale
                size=(550,550)
                final_image = pil_image.resize(size, Image.ANTIALIAS)
                image_array=np.array(final_image,"uint8")
                faces=face_cascade.detectMultiScale(image_array,minNeighbors=5)
                for (x,y,w,h) in faces:
                    roi=image_array[y:y+h,x:x+w]
                    x_train.append(roi)
                    y_labels.append(id_)
    with open("labels.pickle",'wb') as f:
        pickle.dump(label_ids,f)
    recognizer.train(x_train,np.array(y_labels))
    recognizer.save("trainner.yml")
def scan(name,value):
    face_cascade=cv2.CascadeClassifier('cascades\data\haarcascade_frontalface_alt2.xml')
    eye_cascade=cv2.CascadeClassifier('cascades\data\haarcascade_eye.xml')
    cap= cv2.VideoCapture(0,cv2.CAP_DSHOW)
    loop2=0
    while loop2==0:
        #capture frame by frame
        ret,frame=cap.read()
        if(frame is not None):
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(gray,scaleFactor=1.5,minNeighbors=5)
        #Axis for faces
        for (x,y,w,h) in faces:
            roi_gray=gray[y:y+h,x:x+w] #ycord-start, ycord-end
            if(frame is not None):
                roi_color=frame[y:y+h,x:x+w]
            img_item='images/'+name+'/'+value+'.png'
            cv2.imwrite(img_item,roi_color)         
        loop1=0
        while loop1==0:
            #display the resulting frame
            try:
                cv2.imshow('frame',frame)
            except:
                loop1=1
                loop2=1
            try:
                f=open('images/'+name+'/'+value+'.png','r')
                f.close()
            except:
                pass
            else:
                cv2.waitKey(2000)
                cap.release()
                cv2.destroyWindow('frame')
            if cv2.waitKey(2):
                break
def changenamestate(name):
    name2=name.lower()
    passname=name2.replace(" ","-")
    return passname
def checkperson(name):
    try:
        f=open('person/'+name+'.txt','r')
    except:
        return False
    else:
        f.close()
        return True
def checkdata(name):
    try:
        f=open('qrcode/'+name+'.jpg','r')
    except:
        return False
    else:
        f.close()
        return True
def createperson(name):
    f=open('person/'+name+'.txt','w')
    f.close()
    os.mkdir('images/'+name)
def getnoofpictures(name):
    val=0
    while val!=-1:
        val=val+1
        value=str(val)
        try:
            f=open('images/'+name+'/'+value+'.png','r')
        except:
            return val
        else:
            f.close()
def setqrode(name,a,b,c,d,e):
    name=str(name)
    a=str(a)
    b=str(b)
    c=str(c)
    d=str(d)
    e=str(e)
    s ="College:"+ a +"\n"+ "Name:"+name+"\n"+"Registration number:"+b+"\n"+"Branch:"+c+"\n"+"Year:"+d+"\n"+"CGPA:"+e+"\n"
    url = pyqrcode.create(s)
    url.png('qrcode/'+name+'.jpg', scale = 6)
def getqrode(name):
    result = decode(Image.open('qrcode/'+name+'.jpg'))
    a=[]
    for i in result:
        a.append(i.data.decode("utf-8"))
    data=(a[0])
    college_val=data.find("Name")-1
    college=data[8:college_val]
    name_val=data.find("Registration number")-1
    name=data[college_val+6:name_val]
    regno_val=data.find("Branch")-1
    regno=data[name_val+21:regno_val]
    branch_val=data.find("Year")-1
    branch=data[regno_val+8:branch_val]
    year_val=data.find("CGPA")-1
    year=data[branch_val+6:year_val]
    cgpa=data[year_val+6:len(data)-1]
def smallwindow():
	def display():
		n=entry_1.get()
		r.destroy()
		name=changenamestate(n)
		if checkperson(name):
			pass
		else:
			createperson(name)
		if getnoofpictures(name)<=10:
			while getnoofpictures(name)<=10:
				val=getnoofpictures(name)
				value=str(val)
				scan(name,value)
		else:
			val=getnoofpictures(name)
			value=str(val)
			scan(name,value)
		facetrain()
	r = Tk()
	r.geometry('215x75')
	r.title("Scan.")
	r.iconbitmap('gui_images/hacker.ico')
	label_1 = Label(r, text="Full Name:",width=20,font=("bold", 10))
	label_1.place(x=-45,y=10)
	entry_1 = Entry(r)
	entry_1.place(x=80,y=10)
	Button(r, text='Submit',width=10,bg='brown',fg='white', command=display).place(x=125,y=40)
	r.mainloop()
class secondpage:
    def __init__ (self,root):
        self.bg1=ImageTk.PhotoImage(file='gui_images/black_bg.png')
        self.my_canvas=Canvas(root,height=1400, width=1020)
        self.my_canvas.pack(fill = "both",expand=True)
        self.my_canvas.create_image(0,0, image=self.bg1,anchor="nw")
        self.my_canvas.create_text(650,95, text = "Face Recognition",font=("Times",55),fill='white')
        def change(e):
            self.bg5 = ImageTk.PhotoImage(file="gui_images/scan_big.png")
            self.b1.config(image = self.bg5)
            self.b1.image = self.bg5
        def change_1(e):	
            self.bg6 = ImageTk.PhotoImage(file="gui_images/recognize_big.png")
            self.b2.config(image = self.bg6)
            self.b2.image = self.bg6
        def change_2(e):	
            self.bg7 = ImageTk.PhotoImage(file="gui_images/info_big.png")
            self.b3.config(image = self.bg7)
            self.b3.image = self.bg7
        def change_back(e):
            self.bg5 = ImageTk.PhotoImage(file="gui_images/scan.png")
            self.b1.config(image = self.bg5)
            self.b1.image = self.bg5
        def change_back_1(e):	
            self.bg6 = ImageTk.PhotoImage(file="gui_images/recognize.png")
            self.b2.config(image = self.bg6)
            self.b2.image = self.bg6
        def change_back_2(e):	 
            self.bg7 = ImageTk.PhotoImage(file="gui_images/info.png")
            self.b3.config(image = self.bg7)
            self.b3.image = self.bg7
        self.bg2 = ImageTk.PhotoImage(file='gui_images/scan.png')
        self.bg3 = ImageTk.PhotoImage(file='gui_images/recognize.png')
        self.bg4 = ImageTk.PhotoImage(file='gui_images/info.png')
        self.my_canvas.create_text(175,500,text="SCAN",fill = "white" ,font=("Times",20,"bold"))
        self.my_canvas.create_text(645,500, text="RECOGNISE" ,fill = "white" ,font=("Times",20,"bold"))
        self.my_canvas.create_text(1115,500, text="INFORMATION",fill = "white" ,font=("Times",20,"bold"))
        self.b1 = Button(root, image = self.bg2, command=smallwindow)#scan
        self.b2 = Button(root,  image = self.bg3, command=facerecognizer)#recognize
        def func11():
            root.destroy()
        def func22():
            searchpage()
        self.b3 = Button(root, image = self.bg4,command=lambda: [func11(),func22()])#info
        self.b4 = Button(root, text="EXIT" ,font=("Times",15,"bold"),command=root.destroy)
        self.b1.configure(width=170,height=170,background = "black",activebackground = "#e60e5d",borderwidth=0)
        b1_window = self.my_canvas.create_window(93,250,anchor="nw",window=self.b1)
        self.b2.configure(width=170,height=170,background = "black",activebackground = "#e60e5d",borderwidth=0)
        b2_window = self.my_canvas.create_window(560,250,anchor="nw",window=self.b2)
        self.b3.configure(width=170,height=170,background = "black",activebackground = "#e60e5d",borderwidth=0)
        b3_window = self.my_canvas.create_window(1026,250,anchor="nw",window=self.b3)
        self.b4.configure(width=15,height=1,background = "#fff",activebackground = "#000",borderwidth=5)
        b4_window = self.my_canvas.create_window(1080,5,anchor="nw",window=self.b4)
	#creating an object to class
        self.b1.bind("<Enter>",change)
        self.b1.bind("<Leave>",change_back)
        self.b2.bind("<Enter>",change_1)
        self.b2.bind("<Leave>",change_back_1)
        self.b3.bind("<Enter>",change_2)
        self.b3.bind("<Leave>",change_back_2)
def page_2_run():
	root=Tk()#create root window
	root.title("Frame Tkinter Application") #Giving a title to ba
	root.iconbitmap('gui_images/hacker.ico')
	root.state("zoomed")
	mb=secondpage(root)
	root.mainloop()
class firstpage:
	def __init__ (self,root):
		self.bg5 = ImageTk.PhotoImage(file='gui_images/black_bg.png')
		self.my_canvas1=Canvas(root,height=1400, width=1020)
		self.my_canvas1.pack(fill = "both",expand=True)
		self.my_canvas1.create_image(0,0, image=self.bg5,anchor="nw")
		self.my_canvas1.create_text(120,45, text = "About",font=("Times","56"),fill='white')
		self.my_canvas1.create_text(30,105,text = """Facial recognition is a way of identifying or confirming an individual’s identity using their face. Facial recognition 
\nsystems can be used to identify people in photos, videos, or inreal-time . Facial recognition is a category of biometric 
\nsecurity. Other forms of biometric software include voice recognition, fingerprint recognition, and eye retina or iris 
\nrecognition. The technology is mostly used for security and law enforcement, though there is increasing interest in other 
\nareas of use. 
\n\nMany people are familiar with face recognition technology through the FaceID used to unlock iPhones (however, 
\nthis is only one application of face recognition). Typically, facial recognition does not rely on a massive database of 
\nphotos to determine an individual’s identity — it simply identifies and recognizes one person as the sole owner of the 
\ndevice, while limiting access to others. Beyond unlocking phones, facial recognition works by matching the faces 
\nof people walking past special cameras, to images of people on a watch list. The watch lists can contain pictures of 
\nanyone, including people who are not suspected of any wrong doing, and the images can come from anywhere — even 
\nfrom our social media accounts.
		""",fill='white',font=("Times","14","bold"),anchor="nw")
		def func1():
			root.destroy()
		def func2():
			page_2_run()
		self.b5 = Button(root, text="NEXT" ,fg = "black",font=("Times","14","bold"),command=lambda: [func1(), func2()])
		self.b5.configure(width=13,height=1,background = "#fff",activebackground = "#000",borderwidth=7)
		b5_window = self.my_canvas1.create_window(1050,580,anchor="nw",window=self.b5)
def page_1_run():
	root=Tk()#create root window
	root.title("Face Recognizer") #Giving a title to ba
	root.iconbitmap('gui_images/hacker.ico')
	root.state("zoomed")
	mb=firstpage(root)
	root.mainloop()
page_1_run()
dir='qrcode/'
for f in os.listdir(dir):
    os.remove(os.path.join(dir,f))