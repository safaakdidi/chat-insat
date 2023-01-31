import tkinter as tk
from tkinter import messagebox
import socket
import threading
from utils import *

username = " "
active_users = []
# network client
client = None
HOST_ADDR = "192.168.1.78"
HOST_PORT = 8080
username = " "
active_users = []





class Client:
    def __init__(self, host, port, username):
        self.private_key = createPrivateKey()
        self.public_key =extractPublicKey(self.private_key)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        print(username)
        self.socket.send(username.encode())
        self.username = username
        self.gui_done = False
        self.running = True
        self.tkDisplay = None
        msg = tk.Tk()
        msg.withdraw()


        gui_thred = threading.Thread(target=self.client_gui)
        receive_thread =threading.Thread(target=self.receive_message_from_server)
        gui_thred.start()
        receive_thread.start()
    def receive_message_from_server(self):

        while True:

            from_server = self.socket.recv(4096).decode()
            if not from_server: break

            print("from server")
            print(from_server)

            # display message from server on the chat window
            if from_server.startswith("[Active Users] "):
                active_users = from_server.split(" ")[2:]
                self.update_active_users(active_users)

            # enable the display area and insert the text and then disable.
            # why? Apparently, tkinter does not allow us insert into a disabled Text widget :(
            self.window.update()

            texts = self.tkDisplay.get("1.0", tk.END).strip()

            self.tkDisplay.config(state=tk.NORMAL)
            if len(texts) < 1:
                self.tkDisplay.insert(tk.END, from_server)
            else:
                self.tkDisplay.insert(tk.END, "\n\n" + from_server)

            self.tkDisplay.config(state=tk.DISABLED)
            self.tkDisplay.see(tk.END)

            # print("Server says: " +from_server)

        self.socket.close()
        self.window.destroy()
    def client_gui(self):
        self.window = tk.Tk()
        self.window.title("Chat")
        self.topFrame = tk.Frame(self.window)

        # btnConnect.bind('<Button-1>', connect)
        self.topFrame.pack(side=tk.TOP)
        self.sideFrame = tk.Frame(self.window, width=200, height=300, bg="grey")
        self.sideFrame_label = tk.Label(self.sideFrame, text="Connected Users", bg="#021b39")

        self.sideFrame.pack(side=tk.LEFT, fill=tk.Y)

        self.listbox = tk.Listbox(self.sideFrame)
        self.listbox.pack(padx=20, pady=5)

        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        self.displayFrame = tk.Frame(self.window)
        self.scrollBar = tk.Scrollbar(self.displayFrame)
        self.scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tkDisplay = tk.Text(self.displayFrame, height=20, width=55)
        self.tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.tkDisplay.tag_config("tag_your_message", foreground="blue")
        self.scrollBar.config(command=self.tkDisplay.yview)
        self.tkDisplay.config(yscrollcommand=self.scrollBar.set, background="#F4F6F7", highlightbackground="grey",
                         state="disabled")
        self.displayFrame.pack(side=tk.TOP)
        self.bottomFrame = tk.Frame(self.window)
        self.tkMessage = tk.Text(self.bottomFrame, height=2, width=55)
        self.tkMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
        self.tkMessage.config(highlightbackground="grey", state="disabled")
        self.tkMessage.bind("<Return>", (lambda event: self.getChatMessage(self.tkMessage.get("1.0", tk.END))))
        self.bottomFrame.pack(side=tk.BOTTOM)
        self.window.mainloop()
    def on_select(self,event):
        selection = self.listbox.get(self.listbox.curselection())
        print(selection)
    def update_active_users(self,active_users):
        self.listbox.config(state='normal')
        self.listbox.delete(0, tk.END)
        for user in active_users:
            if user != username:
                self.listbox.insert(tk.END, user)
    def getChatMessage(self,msg):

        msg = msg.replace('\n', '')
        texts = self.tkDisplay.get("1.0", tk.END).strip()

        # enable the display area and insert the text and then disable.
        # why? Apparently, tkinter does not allow use insert into a disabled Text widget :(
        self.tkDisplay.config(state=tk.NORMAL)
        if len(texts) < 1:
            self.tkDisplay.insert(tk.END, "You->" + msg, "tag_your_message")  # no line
        else:
            self.tkDisplay.insert(tk.END, "\n\n" + "You->" + msg, "tag_your_message")

        self.tkDisplay.config(state=tk.DISABLED)

        self.send_mssage_to_server(msg)

        self.tkDisplay.see(tk.END)
        self.tkMessage.delete('1.0', tk.END)
    def send_mssage_to_server(self,msg):
        client_msg = str(msg)
        client.send(client_msg.encode())
        if msg == "exit":
            client.close()
            self.window.destroy()
        print("Sending message")



