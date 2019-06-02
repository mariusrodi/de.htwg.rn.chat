import socket

Server_IP = socket.gethostbyname(socket.gethostname())
Server_PORT = 50000
MESSAGE = '1Marius'

def recv():
    try:
        msg=sock.recv(1024).decode('utf-8')
        print('Message received; ', msg)
        recv()
    except socket.timeout:
        print('Socket timed out at',time.asctime())
        sock.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Connecting to TCP server with IP ', Server_IP, ' on Port ', Server_PORT)
sock.connect((Server_IP, Server_PORT))
print('Sending message', MESSAGE)
sock.send(MESSAGE.encode('utf-8'))
msg = sock.recv(1024).decode('utf-8')
if len(msg) > 0:
    sock.send(' hallo'.encode('utf-8'))
    sock.send(' hi'.encode('utf-8'))
recv()



