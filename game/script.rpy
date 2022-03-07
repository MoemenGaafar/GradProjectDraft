# type: ignore

define moemen = Character('Moemen')
define alaa = Character('Alaa')

init python:
    import os
    import subprocess
    import socket

    cwd =  '../RenPyTest' # os.getcwd()
    next_file_path = cwd + '/game/info/next_scene.txt'
    choice_file_path = cwd + '/game/info/choice.txt'
    join_file_path = cwd + '/game/info/join_key.txt'

    def start_client():
        subprocess.call('python3 ' + cwd + '/game/client.py', shell=True)

    def send_to_server(message):
        subprocess.call('python3 ' + cwd + '/game/out_channel.py \"'+message+'\"', shell=True)

    def recv_from_server():
        message = subprocess.check_output('python3 ' + cwd + '/game/in_channel.py', shell=True)
        return message.decode('utf-8')[:-1]
    
    def host_new_game():
        send_to_server('host')
    
    def get_join_key():
        key = recv_from_server()
        assert len(key) == 4
        return key

#    start_client()

label start:
    jump login

menu login:
    "Do you want to host a new game or join an already-existing one?"
    "Host": 
        python:
            host_new_game()
            narrator("Waiting for server to send join key")
            join_key = get_join_key()
            narrator("Your join key is "+join_key)

        jump host
    "Join": 
        $ send_to_server('Join')
        jump join

label host:
    "Host"

label join:
    "Join"

menu pickRole:
    "Pick a role!"
    "I want to control how Moemen feels.":
        jump controller
    "I want to perceive how Moemen feels.":
        jump perceiver

label controller:
    python:
        narrator("How do you want Moemen to feel?", interact=False)
        mood = renpy.display_menu([("Happy", "happy"), ("Sad", "sad")])
        with open(next_file_path, 'w') as next_file:
            next_file.write(mood)
        narrator("Moemen is now "+mood+"!")
        renpy.jump("controller")
    
label perceiver:
    scene bg whitehouse
    show moemen main at left
    moemen "Hi I am Moemen"
    moemen "Let's see how I am feeling!"
    jump next

label sad:
    moemen "I am sad"
    jump next

label happy:
    moemen "I am happy"
    jump next

label next:
    moemen "Let's see how I am feeling!"
    python:
        with open(next_file_path, 'r') as next_file:
            next_scene = next_file.read().strip()
        renpy.jump(next_scene)
