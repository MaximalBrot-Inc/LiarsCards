"""
Main Programm for the Server
"""
import socket
import threading
import time


from networking import MSG_SIZE
from classes import Player, TableManager

PORT = 8000

Server = socket.create_server(("0.0.0.0", PORT))

print("Server started on port " + str(PORT))

connection_thread = None
running = True

# Create a table manager instance
table_manager = TableManager()


def await_connections():
    """
    Handle incoming connections and makes it possible to quit the server.
    :return: None
    """
    while running:
        try:
            connection, address = Server.accept()

            # Get the player name and skin from the client
            name, skin = connection.recv(MSG_SIZE).decode().split(",")

            # Add player to table
            table, uid = table_manager.add_player_to_table(name, skin,
                                                           connection)
            print(f"Player {connection} joined table {table}")
            # Start player thread
            time.sleep(0.01)
            player = Player(connection, table, uid, name, skin)
            player.start()
            # Add player to active threads
            table_manager.active_threads.append(player)

        except (KeyboardInterrupt, ConnectionResetError, ConnectionError):
            print("Server is shutting down...")
            Server.close()
            break


if __name__ == "__main__":
    try:
        while True:
            if connection_thread is None:
                # Start the connection thread
                connection_thread = threading.Thread(
                    target=await_connections, daemon=True)
                connection_thread.start()

    except KeyboardInterrupt:
        running = False

        print("Server is shutting down...")
        Server.close()
