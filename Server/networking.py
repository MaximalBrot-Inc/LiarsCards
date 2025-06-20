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
        except (ConnectionResetError, ConnectionAbortedError, ConnectionError,
                BrokenPipeError, OSError, EOFError):
            print("Connection closed")
            table, uid = None, None
            for arg in args:
                print(arg)
                if hasattr(arg, "table"):
                    print(f"Player {arg} has disconnected")
                    table = arg.table
                    uid = arg.uid
                    break
                elif hasattr(arg, "players"):
                    print(f"Table {arg} has disconnected")
                    table = arg
                    uid = kwargs.get("uid", None)
                    if uid is None:
                        print("No UID provided for player removal.")
                        return None
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
    :type message: str or bytes
    :param table: Server instance
    :type table: class
    :param sender_uid: User ID of the sender
    :type sender_uid: int
    :return: None
    """
    if DEBUG:
        print(f"flooding players with message: {message}")

    if sender_uid is not None:
        # If sender_uid is provided, exclude the sender from the flood
        for uid in table.players:
            if (table.players[uid]["uid"] != sender_uid
                    and table.players[uid]["alive"]):
                if type(message) is not bytes:
                    table.players[uid]["conn"].sendall(message.encode())
                else:
                    table.players[uid]["conn"].sendall(message)
    else:
        # If sender_uid is not provided, send to all players
        for uid in table.players:
            if DEBUG:
                print(f"flooding player {uid} with message: {message}")
            #if table.players[uid]["alive"]:
            if type(message) is not bytes:
                table.players[uid]["conn"].sendall(message.encode())
            else:
                table.players[uid]["conn"].sendall(message)


@connection_closed_handler
def send_message(player, message):
    """
    Send a message to a specific player
    :param player: Player instance
    :type player: class
    :param message: Message to send
    :type message: str or bytes
    :return: None
    """
    if type(message) is not bytes:
        message = message.encode()
    player.connection.sendall(message)


@connection_closed_handler
def receive_message(player, msg_size=MSG_SIZE):
    """
    Receive a message from a player
    :param  player: Player instance
    :type player: class
    :param  msg_size: Size of the message to receive. Defaults to MSG_SIZE (2048).
    :type msg_size: int
    :return: Message received
    """
    message = player.connection.recv(msg_size)
    if DEBUG:
        print(f"rec: {message}")
    if not message:
        print("No message received")
        raise EOFError
    try:
        message = pickle.loads(message)
        if DEBUG:
            print(f"{message} is pickle")
    except pickle.UnpicklingError:
        message = message.decode()
        if DEBUG:
            print(f"{message} is not pickle")
    finally:
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
