"""
Main Programm for the Server
"""
import socket
import threading
import pickle
import json
import random


MSG_SIZE = 2048
PORT = 8000

clients = []
Server = socket.create_server(("0.0.0.0", PORT),backlog=5)

#players =  {0: {"name": "Player 1", "skin": "default", "cards": [], "card_count": 0},
#            1: {"name": "Player 1", "skin": "default", "cards": [], "card_count": 0},
#            2: {"name": "Player 1", "skin": "default", "cards": [], "card_count": 0},
#            3: {"name": "Player 1", "skin": "default", "cards": [], "card_count": 0},
#            4: {"name": "Player 1", "skin": "default", "cards": [], "card_count": 0},
#            5: {"name": "Player 1", "skin": "default", "cards": [], "card_count": 0}}

players = {0:None,}

current_player = 0
next_player = 1

#socket.bind("0.0.0.0", 8000)

def shuffle_deck():
    """
    Shuffle the deck
    """
    deck = []
    while len(deck) < 30:
        if len(deck) < 9:
            deck.append("Ace")
        elif len(deck) < 18:
            deck.append("Queen")
        elif len(deck) < 27:
            deck.append("King")
        else:
            deck.append("Joker")
    random.shuffle(deck)
    random.shuffle(deck)

    for player in players:
        players[player]["cards"] = deck[:5]
        deck = deck[5:]


def game_loop(player_info):
    """
    Game loop
    :param player_info: player info
    """
    conn = player_info["conn"]
    shuffle_deck()
    conn.send(pickle.dumps(players[player_info["uid"]]["cards"]))
    while True:
        if current_player == player_info["uid"]:
            # Player's turn
            pass
        elif next_player == player_info["uid"]:
            # Player has to choose a card
            pass

def pregame_loop(player_info):
    old_len = len(players)
    while len(players)<5:
        if old_len != len(players):
            data = ""
            for i in players:
                data += f"{i},{players[i]['name']},{players[i]['skin']};"
            player_info["conn"].send(data.encode())
            old_len = len(players)
        pass
    game_loop(player_info)

def update_players(conn, addr,  uid):
    """
    Update the players
    :param conn: connection
    :param addr: address
    :param uid: user id
    :return: player info
    """
    name,skin = conn.recv(MSG_SIZE).decode().split(",")
    players[uid]["name"] = name
    players[uid]["skin"] = skin
    players[uid]["cards"] = []
    json.dumps(players)

    player_info = players[uid].copy()
    player_info["conn"] = conn
    player_info["addr"] = addr
    player_info["uid"] = uid
    return player_info


def new_connection(conn, addr):
    """
    Handle new connections
    :param conn: connection
    :param addr: address
    """
    print(f"Connection from {addr} has been established!")
    uid = len(clients)
    player_info = update_players(conn, addr, uid)
    conn.send(f"{uid}".encode())

    data = ""
    for i in players:
        data += f"{i},{players[i]['name']},{players[i]['skin']};"
    conn.send(data.encode())

    pregame_loop(player_info)


def disconnect(conn, addr):
    """
    Disconnect the client
    :param conn: connection
    :param addr: address
    """
    print(f"Connection from {addr} has been terminated!")
    conn.close()
    clients.remove(threading.current_thread())
    exit()


print(f"Server is running on port {PORT} and awaiting connections...")
while True:
    try:
        connection, address = Server.accept()
        client = threading.Thread(target=new_connection, args=(connection, address))

        clients.append(client)
        client.start()

    except (KeyboardInterrupt, ConnectionResetError, ConnectionError) as err:
        print("Server is shutting down...")
        for client in clients:
            client.join()
        Server.close()
        break
