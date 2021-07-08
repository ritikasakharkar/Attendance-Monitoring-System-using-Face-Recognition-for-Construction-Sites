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
#window.iconbitmap('yt.ico')
window.configure(background='light steel blue')

#window.attributes('-fullscreen', True)

#window.grid_rowconfigure(0, weight=1)
#window.grid_columnconfigure(0, weight=1)

message = tk.Label(window, text="Face Recognition Based Attendance System" ,bg="slate blue"  ,fg="black"  ,width=int(window.winfo_screenwidth()/2)  ,height=4,font=('algerian', 20, 'bold')).pack()

#message.place(x=120, y=20)


lbl3 = tk.Label(window, text="Remark : ", width=20, fg="black",bg="slate blue", height=3, font=('times', 15, 'bold')) 
lbl3.place(x=50, y=330)


message2 = tk.Label(window, text="", fg="black", bg="white", activeforeground = "green", width=30, height=3, font=('times', 15, ' bold ')) 
message2.place(x=350, y=330)
    
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

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);    
    df=pd.read_csv("EmployeeDetails\EmployeeDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names)    
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)    
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
            if(conf < 50):
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                
            else:
                Id='Unknown'                
                tt=str(Id)  
            if(conf > 75):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
        cv2.imshow('im',im) 
        if (cv2.waitKey(1)==ord('q')):
            break
    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    #Hour,Minute,Second=timeStamp.split(":")
    df_list = attendance.values.tolist()
    Id , name, date, timeStamp = df_list[0][0], df_list[0][1], df_list[0][2], df_list[0][3]
    row = [Id , name, date, timeStamp]
    with open('Attendance\Attendance_Tracker.csv','a+') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()
    #fileName="Attendance\Attendance_Tracker.csv"
    #attendance.to_csv(fileName,index=False)
    cam.release()
    cv2.destroyAllWindows()
    #print(attendance)
    res=attendance
    message2.configure(text= res)

def GenerateDWL():
    df1=pd.read_csv("EmployeeDetails\EmployeeDetails.csv")
    df2=pd.read_csv("Attendance\Attendance_Tracker.csv")
    df3=pd.read_csv("EmployeeDetails\WageDetails.csv")
    dfa = df2[['Id', 'Name','Date']]
    dfa = dfa.merge(df1, on="Id", how = 'left')
    dfa = dfa.merge(df3, on="Role", how = 'left')
    dfa = dfa.drop(['Name_x','Joining_Date','Date_y','Unnamed: 3','Unnamed: 4'], axis=1)
    dfa = dfa.drop_duplicates(subset = ['Id'],ignore_index = True)
    print(dfa)

    df_list = dfa.values.tolist()

    for i in range(len(dfa)):
        Id, Date, Name, Role, Wage = df_list[i][0], df_list[i][1], df_list[i][2], df_list[i][3], df_list[i][4]
        row = [Id, Name, Role, Date, Wage]
        with open('Attendance\DWL_Report.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()

trackImg = tk.Button(window, text="Attendance", command=TrackImages  ,fg="black"  ,bg="yellow green"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
trackImg.place(x=100, y=200)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="black"  ,bg="dark turquoise"  ,width=20  ,height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=400, y=200)
DWLWindow = tk.Button(window, text="Generate DWL Report" , command=GenerateDWL , fg="black"  ,bg="IndianRed1"  ,width=55  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
DWLWindow.place(x=46, y=450)
 
window.mainloop()