from tkinter import *
from PIL import ImageTk
from  tkinter import messagebox
import sign
import utils
from client_gui import Client


def login_user():
    if usernameEntry.get()=='' or pwdEntry.get()=='':
        messagebox.showerror('Error','All fields Are required')

    else:
        if sign.signIn(usernameEntry.get(), pwdEntry.get()) == None:
            messagebox.showerror('Error', 'Invalid username or password')
        else:
            # if utils.verifyCert('build/client.pem'):
            client = Client("192.168.1.7", 8080, usernameEntry.get())
            root.destroy()
            messagebox.showinfo('Welcome', 'login is successful')


            # else:
            # messagebox.showerror('Error', 'Invalid certificate')

def signup_page():
    root.destroy()
    import register

def username_enter(event):
    if usernameEntry.get()=='Username':
        usernameEntry.delete(0,END)

def pwd_enter(event):
    if usernameEntry.get()=='Password':
        usernameEntry.delete(0,END)

def hide():
    openeye.config(file='assets/closeye.png')
    pwdEntry.config(show='*')
    eyeButton.config(command=show)

def show():
    openeye.config(file='assets/openeye.png')
    pwdEntry.config(show='')
    eyeButton.config(command=hide)



root=Tk()
root.geometry('990x660+50+50')
root.resizable(0,0)
root.title('Login Page')
bgImage=ImageTk.PhotoImage(file='assets/bg.jpg')
bgLabel=Label(root,image=bgImage)
bgLabel.place(x=0,y=0)


heading=Label(root,text='SIGN IN',font=('Microsoft Yahei UI Light',23,'bold'),bg='white',fg='firebrick1')
heading.place(x=630,y=120)

usernameEntry=Entry(root,width=25,font=('Microsoft Yahei UI Light',11,'bold'),bd=0,fg='firebrick1')
usernameEntry.place(x=580,y=200)
usernameEntry.insert(0,'Username')

usernameEntry.bind('<FocusIn>',username_enter)


frame1=Frame(root,width=250,height=2)
frame1.place(x=580,y=222)


pwdEntry=Entry(root,width=25,font=('Microsoft Yahei UI Light',11,'bold'),bd=0,fg='firebrick1')
pwdEntry.place(x=580,y=260)
pwdEntry.insert(0,'Password')

pwdEntry.bind('<FocusIn>',pwd_enter)

frame2=Frame(root,width=250,height=2)
frame2.place(x=580,y=282)

openeye=PhotoImage(file='assets/openeye.png')
eyeButton=Button(root,image=openeye,bd=0,bg='white',activebackground='white',cursor='hand2'
                 ,command=hide)
eyeButton.place(x=800,y=255)

loginButton=Button(root,text='Sign In',font=('Open Sans',16,'bold'),
                   fg='white',bg='firebrick1',activeforeground='white',activebackground='firebrick1',cursor='hand2',bd=0,width=19,command=login_user)
loginButton.place(x=578,y=350)

signupLabel=Label(root,text='Dont have an account ?',font=('Open Sans',9,'bold'),fg='firebrick1',bg='white')
signupLabel.place(x=590,y=500)

newaccountButton=Button(root,text='Sign up',font=('Open Sans',9,'bold underline'),
                        fg='firebrick1',bg='white',activeforeground='blue'
                        ,activebackground='white',cursor='hand2',bd=0,command=signup_page)
newaccountButton.place(x=727,y=500)


root.mainloop()
