import time
import subprocess
import socket
import time
import json
from contextlib import closing

cwd = '.'

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
def start_client(port):
    subprocess.Popen(['python', cwd + '/client.py', str(port)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
def send_to_server(message, client_socket):
    client_socket.sendall(message.encode('utf-8'))

def recv_from_server(client_socket):
    message = client_socket.recv(4096)
    return message.decode('utf-8')

def get_join_key(client_socket):
    key = recv_from_server(client_socket)
    assert len(key) == 4
    return key

join_keys = []

for i in range(100):
    # Host Stuff
    port_host = find_free_port()
    print(i)
    start_client(port_host)
    time.sleep(2)
    client_socket_host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_address_host = ('localhost', port_host)
    client_socket_host.connect(client_address_host)

    send_to_server('host', client_socket_host)
    join_key = get_join_key(client_socket_host)
    join_keys.append(join_key)

print(len(join_keys))




