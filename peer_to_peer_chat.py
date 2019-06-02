import socket
import time
import threading

PORT = 50000
IP = socket.gethostbyname(socket.gethostname())
socket.setdefaulttimeout(5)

WRITE_LOCK = threading.Lock()

QUIT_FLAG = 0
QUIT_LOCK = threading.Lock()

NAME = '1Dummkopf\0'

CONNECTIONS = {}
CONNECTIONS_LOCK = threading.Lock()

BUDDYS = {'Marius': socket.gethostbyname(socket.gethostname())}

MESSAGES = []
MESSAGES_LOCK = threading.Lock()

class Broadcaster(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global QUIT_FLAG
        global NAME
        global BUDDYS
        global PORT
        global MESSAGES
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            CONNECTIONS_LOCK.acquire()
            connections = CONNECTIONS
            CONNECTIONS_LOCK.release()
            for key in BUDDYS:
                try:
                    if connections.get(key) == None:
                        sock.connect((BUDDYS[key], PORT))
                        sock.send(NAME.encode('ascii', 'replace'))
                        msg = sock.recv(1024).decode('ascii', 'replace')
                        MESSAGES_LOCK.acquire()
                        MESSAGES.append(msg)
                        MESSAGES_LOCK.release()
                        if msg[:1] == '1':
                            CONNECTIONS_LOCK.acquire()
                            CONNECTIONS[msg] = sock
                            CONNECTIONS_LOCK.release()
                except:
                    pass
                QUIT_LOCK.acquire()
                if QUIT_FLAG == 1:
                    QUIT_LOCK.release()
                    WRITE_LOCK.acquire()
                    print('QUITLFAG has been set! Broadcaster is ending!')
                    sock.close()
                    WRITE_LOCK.release()
                    return
                QUIT_LOCK.release()
            time.sleep(1)


class Listener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global QUIT_FLAG
        global NAME
        global CONNECTIONS
        global PORT
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((IP, PORT))
        sock.listen(1)
        while True:
            try:
                conn, addr = sock.accept()
                msg = conn.recv(1024).decode('ascii', 'replace')
                if msg[:1] == '1':
                    conn.send(NAME.encode('ascii', 'replace'))
                    CONNECTIONS_LOCK.acquire()
                    CONNECTIONS[msg[1:]] = conn
                    CONNECTIONS_LOCK.release()
            except socket.timeout:
                pass
            QUIT_LOCK.acquire()
            if QUIT_FLAG == 1:
                QUIT_LOCK.release()
                WRITE_LOCK.acquire()
                print('QUIT_FLAG has been set! Listener is ending!')
                sock.close()
                WRITE_LOCK.release()
                return
            QUIT_LOCK.release()


class Receiver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        global QUIT_FLAG
        global CONNECTIONS
        global MESSAGES
        while True:
            CONNECTIONS_LOCK.acquire()
            connections = CONNECTIONS
            CONNECTIONS_LOCK.release()
            for key in connections:
                try:
                    msg = connections[key].recv(1024).decode('ascii', 'replace')
                    if (msg[:2] == '01') or (msg[:2] == '00'): 
                        WRITE_LOCK.acquire()
                        print('\n' + key + ' wrote: ' + msg)
                        WRITE_LOCK.release()
                        MESSAGES_LOCK.acquire()
                        MESSAGES.append(msg)
                        MESSAGES_LOCK.release()
                except socket.timeout:
                    pass
            QUIT_LOCK.acquire()
            if QUIT_FLAG == 1:
                QUIT_LOCK.release()
                print('QUIT_FLAG has been set! Receiver is ending!')
                CONNECTIONS_LOCK.acquire()
                for key in CONNECTIONS:
                    CONNECTIONS[key].close()
                CONNECTIONS_LOCK.release()
                return
            QUIT_LOCK.release()
            time.sleep(1)


def take_input():
    global QUIT_FLAG
    global MESSAGES
    user_input = ''
    while True:
        user_input = input('INPUT >> ')
        if user_input == 'quit':
            QUIT_LOCK.acquire()
            QUIT_FLAG = 1
            QUIT_LOCK.release()
            return
        elif user_input == 'conn':
            CONNECTIONS_LOCK.acquire()
            connections = CONNECTIONS
            CONNECTIONS_LOCK.release()
            WRITE_LOCK.acquire()
            print(connections)
            WRITE_LOCK.release()
        elif user_input == 'msg': 
            WRITE_LOCK.acquire()
            MESSAGES_LOCK.acquire()
            print(MESSAGES)
            MESSAGES_LOCK.release()
            WRITE_LOCK.release()
        else:
            try:
                name, msg = user_input.split('::')
                if name == 'ALL':
                    msg = '01' + msg + '\0'
                    CONNECTIONS_LOCK.acquire()
                    for key in CONNECTIONS:
                        CONNECTIONS[key].send(msg.encode('ascii', 'replace'))
                    CONNECTIONS_LOCK.release()
                else:
                    msg = '00' + msg + '\0'
                    CONNECTIONS_LOCK.acquire()
                    if name in CONNECTIONS:
                        CONNECTIONS[name].send(msg.encode('ascii', 'replace'))
                    CONNECTIONS_LOCK.release()
            except:
                WRITE_LOCK.acquire()
                print('ERR: Could not read input! Valid syntax is:\n \
quit               Quit service\n \
receiver::message  Send Message to Receiver\n \
ALL::message       Send Message to All\n \
conn               List connections\n \
msg                List messages\n')
                WRITE_LOCK.release()


def main():
    listener = Listener()
    listener.start()

    broadcaster = Broadcaster()
    broadcaster.start()

    receiver = Receiver()
    receiver.start()

    take_input()
    
    listener.join()
    broadcaster.join()
    receiver.join()

    print('QUIT_FLAG has been set! Input is ending!')

if __name__ == '__main__':
    main()
