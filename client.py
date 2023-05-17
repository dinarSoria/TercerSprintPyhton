import socket
import threading

username = input("Enter your username: ")

host = '127.0.0.1'
port = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "@username":
                client.send(username.encode("utf-8"))
            else:
                print(message)
        except:
            print("An error occurred")
            client.close()
            break

def send_message():
    while True:
        message = input('')
        if message.startswith('/priv'):
            parts = message.split(' ')
            if len(parts) > 2:
                recipient = parts[1]
                content = ' '.join(parts[2:])
                private_message = f"/priv {recipient} {content}"
                client.send(private_message.encode('utf-8'))
            else:
                print("Invalid command. Usage: /priv <username> <message>")
        elif message == '/exit':
            client.send('/exit'.encode('utf-8'))
        else:
            client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_message)
send_thread.start()
