"""
Main Programm for the Server
"""
import socket
import threading
import pickle
import json
import random
import functools

MSG_SIZE = 2048
PORT = 8000

clients = []
Server = socket.create_server(("0.0.0.0", PORT), backlog=5)

players = {}

current_player = 0
card_of_round = ""
shuffle_done_event = threading.Event()
cards_set = []
changes = False


#socket.bind("0.0.0.0", 8000)

def connection_closed_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("Debug Statement")
        try:
            return func(*args, **kwargs)
        except (ConnectionResetError, ConnectionAbortedError, ConnectionError):
            print("Handler has been called!")
            #conn, addr = args
            disconnect()
            exit()

    return wrapper


def shuffle_deck():
    """
    Shuffle the deck
    """
    global card_of_round

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
    card_of_round = random.choice(["Ace", "Queen", "King"])

    for player in players:
        players[player]["cards"] = deck[:5]
        deck = deck[5:]

    shuffle_done_event.set()



@connection_closed_handler
def flood_players(data, origin_uid=None):
    """
    Flood the players
    :param data: data to flood
    :param origin_uid: origin user id
    """
    for player in players:
        if player != origin_uid:
            conn = players[player]["conn"]
            conn.send(f"{data}".encode())


def increment_player():
    """
    Increment the player
    """
    global current_player
    current_player += 1
    if current_player == len(players):
        current_player = 0

#TODO
@connection_closed_handler
def game_loop(uid):
    """
    Game loop
    :param uid: User ID of the player
    """
    global current_player
    global cards_set

    conn = players["uid"]["conn"]

    if current_player == uid:
        shuffle_deck()
        conn.send(b"first")
        conn.send(pickle.dumps(players["uid"]["cards"]))
        cards_set = conn.recv(MSG_SIZE).decode().split(",")
        flood_players(len(cards_set), "uid")
        increment_player()
    else:
        conn.send(current_player.to_bytes(4, "big"))
        # Wait until shuffling is done
        shuffle_done_event.wait()
        conn.send(pickle.dumps(players["uid"]["cards"]))

    while True:
        if current_player == uid:
            if not players["uid"]["alive"]: increment_player()
            conn.send(b"now")
            return_data = conn.recv(MSG_SIZE).decode()
            if return_data == b"liar": flood_players(cards_set); liar()
            else: cards_set=return_data.split(",")
            increment_player()

        pass


#TODO
def liar():
    """
    Liar
    Check if the player is a liar and handle the consequences
    """
    accused_player = current_player-1
    if accused_player == -1:
        accused_player = len(players)

    for card in cards_set:
        if card != card_of_round or card != "Joker":
            break
    else:
        flood_players(f"liar,{current_player}")
        gun_handler(current_player)
        for card in cards_set:
            players[accused_player]["cards"].remove(card)
        return

    flood_players(f"liar,{accused_player}")
    gun_handler(accused_player)
    return

def gun_handler(uid):
    """
    Gun Handler
    """
    random.shuffle(players[uid]["gun"])
    if players[uid]["gun"][0]:
        players[uid]["alive"] = False
        flood_players(f"gun,{uid},live")
        return
    else:
        players[uid]["gun"].pop(0)
        flood_players(f"gun,{uid},blank")
        return






#TODO
@connection_closed_handler
def pregame_loop(uid):
    old_len = len(players)
    conn = players[uid]["conn"]
    votes = 0
    amount = 6
    global changes
    changes = False

    while len(players) < 6 or votes < amount:
        votes = 0
        amount = 0

        if old_len != len(players):
            old_len = len(players)
            changes = True


        transfer_data = conn.recv(MSG_SIZE)
        if transfer_data != 0:
            if transfer_data == b"True":
                players[uid]["voted"] = True
                changes = True

        for i in players:
            if players[i]["voted"]:
                votes += 1
            amount += 1
        if changes:
            data = ""
            for i in players:
                data += f"{i},{players[i]['name']},{players[i]['skin']},{players[i]['voted']};"
            players[uid]["conn"].send(data.encode())
            changes = False
            
    game_loop(uid)


def update_players(conn, addr, uid):
    """
    Update the players
    :param conn: connection
    :param addr: address
    :param uid: user id
    :return: player info
    """
    name, skin = conn.recv(MSG_SIZE).decode().split(",")
    players[uid] = {}
    players[uid]["name"] = name
    players[uid]["skin"] = skin
    players[uid]["cards"] = []
    players[uid]["voted"] = False
    players[uid]["alive"] = True
    players[uid]["gun"] = [False, False, False, False, False, True]
    players[uid]["conn"] = conn
    players[uid]["addr"] = addr
    random.shuffle(players[uid]["gun"])
    #json.dumps(players)


@connection_closed_handler
def new_connection(conn, addr):
    """
    Handle new connections
    :param conn: connection
    :param addr: address
    """
    #conn.settimeout(0.1)
    print(f"Connection from {addr} has been established!")
    uid = len(clients)-1
    update_players(conn, addr, uid)
    print(f"Player {uid} has joined the game with name {players[uid]['name']} and skin {players[uid]['skin']}")
    conn.send(f"{uid}".encode())
    print(f"Player {uid} has been assigned the ID {uid}")

    data = ""
    for i in players:
        data += f"{i},{players[i]['name']},{players[i]['skin']},{players[i]['voted']};"
    conn.send(data.encode())
    print(f"Informed Player {uid}")

    pregame_loop(uid)

#TODO
def disconnect(conn=None, addr=None):
    """
    Disconnect the client
    :param conn: connection
    :param addr: address
    """
    if conn is not None:
        print(f"Connection from {addr} has been terminated!")
        conn.close()
    else:
        print(f"Unexpected connection termination from unknown!")
    clients.remove(threading.current_thread())
    exit()

#TODO
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
