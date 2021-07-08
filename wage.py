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
window.title("IntelliSense")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'
#answer = messagebox.askquestion(dialog_title, dialog_text)
 
width, height = window.winfo_screenwidth()/2, window.winfo_screenheight()*2/3
window.geometry('%dx%d+0+0' % (width,height))
window.configure(background='light steel blue')

message = tk.Label(window, text="Face Recognition Based Attendance System" ,bg="slate blue"  ,fg="black"  ,width=int(window.winfo_screenwidth()/2)  ,height=4,font=('algerian', 20, 'bold')).pack()

lbl = tk.Label(window, text="Unskilled",width=15  ,height=2  ,fg="black"  ,bg="slate blue" ,font=('algerian', 15, ' bold ') ) 
lbl.place(x=50, y=150)

txt = tk.Entry(window,width=25  ,bg="white" ,fg="black", font=('times', 15, ' bold '))
txt.place(x=280, y=150, height=50)

lbl2 = tk.Label(window, text="Semi-Skilled",width=15  ,fg="black"  ,bg="slate blue"    ,height=2 ,font=('algerian', 15, ' bold ')) 
lbl2.place(x=50, y=230)

txt2 = tk.Entry(window,width=25  ,bg="white"  ,fg="black", font=('times', 15, ' bold ')  )
txt2.place(x=280, y=230, height=50)

lbl3 = tk.Label(window, text="Skilled",width=15  ,height=2  ,fg="black"  ,bg="slate blue" ,font=('algerian', 15, ' bold ') ) 
lbl3.place(x=50, y=310)

txt3 = tk.Entry(window,width=25  ,bg="white" ,fg="black", font=('times', 15, ' bold '))
txt3.place(x=280, y=310, height=50)

lbl4 = tk.Label(window, text="Highly Skilled",width=15  ,fg="black"  ,bg="slate blue"    ,height=2 ,font=('algerian', 15, ' bold ')) 
lbl4.place(x=50, y=390)

txt4 = tk.Entry(window,width=25 ,bg="white"  ,fg="black", font=('times', 15, ' bold ')  )
txt4.place(x=280, y=390, height=50)

lbl5 = tk.Label(window, text="Notification : ",width=20  ,fg="black"  ,bg="slate blue"  ,height=2 ,font=('algerian', 15, ' bold underline ')) 
lbl5.place(x=50, y=470)

message = tk.Label(window, text="" ,bg="white"  ,fg="black"  ,width=30  ,height=2, activebackground = "yellow" ,font=('times', 15, ' bold ')) 
message.place(x=350, y=470)

def clear():
    txt.delete(0, 'end')    
    res = ""
    txt2.delete(0, 'end')    
    res = ""
    txt3.delete(0, 'end')    
    res = ""
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

def TakeData():        
    s1=(txt.get())
    s2=(txt2.get())
    s3=(txt3.get())
    s4=(txt4.get())
    if(is_number(s1) and is_number(s2) and is_number(s3) and is_number(s4)):
        ts = time.time()      
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        res = "Details Saved Successfully"
        '''
        row = [s1 , s2, s3, s4, date]
        with open('EmployeeDetails\WageDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
        '''
        role = []
        wage = []
        role = ['Unskilled','SemiSkilled','Skilled','HighlySkilled']
        wage = [s1,s2,s3,s4]
        with open('EmployeeDetails\WageDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            row = [role[0], wage[0], date]
            writer.writerow(row)
            row = [role[1], wage[1], date]
            writer.writerow(row)
            row = [role[2], wage[2], date]
            writer.writerow(row)
            row = [role[3], wage[3], date]
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        res = "Enter Numeric value only "
        message.configure(text= res)

# OptionMenu Button
'''
options = tk.StringVar(window)
options.trace_add('write', lambda *args: print(options.get()))
options.set("Per Day") # default value

om1 =tk.OptionMenu(window, options, "Per Day","Per Hr")
om1["bg"] = "IndianRed1"
om1["highlightthickness"]=0 
om1.config(width=9, height=1, font=('times', 15, ' bold '))
om1['menu'].config(font=('times',(15), ' bold '),bg='IndianRed1')
om1.place(x=587, y=155)
'''

perButton = tk.Button(window, text="Per Day",fg="black"  ,bg="yellow green"  ,width=10  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
perButton.place(x=587, y=155) 
clearButton = tk.Button(window, text="Clear All", command=clear  ,fg="black"  ,bg="IndianRed1"  ,width=10  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton.place(x=587, y=235)  
trackData = tk.Button(window, text="Save All", command=TakeData , fg="black"  ,bg="IndianRed1"  ,width=10  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
trackData.place(x=587, y=315)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="black"  ,bg="dark turquoise"  ,width=10  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=587, y=395)
 
window.mainloop()