"""
Main Programm for the Server
"""
import socket
import threading

from networking import *
from classes import *

PORT = 8000



Server = socket.create_server(("0.0.0.0", PORT))

# Im Hauptprogramm
table_manager = TableManager()

while True:
    try:
        connection, address = Server.accept()

        name, skin = connection.recv(MSG_SIZE).decode().split(",")  # Spielerinformationen empfangen

        # Add player to table
        table, uid = table_manager.add_player_to_table(name, skin, connection)
        print(f"Player {connection} joined table {table}")
        # Start player thread
        player = Player(connection, table, uid, name, skin)
        player.start()
        # Add player to active threads
        table_manager.active_threads.append(player)


    except (KeyboardInterrupt, ConnectionResetError, ConnectionError):
        print("Server is shutting down...")
        Server.close()
        break

