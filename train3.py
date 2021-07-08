import tkinter as tk
from tkinter import Message ,Text
from cv2 import cv2
import os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font

window = tk.Tk()
#helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
window.title("IntelliSense")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'
#answer = messagebox.askquestion(dialog_title, dialog_text)
 
width, height = window.winfo_screenwidth()/2, window.winfo_screenheight()*2/3
window.geometry('%dx%d+0+0' % (width,height))
window.configure(background='light steel blue')

message = tk.Label(window, text="Face Recognition Based Attendance System" ,bg="slate blue"  ,fg="black"  ,width=int(window.winfo_screenwidth()/2)  ,height=4,font=('algerian', 20, 'bold')).pack()

lbl = tk.Label(window, text="Enter ID",width=12  ,height=2  ,fg="black"  ,bg="slate blue" ,font=('algerian', 15, ' bold ') ) 
lbl.place(x=50, y=150)

txt = tk.Entry(window,width=30  ,bg="white" ,fg="black", font=('times', 15, ' bold '))
txt.place(x=250, y=150, height=50)

lbl2 = tk.Label(window, text="Enter Name",width=12  ,fg="black"  ,bg="slate blue"    ,height=2 ,font=('algerian', 15, ' bold ')) 
lbl2.place(x=50, y=230)

txt2 = tk.Entry(window,width=30  ,bg="white"  ,fg="black", font=('times', 15, ' bold ')  )
txt2.place(x=250, y=230, height=50)

lbl4 = tk.Label(window, text="Enter Role",width=12  ,fg="black"  ,bg="slate blue"    ,height=2 ,font=('algerian', 15, ' bold ')) 
lbl4.place(x=50, y=310)

txt4 = tk.Entry(window,width=30  ,bg="white"  ,fg="black", font=('times', 15, ' bold ')  )
txt4.place(x=250, y=310, height=50)

lbl3 = tk.Label(window, text="Notification : ",width=20  ,fg="black"  ,bg="slate blue"  ,height=2 ,font=('algerian', 15, ' bold underline ')) 
lbl3.place(x=50, y=390)

message = tk.Label(window, text="" ,bg="white"  ,fg="black"  ,width=30  ,height=2, activebackground = "yellow" ,font=('times', 15, ' bold ')) 
message.place(x=350, y=390)
 
def clear():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')    
    res = ""
    message.configure(text= res)    

def clear3():
    txt4.delete(0, 'end')    
    res = ""
    message.configure(text= res)   
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
 
def TakeImages():        
    Id=(txt.get())
    name=(txt2.get())
    role=(txt4.get())
    if(is_number(Id) and name.isalpha() and role.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                #incrementing sample number 
                sampleNum=sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
                cv2.imshow('frame',img)
            #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum>60:
                break
        ts = time.time()      
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id , name, role, date]
        with open('EmployeeDetails\EmployeeDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        if(is_number(name)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(Id.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text= res)
        if(is_number(role)):
            res = "Enter Alphabetical Role"
            message.configure(text= res)
    
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Image Trained"#+",".join(str(f) for f in Id)
    message.configure(text= res)

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #print(imagePaths)
    #create empth face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids
  
clearButton = tk.Button(window, text="Clear", command=clear  ,fg="black"  ,bg="IndianRed1"  ,width=10  ,height=1 ,activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton.place(x=587, y=155)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="black"  ,bg="IndianRed1"  ,width=10  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton2.place(x=587, y=235)
clearButton3 = tk.Button(window, text="Clear", command=clear3  ,fg="black"  ,bg="IndianRed1"  ,width=10  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton3.place(x=587, y=315)    
takeImg = tk.Button(window, text="Take", command=TakeImages  ,fg="black"  ,bg="DarkGoldenrod1"  ,width=15  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
takeImg.place(x=50, y=470)
trainImg = tk.Button(window, text="Train", command=TrainImages  ,fg="black"  ,bg="yellow green"  ,width=15  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
trainImg.place(x=288, y=470)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="black"  ,bg="dark turquoise"  ,width=15  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=525, y=470)
 
window.mainloop()