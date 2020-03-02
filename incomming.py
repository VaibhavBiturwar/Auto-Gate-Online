from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql
from datetime import datetime
from datetime import date
import cv2
# import pytesseract
import re
import imutils
import numpy as np
import requests
from firebase import firebase
firebase = firebase.FirebaseApplication("https://fastgate-d2d06.firebaseio.com/",None)

frame = []
uid = ""

def search():
    global uid
    oname = t2.get()
    mobile  = t3.get()
    block = t4.get()
    flat = t5.get()

    try:
        if block != "":
             block = block.upper()

        if block !="" and flat == ""  or block =="" and flat != "" :
            messagebox.showinfo(title="Invalid Entry", message="Please Enter Block and flat No Together")

        query = "SELECT * FROM entry WHERE owner_name LIKE '"+oname +"' OR mob LIKE '"+mobile+"'  OR block  LIKE '"+block+"' AND flat_no LIKE '"+flat+"'"
        print(query)

        conn = pymysql.connect(host="127.0.0.1", user="root", passwd='', db='license')
        mycursor = conn.cursor()
        mycursor.execute(query)
        records = mycursor.fetchone()

        if mycursor.rowcount == 0:
            messagebox.showinfo(title="Invalid Entry", message="No Match Found")
            t2.delete(0, END)
            t3.delete(0, END)
            t4.delete(0, END)
            t5.delete(0, END)
            t6.delete(0, END)
            t7.delete(0, END)

        elif mycursor.rowcount > 1:
            messagebox.showinfo(title="Invalid Entry", message="Too many Entries!! Try something else")
            t2.delete(0,END)
            t3.delete(0,END)
            t4.delete(0,END)
            t5.delete(0,END)
            t6.delete(0,END)
            t7.delete(0,END)
        else:
            uid = records[1]
            t2.delete(0,END)
            t2.insert(0 , records[2])
            t3.delete(0,END)
            t3.insert(0 , records[3])
            t4.delete(0,END)
            t4.insert(0 , records[4])
            t5.delete(0,END)
            t5.insert(0 , records[5])

            t6.delete(0,END)
            t6.insert(0 , date.today())

            t7.delete(0,END)
            t7.insert(0 ,datetime.now().strftime("%H:%M:%S"))

    except Exception as e:
        print(e)

def capture():
    global frame
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

    image = imutils.resize(frame, width=500)

    # cv2.imshow("Original Image", image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("1 - Grayscale Conversion", gray)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    # cv2.imshow("2 - Bilateral Filter", gray)
    edged = cv2.Canny(gray, 170, 200)
    # cv2.imshow("4 - Canny Edges", edged)

    find = False
    try:
        (new, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
        NumberPlateCnt = None
        count = 0
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                NumberPlateCnt = approx
                break

        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [NumberPlateCnt], 0, 255, -1)
        new_image = cv2.bitwise_and(image, image, mask=mask)
        find = True
        cv2.namedWindow("Final_image", cv2.WINDOW_NORMAL)
        cv2.imshow("Final_image", new_image)
        cv2.waitKey(0)
    except Exception as e:
        print(e)

    if find:
        config = ('-l eng --oem 1 --psm 3')
        str = pytesseract.image_to_string(new_image)
        print(str)
        regex = re.compile('[^a-zA-Z0-9\s]')
        regex = regex.sub('', str)
        print(regex)
        t1.delete(0,END)
        t1.insert(0,regex)

def save():
    global uid

    vehicle = t1.get()
    oname = t2.get()
    mob = t3.get()
    block = t4.get().upper()
    flat = t5.get()
    date = t6.get()
    time = t7.get()
    ty = type.get()
    print(ty)

    data = {
        'vehicle': vehicle,
        'date': date,
        'time': time,
        'type': ty
    }




    try:
        code = firebase.post('USER/'+uid, data)
        code = code['name']

        conn = pymysql.connect(host="127.0.0.1", user="root", passwd='', db='license')
        mycursor = conn.cursor()
        url = "INSERT INTO incomming (owner_name,block,flat_no,v_no,dt,tm,type) VALUES('"+oname+"','"+block+"','"+flat+"','"+vehicle+"','"+date+"','"+time+"','"+ty+"')"
        print(url)
        mycursor.execute(url)
        conn.commit()
        print("Successful")
        msg(vehicle,mob,date,time,ty)
    except Exception as e:
        messagebox.showinfo(title="Error", message="Try Again")
        print(e)
    finally:
        conn.close()

