import time
import subprocess
import socket
import time
import threading
import json
from contextlib import closing
from random import choice, randint

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

def load_file(file):
    f = open(file)
    data = json.load(f)
    f.close()
    return data

def get_next_scene(client_socket):
    event = {'type': 'show_request'}
    send_to_server(json.dumps(event), client_socket)
    scene = recv_from_server(client_socket)
    return scene

def validate_choices(label, menu_label, client_socket):
    event = {'type': 'validate_choices', 'label': label, 'menu_label': menu_label}
    send_to_server(json.dumps(event), client_socket)
    valid_choices = json.loads(recv_from_server(client_socket))['choices']
    return valid_choices

def send_choice(label, menu_label, choice, client_socket):
    event = {'type': 'choice', 'label': label, 'menu_label': menu_label, 'choice': choice}
    send_to_server(json.dumps(event), client_socket)

def is_choice_done(label, menu_label, client_socket):
    event = {'type': 'check_choice', 'label': label, 'menu_label': menu_label}
    send_to_server(json.dumps(event), client_socket)
    choice = recv_from_server(client_socket)
    if choice == 'None':
        return None
    return choice

roles = ['Red', 'Wolf']
scenes = load_file('scenes.json')

def play(current_scene, client_socket, wait_times, index):
    time.sleep(randint(5, 20))
    current_waits = []
    while True:
        menus = scenes[current_scene]['menus']
        for menu in menus:
            if is_choice_done(current_scene, menu, client_socket) is None:
                start_time = time.time()
                valid_choices = validate_choices(current_scene, menu, client_socket)
                end_time = time.time()
                current_waits.append(end_time - start_time)
                
                if is_choice_done(current_scene, menu, client_socket) is None or len(valid_choices) != 0:
                    my_choice = choice(valid_choices)
                    send_choice(current_scene, menu, my_choice, client_socket)
                    time.sleep(randint(5, 20))

        start_time = time.time()
        next_scene = get_next_scene(client_socket)
        end_time = time.time()
        current_waits.append(end_time - start_time)
    
        if next_scene != 'wait_scene':
            time.sleep(randint(5, 20))
            current_scene = next_scene
        else:
            time.sleep(2)

        if current_scene == 'end_scene':
            wait_times[index]['max'] = max(current_waits)
            wait_times[index]['avg'] = sum(current_waits) / len(current_waits)
            break

def simulate_session(wait_times):
    # wait_times = [{'max': 0, 'avg': 0}, {'max': 0, 'avg': 0}]
    # Host Stuff
    print('Started a new session')
    port_host = find_free_port()
    start_client(port_host)
    time.sleep(2)
    client_socket_host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_address_host = ('localhost', port_host)
    client_socket_host.connect(client_address_host)
    send_to_server('host', client_socket_host)
    join_key = get_join_key(client_socket_host)


    # Join Stuff
    port_join = find_free_port()
    start_client(port_join)
    time.sleep(2)
    client_socket_join = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_address_join = ('localhost', port_join)
    client_socket_join.connect(client_address_join)
    send_to_server('join', client_socket_join)
    time.sleep(2)
    send_to_server(join_key, client_socket_join)

    # Receive start signals
    signal = recv_from_server(client_socket_host)
    assert signal == 'joined'
    signal = recv_from_server(client_socket_join)
    assert signal == 'joined'

    # Set Roles
    host_role = choice(roles)
    send_to_server(host_role, client_socket_host)
    host_current_scene = recv_from_server(client_socket_host)
    join_role = recv_from_server(client_socket_join)
    join_current_scene = recv_from_server(client_socket_join)

    host_thread = threading.Thread(target=play, args=(host_current_scene, client_socket_host, wait_times, 0))
    join_thread = threading.Thread(target=play, args=(join_current_scene, client_socket_join, wait_times, 1))

    host_thread.start()
    join_thread.start()

    host_thread.join()
    join_thread.join()
    print(wait_times)
    return wait_times

#while True:
#    host_menus = scenes[host_current_scene]['menus']
#    for menu in host_menus:
#        if is_choice_done(host_current_scene, menu, client_socket_host) is None:
#            valid_choices = validate_choices(host_current_scene, menu, client_socket_host)
#            my_choice = choice(valid_choices)
#            send_choice(host_current_scene, menu, my_choice, client_socket_host)
#            time.sleep(randint(5, 10))
#            
#    host_next_scene = get_next_scene(client_socket_host)
#
#    if host_next_scene != 'wait_scene':
#        time.sleep(randint(5, 10))
#        host_current_scene = host_next_scene
#
#    if join_current_scene == 'end_scene' and host_current_scene == 'end_scene':
#        break
#
#    join_menus = scenes[join_current_scene]['menus']
#    for menu in join_menus:
#        if is_choice_done(join_current_scene, menu, client_socket_join) is None:
#            valid_choices = validate_choices(join_current_scene, menu, client_socket_join)
#            my_choice = choice(valid_choices)
#            send_choice(join_current_scene, menu, my_choice, client_socket_join)
#            time.sleep(1)
#            
#    join_next_scene = get_next_scene(client_socket_join)
#    if join_next_scene != 'wait_scene':
#        join_current_scene = join_next_scene
#
#    if join_current_scene == 'end_scene' and host_current_scene == 'end_scene':
#        break
#
#print('done')
