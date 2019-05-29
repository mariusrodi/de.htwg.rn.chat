import socket
import time
import threading

PORT = 50000
IP = socket.gethostbyname(socket.gethostname())
socket.setdefaulttimeout(5)

QUIT_FLAG = 0
QUIT_LOCK = threading.Lock()

MESSAGES = []
MESSAGES_LOCK = threading.Lock()

NAME = 'Dummkopf'

CONNECTIONS = []
CONNECTIONS_LOCK = threading.Lock()

BUDDYS = []


# TODO add global buddy list, contains buddy IPs
# TODO add global connection list, contains toupel of NAME and IP


class Searcher(threading.Thread):
    # TODO go throug buddy list and try to connect
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = 'Searcher'

    def __repr__(self):
        return self.name

    def run(self):
        pass


class Listener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = 'Listener'

    def __repr__(self):
        return self.name

    def run(self):
        global QUIT_FLAG
        global NAME
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((IP, PORT))
        #print('Listening on Port', PORT, 'for incoming TCP connection')
        sock.listen(1)
        try:
            conn, addr = sock.accept()
            #print('Connection etablished with ' + conn)
            receiver = Receiver(conn, addr, True)
            receiver.run()
        except socket.timeout:
            #print('ERR:TIMEOUT No connection etablished!')
            pass
        sock.close()
        QUIT_LOCK.acquire()
        if QUIT_FLAG == 1:
            QUIT_LOCK.release()
            print('QUIT_FLAG has been set!')
        else:
            QUIT_LOCK.release()
            #print('Renewing connection!')
            self.run()


class Receiver(threading.Thread):
    def __init__(self, conn, addr, is_first):
        self.name = addr
        self.conn = conn
        self.is_first = is_first
        self.counter = 0
    
    def __repr__(self):
        return 'Receiver of ' + self.name

    def run(self):
        global QUIT_FLAG
        global CONNECTIONS
        if self.is_first == True:
            sender = Sender(self.conn, self.addr, False)
            sender.start()
        while True:
            QUIT_LOCK.acquire()
            if QUIT_FLAG == 1:
                QUIT_LOCK.release()
                return
            msg = conn.recv(1024)
            if self.counter == 0:
                CONNECTIONS_LOCK.acquire()
                CONNECTIONS.append([self.addr, msg])
                CONNECTIONS_LOCK.release()
            counter += 1
            print(self.name + ' wrote: ' + msg)


class Sender(threading.Thread):
    def __init__(self, conn, addr, is_first):
        threading.Thread.__init__(self)
        self.name = addr
        self.conn = conn
        self.is_first = is_first

    def __repr__(self):
        return 'Sender of ' + self.name

    def run(self):
        global MESSAGES
        sock.send(NAME.encode(utf-8))
        if self.is_first == True:
            recv = Receiver(self.conn, self.addr, False)
            recv.start()
        while True:
            MESSAGES_LOCK.acquire()
            while element in MESSAGES:
                name = element[0]
                # TODO Find name in CONNECTIONS and get IP address of name.
                #      Compare IP address with self.name -> true: send msg
                #if name == self.name:
                    #conn.send(element[1].encode('utf-8'))
                    #MESSAGES.remove(element)
            MESSGAES_LOCK.release()
            QUIT_LOCK.acquire()
            if QUIT_FLAG == 1:
                QUIT_LOCK.release()
                return


def take_input():
    global QUIT_FLAG
    global MESSAGES
    user_input = ''
    while True:
        user_input = input('INPUT >> \n')
        if user_input == 'quit':
            QUIT_LOCK.acquire()
            QUIT_FLAG = 1
            QUIT_LOCK.release()
            return
        try:
            name, msg = user_input.split('::')
            MESSAGES_LOCK.acquire()
            MESSAGES.append([name, msg])
            MESSAGES_LOCK.release()
            print('You send to ' + name + ' following message: ' + msg)
        except:
            print('ERR: Could not read input! Valid syntax is:\nquit               Quit service\nreceiver::message  Send Message to Receiver')

def main():
    listener = Listener()
    listener.start()
    take_input()

if __name__ == '__main__':
    main()
