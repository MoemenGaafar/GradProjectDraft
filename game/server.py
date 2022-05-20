#!/usr/bin/env python

import asyncio
import websockets
import os
import signal
import json
import random
import string
from experience_manager import ExperienceManager


JOIN = {}

async def error(websocket, message):
    event = {
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))

async def play(websocket, game, connected, player):
    async for message in websocket:
        event = json.loads(message)
        print("Server received", event, "from player", player)
        type = event['type']

        if type == 'role':
            role = event['pick']
            game.set_player_role(player, role)
            if game.all_players_assigned():
                for player in range(len(connected)):
                    first_scene = game.get_first_scene(player)
                    event = {"type": "show", "label": first_scene}
                    await connected[player].send(json.dumps(event))

        elif type == 'choice':
            game.apply_choice_postconditions(label = event['label'], menu_label = event['menu_label'], choice = event['choice'])

        elif type == 'show_request':
            players, next_scene = game.get_next_scene(player)
            for id in players:
                event = {"type": "show","label": next_scene}
                await connected[id].send(json.dumps(event))
                print("Server sent", event, "to player", id)
        
        elif type == 'check_choice':
            choice = game.check_choice(event['label'], event['menu_label'])
            event = {'type': 'checked_choice', 'choice': choice}
            await connected[player].send(json.dumps(event))
            print("Server sent", event, "to player", player)
        
        elif type == 'validate_choices':
            valid_choices = game.validate_choices(event['label'], event['menu_label'])
            event = {'type': 'validated_choices', 'choices': valid_choices}
            await connected[player].send(json.dumps(event))
            print("Server sent", event, "to player", player)

async def join(websocket, join_key):
    try:
        game, connected = JOIN[join_key]
    except KeyError:
        await error(websocket, "Game not found.")
        return

    # Register to receive moves from this game.
    connected.append(websocket)

    try:
        event = {
            "type": "game",
            "action": "start"
        }

        websockets.broadcast(connected, json.dumps(event))

        # Temporary - for testing.
        print("second player joined game", id(game))

        await play(websocket, game, connected, 1)

    finally:
        print('Disconnected from game session')
#        connected.remove(websocket)

async def start(websocket):
    # Initialize an Experience Manager, the set of WebSocket connections
    # receiving events from this game, and secret access token.
    game = ExperienceManager(state_file = "initial_state.json", \
        scene_file = "scenes.json", plot_file = "plot.json", players_file= "players_data.json")
    connected = [websocket]

    join_key = "".join(random.choice(string.ascii_letters) for _ in range(4)).upper()

    JOIN[join_key] = game, connected

    try:
        # Send the secret access token to the client of the first player.
        event = {
            "type": "init",
            "join": join_key,
        }
        await websocket.send(json.dumps(event))

        # Temporary - for testing.
        print("first player started game", id(game))
        await play(websocket, game, connected, 0)

    finally:
        print('Ended and Removed game session')
        # TODO: Implement clean ending of game session
#        del JOIN[join_key]


async def handler(websocket):
    # Receive and parse the "init" event from the Client
    message = await websocket.recv()
    event = json.loads(message)
    if event["type"] == "init":
        print('received init')
        # First player starts a new game.
        await start(websocket)
    elif event['type'] == 'join':
        print('received join with key', event['key'])
        # Second player joins an existing game.
        await join(websocket, event["key"])

async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    port = int(os.environ.get("PORT", "8765"))
    async with websockets.serve(handler, "", port, ping_interval = None):
        await stop


asyncio.run(main())