import socket
import time
import threading

# Standard input only in main thread. If message should be send: identify
# connection thread with name of client and thread id and give message to thread


PORT = 50000
IP = socket.gethostbyname(socket.gethostname())
QUIT_FLAG = 0
QUIT_LOCK = threading.Lock()
MESSAGES = []
MESSAGES_LOCK = threading.Lock()
NAME = 'Dummkopf'

socket.setdefaulttimeout(5)

def recv_message():
    msg = sock.recv(1024)
    print(msg)
    QUIT_LOCK.acquire()
    if QUIT_FLAG == 1:
        QUIT_LOCK.release()
        print('QUIT_FLAG has been set')
        sock.close()
    else:
        recv_message() 

def send_message():
    MESSAGES_LOCK.acquire()
    while element in MESSAGES:
        if sock.send(element.encode('utf-8')):
            MESSAGES.remove(element)
    MESSAGES_LOCK.release()

def start_communication():
    thread = threading.Thread(target = recv_message())
    thread.start()
    send_message()

def start_server():
    global QUIT_FLAG
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP, PORT))
    print('Listening on Port', PORT, 'for incoming TCP connection')
    sock.listen(1)
    try:
        conn, addr = sock.accept()
        sock.send(NAME.encode(utf-8))
        thread = threading.Thread(target = start_server)
        thread.start()
        start_communication()
    except socket.timeout:
        print('ERR:TIMEOUT No connection etablished!')
        sock.close()
        QUIT_LOCK.acquire()
        if QUIT_FLAG == 1:
            QUIT_LOCK.release()
            print('QUIT_FLAG has been set')
        else:
            QUIT_LOCK.release()
            start_server()

def take_input():
    global QUIT_FLAG
    user_input = ''
    while True:
        user_input = input('INPUT >> ')
        if user_input == 'quit':
            QUIT_LOCK.acquire()
            QUIT_FLAG = 1
            QUIT_LOCK.release()
            return
        MESSAGES_LOCK.acquire()
        MESSAGES.append(user_input)
        MESSAGES_LOCK.release()

def main():
    thread = threading.Thread(target = start_server)
    thread.start()
    #start_server()
    take_input()

if __name__ == '__main__':
    main()
    