def msg(v,m,d,t,ty):
    url = "https://www.fast2sms.com/dev/bulk"
    msg = "\nVehicle No: "+v+"\nDate: "+d+"\nTime: "+t+"\n"+ty
    querystring = {"authorization": "my8icw0ebfonXukEPQYIjG1qLTSKMNWdBhJr3V72CvgFZ6aUslCl42JqOKsaUoWN7IruchnPfimzeFRG",
                   "sender_id": "FSTSMS", "message": msg, "language": "english", "route": "p", "numbers": m}
    headers = {'cache-control': "no-cache"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)

def exit():
    window.destroy()



window = Tk()
window.title("Incomming Vehicle")
Label(window , text = "Incomming Vehicle" , font=("Fantasy ",30), bg="White" ,fg="Black").grid(row = 0 , column = 0 , columnspan=2)

Label(window , text = "Vehicle Number" , font=("monospaced ",15), bg="White" ,fg="Black").grid(row=1 ,column=0)
t1 = Entry(window , width=15 ,font=("Arial Bold" , 20) )
t1.grid(row=1 , column= 1)

Label(window , text = "Owner Name" , font=("monospaced ",15), bg="White" ,fg="Black").grid(row=2 ,column=0)
t2 = Entry(window , width=15 ,font=("Arial Bold" , 20) )
t2.grid(row=2 , column= 1)

Label(window , text = "Mobile" , font=("monospaced ",15), bg="White" ,fg="Black").grid(row=3 ,column=0)
t3 = Entry(window , width=15 ,font=("Arial Bold" , 20) )
t3.grid(row=3 , column= 1)

Label(window , text = "Block" , font=("monospaced ",15), bg="White" ,fg="Black").grid(row=4 ,column=0)
t4 = Entry(window , width=15 ,font=("Arial Bold" , 20) )
t4.grid(row=4 , column= 1)

Label(window , text = "Flat_no" , font=("monospaced ",15), bg="White" ,fg="Black").grid(row=5 ,column=0)
t5 = Entry(window , width=15 ,font=("Arial Bold" , 20) )
t5.grid(row=5 , column= 1)

Label(window , text = "Date" , font=("monospaced ",15), bg="White" ,fg="Black").grid(row=6 ,column=0)
t6 = Entry(window , width=15 ,font=("Arial Bold" , 20) )
t6.grid(row=6 , column= 1)

Label(window , text = "In Time" , font=("monospaced ",15), bg="White" ,fg="Black").grid(row=7 ,column=0)
t7 = Entry(window , width=15 ,font=("Arial Bold" , 20) )
t7.grid(row=7 , column= 1)

Label(window , text = "Entry  Type" , font=("monospaced ",15), bg="White" ,fg="Black").grid(row=8 ,column=0)
type = ttk.Combobox(window , font=("monospaced" , 20))
type["values"] = ("Visitor" , "Zomato" , "Swiggy" , "Uber" , "Ola" , "Other")
type.current(0)
type.grid(row=8 , column= 1)

b1 =Button(window , text="Search" , font=("monospaced" , 15) , command = search).grid(row=2, column=2 )
b2 =Button(window , text="Save" , font=("monospaced" , 20) , command = save).grid(row=9, column=0 , columnspan = 2 )
ex =Button(window , text="Exit" , font=("monospaced" , 20) , command = exit).grid(row=10, column=0 , columnspan = 2 )

# capture =Button(window , text="Capture" , font=("monospaced" , 15) , command = capture).grid(row=1, column=2)

window.geometry("700x500")
window.mainloop()



