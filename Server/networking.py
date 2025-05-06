"""
Networking module for the game server.
This module handles the communication between the server and the players.
"""
import functools
import pickle

MSG_SIZE = 2048
DEBUG = True


# Decorator to handle connection closed exceptions
def connection_closed_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ConnectionResetError, ConnectionAbortedError, ConnectionError, BrokenPipeError, OSError, EOFError):
            print("Connection closed")
            table, uid = None, None
            for arg in args:
                print(arg)
                if hasattr(arg, "table"):
                    print(f"Player {arg} has disconnected")
                    table= arg.table
                    uid = arg.uid
                    break
                elif hasattr(arg, "players"):
                    print(f"Table {arg} has disconnected")
                    table = arg
                    uid = kwargs.get("uid", None)
                    if uid is None:
                        print("No UID provided for player removal.")
                        return
                    break

            if table is not None and uid is not None:
                remove_player_from_table(table, uid)
            exit()

    return wrapper



@connection_closed_handler
def flood_players(message, table, sender_uid=None):
    """
    Flood Players
    Send a message to all players
    :param message: Message to send
    :type message: str
    :param table: Server instance
    :type table: class
    :param sender_uid: User ID of the sender
    :type sender_uid: int
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
    :type player: class
    :param message: Message to send
    :type message: str or bytes
    :return: None
    """
    if type(message) != bytes:
        message = message.encode()
    player.connection.sendall(message)


@connection_closed_handler
def receive_message(player):
    """
    Receive a message from a player
    :param  player: Player instance
    :type player: class
    :return: Message received
    """
    message = player.connection.recv(MSG_SIZE)
    if DEBUG: print(f"rec: {message}")
    try:
        message = pickle.loads(message)
        if DEBUG: print(f"{message} is pickle")
    except pickle.UnpicklingError:
        message= message.decode()
    if DEBUG: print(f"{message} is not pickle")
    return message


def disconnect(player):
    """
    Disconnect a player
    :param  player: player instance
    :return: None
    """
    player.connection.close()
    remove_player_from_table(player.table, player.uid)
    player.alive = False


def remove_player_from_table(table, uid):
    """
    Remove a player from the table
    :param table: table instance to remove the player from
    :param uid:  User ID
    :return none:
    """
    for i in table.players:
        if i == uid:
            del table.players[i]
            break
