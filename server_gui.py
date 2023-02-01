import time
import tkinter as tk
import socket
import threading

import utils

window = tk.Tk()
window.title("Sever")

# Top frame consisting of two buttons widgets (i.e. btnStart, btnStop)
topFrame = tk.Frame(window)
btnStart = tk.Button(topFrame, text="Connect", command=lambda : start_server())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(topFrame, text="Stop", command=lambda : stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))

# Middle frame consisting of two labels for displaying the host and port info
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Host: X.X.X.X")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

# The client frame shows the client area
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="**********Client List**********").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=15, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))


server = None
HOST_ADDR = "192.168.1.7"
HOST_PORT = 8080

server_private_key=utils.createPrivateKey()
server_pub_key=utils.extractPublicKey(server_private_key)
print('server pub key')
print(server_pub_key)
ser_pub_key=utils.serialize_key(server_pub_key)
print('serializable')
print(ser_pub_key)

client_name = " "
clients = {}
clients_names = []
client_public_keys ={}
clients_keys={}

def send_active_users():
    active_users = "[Active Users] " + " ".join(clients_names)
    for client in clients:
        #key =  desrialize_key(client_public_keys[client])
        #client.send(encrypt_message(key, active_users))
        client.send(active_users.encode())

# Start server function
def start_server():
    global server, HOST_ADDR, HOST_PORT # code is fine without this
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(socket.AF_INET)
    print(socket.SOCK_STREAM)

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)  # server is listening for client connection

    threading._start_new_thread(accept_clients, (server, " "))

    lblHost["text"] = "Host: " + HOST_ADDR
    lblPort["text"] = "Port: " + str(HOST_PORT)


# Stop server function
def stop_server():
    global server
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)


def accept_clients(the_server, y):
    while True:
        client, addr = the_server.accept()

        # use a thread so as not to clog the gui thread
        threading._start_new_thread(send_receive_client_message, (client, addr))


def send_private_message( recipient, message, sender):
    for client in clients:
        print(clients[client])
        if clients[client] == recipient:
            print("recipient")
            key = clients_keys[client]
            message = f"{sender} -> you : {message}"
            print("message")
            print(message)
            client.send(str(utils.encrypt_message(key, message)).encode())
            print("sent success")




# Function to receive message from current client AND
# Send that message to other clients
def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, clients, clients_addr
    client_msg = " "

    # send welcome message to client
    client_name  = client_connection.recv(4096).decode()
    clients[client_connection] = client_name

    print(client_name)
    print("0000000000000000000000000000")
    time.sleep(0.5)
    from_client = client_connection.recv(4096).decode()

    if from_client.startswith('PUBKEY'):
        key = " ".join(from_client.split(" ")[1:]).encode()
        print(key)
        pub_key = utils.desrialize_key(key)
        clients_keys[client_connection] = pub_key

    welcome_msg = "Welcome " + client_name + ". Use 'exit' to quit ."
    client_connection.send(welcome_msg.encode())
    time.sleep(0.5)
    client_connection.send(f"PUBKEY {ser_pub_key.decode()}".encode())
    time.sleep(0.5)
    send_active_users()

    clients_names.append(client_name)

    update_client_names_display(clients_names)  # update client names display


    while True:
        data = client_connection.recv(4096)
        if not data: break
        if data == "exit" : break

        client_msg = utils.decrypt_message(server_private_key,data)

        idx = get_client_index(clients, client_connection)
        sending_client_name = clients_names[idx]
        print(client_msg)

        if client_msg[0]=='@':
            print("famaaa @")
            recipient = client_msg.split(" ")[0][1:]
            print(recipient)
            message = " ".join(client_msg.split(" ")[1:])
            print(message)
            send_private_message(recipient, message, sending_client_name)


    # find the client index then remove from both lists(client name list and connection list)
    server_msg = "BYE!"
    client_connection.send(server_msg.encode())
    client_connection.close()

    update_client_names_display(clients_names)  # update client names display


# Return the index of the current client in the list of clients
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


# Update client name display when a new client connects OR
# When a connected client disconnects
def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c+"\n")
    tkDisplay.config(state=tk.DISABLED)


window.mainloop()
