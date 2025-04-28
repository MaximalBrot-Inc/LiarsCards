import random
import threading
import pickle
import time
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
        self.deck = []
        self.liar_event = threading.Event()

    def run(self):
        """
        Run the game loop
        """
        if DEBUG: print("Table started")
        self.pregame_loop()

        self.game_started = True
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
            "gun": [False, False, False, False, False, True],
            "obj": None
        }
        self.player_count += 1
        if DEBUG: print(f"Player {uid} added to table")

        return uid

    def add_player_object(self, player):
        self.players[player.uid]["obj"] = player

    def shuffle_deck(self):
        """
        Shuffle the deck
        """
        deck = self.deck

        if DEBUG: print("Shuffling deck")


        if self.player_count < 7:
            while len(deck) < 30:
                if len(deck) < 9:
                    deck.append("Ace")
                elif len(deck) < 18:
                    deck.append("Queen")
                elif len(deck) < 27:
                    deck.append("King")
                else:
                    deck.append("Joker")
        else:
            raise PermissionError("Not enough players / Not implemented yet")

        random.shuffle(deck)
        random.shuffle(deck)
        self.card_of_round = random.choice(["Ace", "Queen", "King"])

        for uid in self.players:
            self.players[uid]["cards"] = deck[:5]
            deck = deck[5:]
            self.players[uid]["obj"].reshuffle.set()

        #shuffle_done_event.set()

    def increment_player(self):
        """
        Increment the player
        """
        self.last_player = self.current_player
        self.current_player += 1
        while not self.players[self.current_player]["alive"]:
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

    def pregame_loop(self):
        votes = 0
        old_len = 0
        last_votes = 0

        while 6 > len(self.players) != votes:
            try:
                votes = 0
                changes = False

                if old_len != len(self.players):
                    old_len = len(self.players)
                    changes = True

                for uid in self.players:
                    if self.players[uid]["voted"]:
                        votes += 1

                if votes != last_votes:
                    changes = True
                    last_votes = votes

                if changes:
                    for uid in self.players:
                        if self.players[uid]["obj"] is not None:
                            if DEBUG: print(f"Sending update data to player {uid}")
                            self.players[uid]["obj"].data_dump()

            except RuntimeError as e:
                if DEBUG: print("RuntimeError in pregame loop :", e)
                pass

    def game_loop(self):
        """
        Game loop
        """

        self.shuffle_deck()
        alive_players = self.player_count

        self.players[self.current_player]["obj"].first = True

        for uid in self.players:
            self.players[uid]["obj"].game_loop()
        #while self.game_started:

        while self.game_started and alive_players >= 1:
            alive_players = self.player_count
            for uid in self.players:
                if not self.players[uid]["alive"]:
                    alive_players -= 1

            if self.liar_event.is_set():
                self.liar_event.clear()
                self.liar_handler()

    def liar_handler(self):
        """
        Liar Handler
        """
        for card in self.cards_set:
            if card != self.card_of_round and card != "Joker":
                flood_players(f"liar,{self.last_player}", self)
                self.players[self.last_player]["obj"].gun_handler()
                break

        else:
            flood_players(f"liar,{self.current_player}", self)
            self.players[self.current_player]["obj"].gun_handler()

        self.shuffle_deck()

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
        self.reshuffle = threading.Event()
        self.sub_thread = None

    def run(self):
        """
        Run the player thread
        """
        if DEBUG: print(f"Player {self.uid} started")
        self.table.add_player_object(self)

        send_message_to_player(self, f"{self.uid}")
        if DEBUG: print(f"Player {self.uid} has joined the game with name {self.name} and skin {self.skin}")

        self.data_dump()
        if DEBUG: print(f"Informed Player {self.uid}")

        self.table.players[self.uid]["ready"] = True

        if DEBUG: print(f"Waiting for game to start")

        while not self.table.start_event.is_set():
            self.sub_thread = threading.Thread(target=self.vote_handler)
            self.sub_thread.start()

            self.table.start_event.wait()

    def game_loop(self):
        """
        Game loop
        """
        if DEBUG: print(f"Game loop started for player {self.uid}")

        if self.first:
            send_message_to_player(self, "first")
            time.sleep(0.01)
            send_message_to_player(self, pickle.dumps(self.table.players[self.uid]["cards"]))
            self.cards_set = receive_message(self).split(",")
            self.cards_set.sort(invert)
            for card in self.cards_set:
                self.cards.pop(card)
            flood_players(f"{len(self.cards_set)}", self.table, self.uid)
            self.table.increment_player()

        else:
            send_message_to_player(self, "sleep")
            time.sleep(0.01)
            send_message_to_player(self, pickle.dumps(self.table.players[self.uid]["cards"]))

        self.subthread = threading.Thread(target=self.shuffle_handler)
        self.subthread.start()

        while True:
            self.now.wait()
            send_message_to_player(self, "now")
            return_data = receive_message(self)
            if return_data == "liar":
                self.table.liar_event.set()
            else:
                self.cards_set = return_data.split(",")
                flood_players(self.cards_set, self.table, self.uid)
                self.table.increment_player()

    def vote_handler(self):
        """
        Vote Handler
        """
        while not self.table.start_event.is_set():
            msg = receive_message(self)
            if msg == "True":
                self.table.players[self.uid]["voted"] = True
            elif msg == "False":
                self.table.players[self.uid]["voted"] = False

    def shuffle_handler(self):
        """
        Shuffle Handler
        """
        self.reshuffle.wait()
        self.reshuffle.clear()
        send_message_to_player(self, pickle.dumps(self.table.players[self.uid]["cards"]))


    def data_dump(self):
        """
        Data Dump
        """
        data = ""
        for i in self.table.players:
            data += f"{i},{self.table.players[i]['name']},{self.table.players[i]['skin']},{self.table.players[i]['voted']};"
        send_message_to_player(self, data)

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
        uid = table.add_player(name, skin, conn)
        return table, uid