from tkinter import *
from PIL import ImageTk
from  tkinter import messagebox
import sign

def clear():
    emailEntry.delete(0,END)
    usernameEntry.delete(0,END)
    pwdEntry.delete(0, END)
    pwd2Entry.delete(0, END)



def connect_db():
    if emailEntry.get()=='' or usernameEntry.get()=='' or pwdEntry.get()=='' or pwd2Entry.get()=='':
        messagebox.showerror('Error','All fields Are required')
    elif pwdEntry.get()!= pwd2Entry.get():
        messagebox.showerror('Error','passwords mismatch')
    else:
        # user = {
        #     'username': usernameEntry.get(),
        #     'password': wdEntry.get(),
        #     'email': emailEntry.get(),  # student card
        # }

        # # Register user with LDAP Service
        # ldapserver.register(user)
        # utils.createCertRequest(usernameEntry.get(),'TN','Tunis', 'insat', usernameEntry.get(), emailEntry.get(),'build/client.pem','build/client')
        # utils.createCert('build/client.pem')
        sign.signUp(usernameEntry.get(),emailEntry.get(),pwdEntry.get())
        messagebox.showinfo('Success','Registration is successful')

        clear()
        signIn_pege()



def signIn_pege():
    sinup_window.destroy()
    import signIn


sinup_window=Tk()
sinup_window.title('SignUp Page')
sinup_window.resizable(False,False)
background=ImageTk.PhotoImage(file='assets/background.jpg')


bgLabel=Label(sinup_window,image=background)
bgLabel.grid()

frame = Frame(sinup_window,bg='white')
frame.place(x=454, y=50)

heading=Label(frame,text='REGISTER TO INSAT CHAT',font=('Microsoft Yahei UI Light',15,'bold'),bg='white',fg='firebrick1')
heading.grid(row=0,column=0,padx=10,pady=10)


emailLabel=Label(frame,text='Email',font=('Microsoft Yahei UI Light',10,'bold')
                 ,bg='white',fg='firebrick1')
emailLabel.grid(row=1,column=0,sticky='w',padx=25,pady=(10,0) )


emailEntry=Entry(frame,width=25,font=('Microsoft Yahei UI Light',10,'bold'),fg='firebrick1')
emailEntry.grid(row=2,column=0,sticky='w',padx=25)



usernameLabel=Label(frame,text='Username',font=('Microsoft Yahei UI Light',10,'bold')
                 ,bg='white',fg='firebrick1')
usernameLabel.grid(row=3,column=0,sticky='w',padx=25,pady=(10,0))

usernameEntry=Entry(frame,width=25,font=('Microsoft Yahei UI Light',10,'bold'),fg='firebrick1')
usernameEntry.grid(row=4,column=0,sticky='w',padx=25)


pwdLabel=Label(frame,text='Password',font=('Microsoft Yahei UI Light',10,'bold')
                 ,bg='white',fg='firebrick1')
pwdLabel.grid(row=5,column=0,sticky='w',padx=25,pady=(10,0) )


pwdEntry=Entry(frame,width=25,font=('Microsoft Yahei UI Light',10,'bold'),fg='firebrick1')
pwdEntry.grid(row=6,column=0,sticky='w',padx=25)


pwd2Label=Label(frame,text='Confirm Password',font=('Microsoft Yahei UI Light',10,'bold')
                 ,bg='white',fg='firebrick1')
pwd2Label.grid(row=7,column=0,sticky='w',padx=25,pady=(10,0) )


pwd2Entry=Entry(frame,width=25,font=('Microsoft Yahei UI Light',10,'bold'),fg='firebrick1')
pwd2Entry.grid(row=8,column=0,sticky='w',padx=25)


signupButton=Button(frame,text='Signup',font=('Open Sans',16,'bold'),bd=0,bg='firebrick1',fg='white'
                    ,activebackground='firebrick1',activeforeground='white',width=17,command=connect_db)
signupButton.grid(row=9,column=0,pady=25)


alreadyaccount=Label(frame,text='Already have an account ?',font=('Open Sans',9,'bold'),
                     bg='white',fg='firebrick1')
alreadyaccount.grid(row=10,column=0,sticky='w',padx=25,pady=10)

loginButton=Button(frame,text='Sing In',font=('Open Sans',9,'bold underline'),
                   fg='firebrick1',bg='white',activeforeground='blue'
                   ,activebackground='white',cursor='hand2',bd=0,command=signIn_pege)
loginButton.place(x=177
                  ,y=382)
sinup_window.mainloop()