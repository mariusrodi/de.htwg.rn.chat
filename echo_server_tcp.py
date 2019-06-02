import socket
import time

My_IP = socket.gethostbyname(socket.gethostname())
My_PORT = 50000
server_activity_period=30;
socket.setdefaulttimeout(5)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((My_IP, My_PORT))
print('Listening on Port ',My_PORT, ' for incoming TCP connections');

t_end=time.time()+server_activity_period # Ende der Aktivitätsperiode

sock.listen(1)
print('Listening ...')

try:
    conn, addr = sock.accept()
    data = conn.recv(1024).decode('utf-8')
    print('received message: ', data, 'from ', addr)
    conn.send('1Marius\0'.encode('ascii', 'replace'))
    print('send message 1Marius')
except socket.timeout:
    print('Socket timed out listening',time.asctime())

conn.send('00hi there, everything good?\0'.encode('ascii', 'replace'))
sock.close()
if conn:
    conn.close()
