import socket
import time

# Standard input only in main thread. If message should be send: identify
# connection thread with name of client and thread id and give message to thread


PORT = 50000
IP = socket.gethostbyname(socket.gethostname())
QUIT_FLAG = 0

socket.setdefaulttimeout(5)

def start_communication():
    sock.send(message.encode('utf-8'))
    msg=sock.recv(1024)
    sock.close()

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP, PORT))
    print('Listening on Port', PORT, 'for incoming TCP connection')
    sock.listen(1)
    try:
        conn, addr = sock.accept()
        # starte Kommunikation über Funktion start_task()
    except socket.timeout:
        print('ERR:TIMEOUT No connection etablished!')
        sock.close()
        start_server()
        pass


def main():
    start_server()

if __name__ == '__main__':
    main()
