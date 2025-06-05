import random
import threading
import pickle
import time

from networking import flood_players, send_message, receive_message


send_delay = 0.1
card_removing_delay = 2.5

DEBUG = True


class Table(threading.Thread):
    def __init__(self):
        """"
        Table class to handle the game logic and player management.
        Thread for game loop and player actions.
        :return: None
        """
        super().__init__(daemon=True)
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
        self.reshuffle_event = threading.Event()

    def run(self):
        """
        The main function of the table thread.
        This function is called when the table thread is started.
        :return: None
        """
        if DEBUG:
            print("Table started")

        self.pregame_loop()

        self.game_started = True

        self.game_loop()

    def add_player(self, name, skin, conn):
        """
        Add a player to the table
        :param name: Name of the player
        :type name: str
        :param skin: Skin of the player
        :type skin: str
        :param conn: Connection object of the player
        :type conn: socket object
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

        if DEBUG:
            print(f"Player {uid} added to table")

        return uid

    def add_player_object(self, player):
        self.players[player.uid]["obj"] = player

    def shuffle_deck(self):
        """
        Shuffle the deck
        :return: None
        """
        deck = self.deck

        if DEBUG:
            print("Shuffling deck")

        if self.player_count == 4:
            while len(deck) < 20:
                if len(deck) < 7:
                    deck.append("Ace")
                elif len(deck) < 13:
                    deck.append("Queen")
                elif len(deck) < 19:
                    deck.append("King")
                else:
                    deck.append("Joker")

        elif self.player_count < 7:
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

        self.reshuffle_event.set()
        time.sleep(0.1)
        self.reshuffle_event.clear()

    def increment_player(self):
        """
        Increment the player
        :return: None
        """
        self.last_player = self.current_player
        self.current_player += 1
        if self.current_player == self.player_count:
            self.current_player = 0

        if DEBUG:
            print(f"Current player: {self.current_player}"
                  f" of {self.player_count-1}")

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
        """
        Function to handle the pregame loop.
        This function is called when the game starts.
        It handles the voting process and the player count.
        :return: None
        """
        old_len = 0
        last_votes = 0

        players = self.players.copy()
        time.sleep(1)
        while True:

            votes = 0
            changes = False

            if old_len != len(players):
                old_len = len(players)
                changes = True

            for uid in players:
                if players[uid]["voted"]:
                    votes += 1

            if votes != last_votes:
                changes = True
                last_votes = votes

            if changes:
                for uid in players:
                    if players[uid]["obj"] is not None:
                        if DEBUG:
                            print(f"Sending update data to player {uid}")

                        players[uid]["obj"].data_dump()

            if votes > 1:
                if 6 == len(players) or len(players) == votes:
                    break
            players = self.players.copy()

    def game_loop(self):
        """
        Main game loop. This function is called when the game starts.
        It handles the game logic and player turns.
        :return: None
        """
        last_player = 0

        self.shuffle_deck()
        alive_players = self.player_count

        self.players[self.current_player]["obj"].first = True

        self.start_event.set()
        players = self.players.copy()

        while self.game_started and alive_players >= 1:
            alive_players = self.player_count
            for uid in players:
                if not self.players[uid]["alive"]:
                    alive_players -= 1
            try:
                if self.current_player != last_player:
                    players[self.current_player]["obj"].now.set()

                    if DEBUG:
                        print(f"Player {self.current_player} turn")

                    players[self.current_player]["obj"].now.clear()
            except KeyError:
                players = self.players.copy()

                if DEBUG:
                    print(f"\n\n\n Key error, "
                          f"{self.current_player} not in players")

                continue

            if self.liar_event.is_set():
                self.liar_event.clear()
                self.liar_handler()

            last_player = self.current_player

            players = self.players.copy()

    def liar_handler(self):
        """
        Function to handle the liar logic.
        If the accused is caught lying, they have to use their gun.
        If the accused is innocent, the caller must use their gun.
        :return :None
        """
        if DEBUG:
            print("Liar handler called")

        data = []

        if DEBUG:
            print(f"{self.players[self.last_player]["cards"]} ")
            print(f"{self.cards_set}")

        for card in self.cards_set:
            if DEBUG:
                print(f"Card {card} is set \n"
                      f" {self.players[self.last_player]["cards"][card]}")

            data.append(self.players[self.last_player]["cards"][card])

        for card in data:
            if card != self.card_of_round and card != "Joker":
                flood_players(f"liar,{self.last_player}", self)

                if DEBUG:
                    print(f"Player {self.last_player} is a liar")

                time.sleep(send_delay)
                flood_players(pickle.dumps(data), self)
                self.players[self.last_player]["obj"].gun_handler()
                break

        else:
            flood_players(f"liar,{self.current_player}", self)

            if DEBUG:
                print(f"Player {self.current_player} is a liar")

            time.sleep(send_delay)
            flood_players(pickle.dumps(data), self)
            self.players[self.current_player]["obj"].gun_handler()

        self.players[self.last_player]["obj"].remove_played_cards()

        if not self.players[self.current_player]["alive"]:
            self.increment_player()

        if DEBUG:
            print(f"Flooding the players with the current player: {self.current_player}")

        time.sleep(card_removing_delay)
        flood_players(f"{self.current_player}", self)
        time.sleep(send_delay)

        self.shuffle_deck()

        return


class Player(threading.Thread):
    def __init__(self, connection, table, uid, name, skin):
        """
        :param connection: Connection object of the player
        :type connection:
        :param table: Object of the table the player is sitting at
        :type table:
        :param uid: User ID of the player on the table
        :type uid:
        :param name: Name of the player
        :type name:
        :param skin: Skin of the player
        :type skin:
        """
        super().__init__(daemon=True)
        self.table = table
        self.uid = uid
        self.name = name
        self.skin = skin
        self.connection = connection
        self.alive = self.table.players[self.uid]["alive"]
        self.voted = self.table.players[self.uid]["voted"]
        self.gun = self.table.players[self.uid]["gun"]
        self.first = False
        self.now = threading.Event()
        self.cards_set = self.table.cards_set
        self.sub_thread = None

    def run(self):
        """
        Function wich executes at the start of the player thread.
        Also contains the pregame loop.
        :return: None
        """
        if DEBUG:
            print(f"Player {self.uid} started")

        self.table.add_player_object(self)

        send_message(self, f"{self.uid}")

        if DEBUG:
            print(f"Player {self.uid} has joined the game"
                  f" with name {self.name} and skin {self.skin}")

        self.data_dump()

        if DEBUG:
            print(f"Informed Player {self.uid}")

        self.table.players[self.uid]["ready"] = True

        if DEBUG:
            print("Waiting for game to start")

        if not self.table.start_event.is_set():
            self.sub_thread = threading.Thread(
                target=self.vote_handler, daemon=True)
            self.sub_thread.start()
            self.sub_thread.name = f"VoteHandler-{self.uid}"

            self.table.start_event.wait()

        self.game_loop()

    def game_loop(self):
        """
        Core game loop for the player thread
        :return: None
        """
        if DEBUG:
            print(f"Game loop started for player {self.uid}"
                  f" with {threading.current_thread()}")

        if self.first:
            send_message(self, f"{self.table.current_player}")
            self.initial_cards()

            if DEBUG:
                print(f"Player {self.uid} is first")

            # Ensure cards are received correctly
            cards_set = receive_message(self)

            if DEBUG:
                print(f"Player {self.uid} sent cards: {cards_set}")

            try:
                self.table.cards_set = list(eval(cards_set))
            except SyntaxError:
                self.table.cards_set = self.table.cards_set.split(",")
                self.table.cards_set = [int(i) for i in self.table.cards_set]
                print(f"Player {self.uid}"
                      f" sent invalid cards: {self.table.cards_set}")

            self.played_cards()

        else:
            if DEBUG:
                print(f"{self.uid} is sleeping")

            send_message(self, f"{self.table.current_player}")
            self.initial_cards()

        self.sub_thread = threading.Thread(
            target=self.shuffle_handler, daemon=True)
        self.sub_thread.start()
        self.sub_thread.name = f"ShuffleHandler-{self.uid}"

        while True:
            self.now.wait()

            if DEBUG:
                print(f"Waiting for player {self.uid} to send cards")
            # send_message_to_player(self, "now")

            return_data = receive_message(self)
            if return_data == "liar":
                self.table.liar_event.set()
                self.now.clear()
            else:
                self.remove_played_cards()

                self.table.cards_set = list(eval(return_data))

                self.played_cards()

    def initial_cards(self):
        """
        Function to send the initial cards to the player.
        :return: None
        """
        if DEBUG:
            print(f"{self.uid} initial cards")

        time.sleep(send_delay)

        if DEBUG:
            print(self.table.players[self.uid]["cards"])
            print(self.table.card_of_round)

        send_message(self, pickle.dumps(self.table.players[self.uid]["cards"]))
        time.sleep(send_delay)
        send_message(self, f"{self.table.card_of_round}")

    def played_cards(self):
        self.table.cards_set.sort(reverse=True)
        flood_players(f"{self.uid}", self.table, self.uid)
        flood_players(f"{len(self.table.cards_set)}", self.table, self.uid)

        if DEBUG:
            print(f"Cards played by {self.uid}: {self.table.cards_set}")

        self.table.increment_player()

    def vote_handler(self):
        """
        Function to handle the voting process, done in a separate thread.
        :return: None
        """
        while not self.table.start_event.is_set():
            msg = receive_message(self, 5)
            if msg == "True":
                self.table.players[self.uid]["voted"] = True
            elif msg == "False":
                self.table.players[self.uid]["voted"] = False
            elif msg == "Start":
                if DEBUG:
                    print(f"closing vote handler for {self.uid}")

                exit()

    def shuffle_handler(self):
        """
        Function to handle the reshuffling of the deck. Player sided.
        Sends the new cards to the player.
        :return: None
        """
        while self.table.game_started:
            self.table.reshuffle_event.wait()
            time.sleep(1)
            send_message(self,
                         pickle.dumps(self.table.players[self.uid]["cards"]))

            if DEBUG:
                print(f"Player {self.uid} now has "
                      f"{self.table.players[self.uid]["cards"]}")

            time.sleep(send_delay)
            send_message(self, f"{self.table.card_of_round}")

            if DEBUG:
                print(f"Card of round is now {self.table.card_of_round}")

    def data_dump(self):
        """
        Function to send the player dict to the client.
        :return: None
        """
        data = ""
        for i in self.table.players:
            data += (f"{i},{self.table.players[i]['name']},"
                     f"{self.table.players[i]['skin']},"
                     f"{self.table.players[i]['voted']};")
        send_message(self, data)

    def gun_handler(self):
        """
        Function to handle the gun logic.
        If the player is shot, the player is set to dead.
        This info is sent to all players.
        """
        self.gun = self.table.players[self.uid]["gun"]
        random.shuffle(self.gun)
        if self.gun[0]:
            self.alive = False
            flood_players(f"gun,{self.uid},live", self.table)

            if DEBUG:
                print(f"Player {self.uid} is dead")

            self.table.players[self.uid]["gun"] = self.gun
            return
        else:
            self.gun.pop(0)
            flood_players(f"gun,{self.uid},blank", self.table)

            if DEBUG:
                print(f"Player {self.uid} is not dead")

            self.table.players[self.uid]["gun"] = self.gun
            return

    def remove_played_cards(self):
        """
        Function to remove the played cards from the players hand.
        :return: None
        """
        for card in self.table.cards_set:
            self.table.players[self.table.last_player]["cards"].pop(card)
        self.table.cards_set = []


class TableManager:
    def __init__(self):
        self.tables = []
        self.active_threads = []

    def get_or_create_table(self):
        """
        Find a non-running table or create a new one.
        :return: A table object
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
        :param name: Name of the player
        :type name: str
        :param skin: Skin of the player
        :type skin: str
        :param conn: Connection object of the player
        :type conn: socket object
        """
        table = self.get_or_create_table()
        uid = table.add_player(name, skin, conn)
        return table, uid
