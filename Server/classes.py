import random
import threading
import pickle
from operator import invert

from networking import *

DEBUG = True

class Table(threading.Thread):
    def __init__(self):
        super().__init__()
        self.players = {}
        self.card_of_round = None
        self.current_player = 0
        self.player_count = 0
        self.game_started = False
        self.last_player = 0
        self.start_event = threading.Event()
        self.cards_set = []

    def run(self):
        """
        Run the game loop
        """
        if DEBUG: print("Table started")
        self.pregame_loop()

        self.game_started = True
        with self.start_event:
            self.start_event.set()

        self.game_loop()

    def add_player(self, name, skin, conn):
        """
        Add a player to the table
        :param name: Name of the player
        :param skin: Skin of the player
        :param conn: Connection object of the player
        """
        uid = self.generate_uid()
        if uid is None:
            raise SystemError("Problem with UID generation")
        self.players[uid] = {
            "uid": uid,
            "name": name,
            "skin": skin,
            "conn": conn,
            "alive": True,
            "voted": False,
            "cards": [],
            "gun": [False, False, False, False, False, True]
        }
        self.player_count += 1

    def add_player_object(self, player):
        self.players[player["uid"]]["obj"] = player

    def shuffle_deck(self):
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
        self.card_of_round = random.choice(["Ace", "Queen", "King"])

        for player in self.players:
            self.players[player]["cards"] = deck[:5]
            deck = deck[5:]

        #shuffle_done_event.set()

    def increment_player(self):
        """
        Increment the player
        """
        self.last_player = self.current_player
        self.current_player += 1
        while self.current_player is not self.players[self.current_player]["alive"]:
            self.current_player += 1
            if self.current_player == self.player_count:
                self.current_player = 0

    def generate_uid(self):
        """
        Generate a unique user ID
        :return: Unique user ID
        """
        for uid in range(0, 6, 1):
            if uid not in self.players:
                return uid
            return None
        return None

    def pregame_loop(self):
        votes = 0
        old_len = 0
        last_votes = 0


        while len(self.players) < 6 or votes < len(self.players):
            votes = 0
            changes = False

            if old_len != len(self.players):
                old_len = len(self.players)
                changes = True


            for player in self.players:
                if player["voted"]:
                    votes += 1

            if votes != last_votes:
                changes = True
                last_votes = votes

            if changes:
                for player in self.players:
                    player.data_dump()



    def game_loop(self):
        """
        Game loop
        """

        self.shuffle_deck()


        self.players[self.current_player]["obj"].first=True

        for player in self.players:
            player.game_loop()
        #while self.game_started:

        while self.game_started:
            pass

    def liar_handler(self):
        """
        Liar Handler
        """
        self.players[self.current_player]["obj"].now.notify_all()
        self.players[self.current_player]["obj"].gun_handler()

        for card in self.cards_set:
            if card != self.card_of_round or card != "Joker":
                flood_players(f"liar,{self.last_player}")
                self.players[self.last_player]["obj"].gun_handler()
                break

        else:
            flood_players(f"liar,{self.current_player}")
            self.players[self.current_player]["obj"].gun_handler()

        return


class Player(threading.Thread):
    def __init__(self, connection, table, uid, name, skin):
        super().__init__()
        self.table = table
        self.uid = uid
        self.name = name
        self.skin = skin
        self.connection = connection
        self.alive = self.table.players[self.uid]["alive"]
        self.voted = self.table.players[self.uid]["voted"]
        self.cards = self.table.players[self.uid]["cards"]
        self.gun = self.table.players[self.uid]["gun"]
        self.first = False
        self.now = threading.Condition()
        self.cards_set = self.table.cards_set

    def run(self):
        """
        Run the player thread
        """
        if DEBUG: print(f"Player {self.uid} started")
        self.table.add_player_object(self)

        send_message_to_player(self.connection, f"{self.uid}")
        if DEBUG: print(f"Player {uid} has joined the game with name {self.name} and skin {self.skin}")

        self.data_dump()
        if DEBUG: print(f"Informed Player {uid}")

        if DEBUG: print(f"Waiting for game to start")

        while not self.table.start_event.is_set():
            self.sub_thread=threading.Thread(target=self.table.start_event.wait)
            self.sub_thread.start()

            self.table.start_event.wait()

    def game_loop(self):
        """
        Game loop
        """
        if DEBUG: print(f"Game loop started for player {self.uid}")

        if self.first:
            send_message_to_player(self.connection, "first")
            send_message_to_player(self.connection, pickle.dumps(self.table.players[self.uid]["cards"]))
            self.cards_set = receive_message(self.connection).split(",")
            self.cards_set.sort(invert)
            for card in self.cards_set:
                self.cards.pop(card)
            flood_players(len(self.cards_set), self.table, self.uid)
            self.table.increment_player()

        else:
            send_message_to_player(self.connection, self.table.current_player.to_bytes(4, "big"))
            send_message_to_player(self.connection, pickle.dumps(self.table.players[self.uid]["cards"]))


        while True:
            self.now.wait()
            send_message_to_player(self.connection, "now")
            return_data = receive_message(self.connection).decode()
            if return_data == "liar":
                self.table.liar_handler()
            else:
                self.cards_set = return_data.split(",")
                flood_players(self.cards_set, self.table, self.uid)
                self.table.increment_player()

    def vote_handler(self):
        """
        Vote Handler
        """
        while not self.table.start_event.is_set():
            msg = receive_message
            if msg == "True":
                self.table.players[self.uid]["voted"] = True
            elif msg == "False":
                self.table.players[self.uid]["voted"] = False


    def data_dump(self):
        """
        Data Dump
        """
        data = ""
        for i in self.table.players:
            data += f"{i},{self.table.players[i]['name']},{self.table.players[i]['skin']},{self.table.players[i]['voted']};"
        send_message_to_player(self.connection, data)

    def gun_handler(self):
        """
        Gun Handler
        """
        random.shuffle(self.gun)
        if self.gun[0]:
            self.alive = False
            flood_players(f"gun,{self.uid},live", self.table, self.uid)
            return
        else:
            self.gun.pop(0)
            flood_players(f"gun,{self.uid},blank", self.table, self.uid)
            return




class TableManager:
    def __init__(self):
        self.tables = []
        self.active_threads = []

    def get_or_create_table(self):
        """
        Find a non-running table or create a new one.
        """
        for table in self.tables:
            if not table.game_started:
                return table

        # Create a new table if no non-running table is found
        new_table = Table()
        new_table.start()
        self.tables.append(new_table)
        return new_table

    def add_player_to_table(self, name, skin, conn):
        """
        Add a player to a non-running table.
        """
        table = self.get_or_create_table()
        table.add_player(name, skin, conn)
        return table, uid


def remove_player_from_table(table, uid):
    """
    Remove a player from the table
    :param table: table instance to remove the player from
    :param uid:  User ID
    :return none:
    """
    for uid in table:
        del table.players[uid]
