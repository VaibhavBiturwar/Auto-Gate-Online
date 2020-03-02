from tkinter import *
from tkinter import messagebox
import pymysql
from firebase import firebase
firebase = firebase.FirebaseApplication("https://fastgate-d2d06.firebaseio.com/",None)

def exit():
    window.destroy()


def click():
    oname   = t1.get()
    mob     = t2.get()
    block   = t3.get()
    block = block.upper()
    flat_no = t4.get()
    uid = t5.get()

    data = {
        'owner_name' : oname,
        'mob' : mob,
        'block' : block,
        'flat_no' : flat_no,
        'uid' : uid
    }

    try:

        code = firebase.put('USER/'+uid,'info', data)
        # code = code['name']
        int(flat_no)
        int(mob)
        print(oname, mob, block, flat_no)
        conn = pymysql.connect(host="127.0.0.1", user="root", passwd='', db='license')
        mycursor = conn.cursor()
        url = "INSERT INTO entry (code,owner_name, mob, block, flat_no) VALUES('"+uid+"','"+oname+"','"+mob+"','"+block+"','"+flat_no+"')"
        mycursor.execute(url)
        conn.commit()
        print("Successful")
        t1.delete(0,END)
        t2.delete(0,END)
        t3.delete(0,END)
        t4.delete(0,END)
        t5.delete(0,END)
    except Exception as e:
        messagebox.showinfo(title="Invalid Entry", message="Invalid Mobile no. or Flat no.")
        print("Invalid Mobile no. or Flat no.")
        print(e)
    finally:
        conn.close()


window = Tk()
window.title("Entry Page")
Label(window , text = "Entry Page" , font=("Fantasy ",30), bg="White" ,fg="Black").grid(row = 0 , column = 0 , columnspan=2)


Label(window , text = "Owner Name" , font=("monospaced ",15), bg="White" ,fg="Black").grid(row=1 ,column=0)
t1 = Entry(window , width=15 ,font=("Arial Bold" , 20) )
t1.grid(row=1 , column= 1)

Label(window , text = "Mobile" , font=("monospaced ",15), bg="White" ,fg="Black").grid(row=2 ,column=0)
t2 = Entry(window , width=15 ,font=("Arial Bold" , 20) )
t2.grid(row=2 , column= 1)

Label(window , text = "Block" , font=("monospaced ",15), bg="White" ,fg="Black").grid(row=3 ,column=0)
t3 = Entry(window , width=15 ,font=("Arial Bold" , 20) )
t3.grid(row=3 , column= 1)

Label(window , text = "Flat No" , font=("monospaced ",15), bg="White" ,fg="Black").grid(row=4 ,column=0)
t4 = Entry(window , width=15 ,font=("Arial Bold" , 20) )
t4.grid(row=4 , column= 1)

Label(window , text = "User ID" , font=("monospaced ",15), bg="White" ,fg="Black").grid(row=5 ,column=0)
t5 = Entry(window , width=20 ,font=("Arial Bold" , 20) )
t5.grid(row=5 , column= 1)


b1 =Button(window , text="Save" , font=("monospaced" , 20) , command = click).grid(row=6, column=0 , columnspan=2)

ext =Button(window , text="Exit" , font=("monospaced" , 20) , command = exit).grid(row=7, column=0 , columnspan=2)




window.geometry("700x500")
window.mainloop()


