"""
Networking module for the game server.
This module handles the communication between the server and the players.
"""
import functools


MSG_SIZE = 2048

def connection_closed_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("Debug Statement")
        try:
            return func(*args, **kwargs)
        except (ConnectionResetError, ConnectionAbortedError, ConnectionError):
            print("Handler has been called!")
            #conn, addr = args
            #disconnect()
            exit()

    return wrapper

@connection_closed_handler
def flood_players(message, table, sender_uid=None):
    """
    Flood Players
    Send a message to all players
    :param message: Message to send
    :param table: Server instance
    :param sender_uid: User ID of the sender
    :return: None
    """
    if sender_uid is not None:
        # If sender_uid is provided, exclude the sender from the flood
        for player in table.players:
            if player["uid"] != sender_uid and player["alive"]:
                player["conn"].sendall(message.encode())
    else:
        for player in table.players:
            if player["alive"]:
                player["conn"].sendall(message.encode())

@connection_closed_handler
def send_message_to_player(player, message):
    """
    Send a message to a specific player
    :param player: Player instance
    :param message: Message to send
    :return: None
    """
    player["conn"].sendall(message.encode())

@connection_closed_handler
def receive_message(player):
    """
    Receive a message from a player
    :param player: Player instance
    :return: Message received
    """
    try:
        message = player["conn"].recv(MSG_SIZE).decode()
        return message
    except (ConnectionResetError, ConnectionAbortedError, ConnectionError):
        print("Connection closed")
        disconnect(player)
        return None


def disconnect(player):
    """
    Disconnect a player
    :param player: player instance
    :return: None
    """
    player["conn"].close()
    player["alive"] = False