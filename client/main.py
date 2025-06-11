'''
main Program
'''
import sys
import os
import time
import threading as th
import ursina as ur  
from ursina.shaders import lit_with_shadows_shader, basic_lighting_shader, normals_shader, unlit_shader, colored_lights_shader
import shutil  # Add this import
import math
import keyboard as kb
from ursina.prefabs.splash_screen import SplashScreen
from ursina.prefabs.first_person_controller import FirstPersonController


from player import Player
from opponent import Opponent
from network import Network
from ui import UI
from lobby import Lobby




# delete model_compressed folder
# models_compressed_path = os.path.join("Client", "models_compressed")
# if os.path.exists(models_compressed_path):
#     print("Deleting models_compressed folder")
#     for i in range(10):
#         print(" ")
#     shutil.rmtree(models_compressed_path)  # Use shutil.rmtree instead of os.system
    
# thread = th.Thread(target=os.system,args=("start cmd.exe /K py C:/Users/Melvin/Desktop/programming/Python/LiarsCards/server/main.py",), daemon=True).start()
# time.sleep(1)
debug = True
class Main(ur.Entity):
    def __init__(self):
        super().__init__()
        '''
        initialize the main class
        '''
        self.state = False
        self.player_ready = False
        self.current_player = -1
        self.opponents = []
        self.positions = {
            0: [(3.5, 0.9, 0.0), (0, -90, 0), "not used" ],
            1: [(-3.5, 0.9, 0.0), (0, 90, 0), "not used"],
            2: [(1.75, 0.9, 3.031), (0, 210, 0), "not used"],
            3: [(-1.75, 0.9, 3.031), (0, 150, 0), "not used"],
            4: [(-1.75, 0.9, -3.031), (0, 30, 0), "not used"],
            5: [(1.75, 0.9, -3.031), (0, 330, 0), "not used"]
        }
        self.cards_width = 0.1
        self.cards_dropped_amount = 0
        self.cards_dropped = 0
        self.current_state = "lobby"
        self.fault = False
        
    def window(self):
        '''
        create the window
        '''
        self.readyy = False
        self.app = ur.Ursina(icon="rsz_leserunde.ico", window_title="3D Game", development_mode=debug)

        # ur.light = ur.DirectionalLight(shadows=False, color=ur.color.white.tint(-0.8))
        # ur.light.look_at(ur.Vec3(0, -1, 0))        
        width, height = ur.window.size
        
        gcd = math.gcd(int(width), int(height))

        self.aspect_ratio = (width // gcd, height // gcd)
        if self.aspect_ratio == (8, 5):
            self.aspect_ratio = (16, 10)
        # self.threed()
        # return
        self.lobby = Lobby()
        self.entities_copy = ur.scene.entities[:]
        
        self.lobby.start_button.on_click = self.start
        th.Thread(target=self.widgets, daemon=True).start()
        
        
    def start(self):
        self.start_round = True
        self.lobby.exit = True
        for entity in self.entities_copy:
            ur.destroy(entity)
        ur.light = ur.DirectionalLight(shadows=False, color=ur.color.white.tint(-0.8))
        ur.light.look_at(ur.Vec3(0, -1, 0)) 
        self.lobby.start_button.hovered = False
        th.Thread(target=self.ready).start()
                
    def ready(self):
        while not self.readyy:
            SplashScreen()
            time.sleep(0.1)
        self.threed()
        
    def input_shi(self):
        server = self.lobby.server_ip.text
        port = self.lobby.server_port.text
        name = self.lobby.name.text
        skin = self.lobby.Dropdown.get_selected()
        
        if skin == None:
            skin = "default"
        skin = skin.replace(" ", "").lower()
        
        if server == "":
            server = "127.0.0.1"
        
        if port == "":
            port = 8000
        
        if name == "":
            name = "Player1"

        return server, int(port), name + "," + skin


        # self.uid = 0


        # self.lst = [(0, "Player 1", "default", False), (1, "Hello world", "hatsune_miku.glb", False), (2, "Player 1", "skin1", False), (3, "Player 2", "skin2", False), (4, "Player 3", "skin3", False), (5, "Player 4", "default", False)]  # Uncomment and update lst
    def widgets(self):
        #sky = ur.Sky()
        self.lamp = ur.Entity(
            model='Lamp.glb',
            color=ur.color.light_gray,
            position=(0, 3, 0),
            scale=2,
            visible=False,
            #shader=lit_with_shadows_shader
        )
        
        self.table = ur.Entity(
            model="table.glb",
            position=(0, 0, 0),
            scale=(1.75, 1.5, 1.75),
            input=self.input,
            #shader=lit_with_shadows_shader
            visible=False,

        )
        

        self.room = ur.Entity(model="room.glb", 
                        scale=1, 
                        position=(0, 0, 0), 
                        #shader=unlit_shader,
                        visible=False,

        ) 
        
        self.god = ur.Entity(model='hatsune_miku',  
                        scale=200,
                        color=ur.color.white.tint(-0.2), 
                        position=(0, 300, -300), 
                        rotation=(-90, -180, 0),
                        visible=False,
                        shader=unlit_shader
        )
        
        
        #lamp_verankerung = ur.Entity(model=)
        self.readyy = True
        print("ready")
        
        
        
    def threed(self):
        '''
        starts the 3D game
        '''
        self.lamp.visible = True
        self.table.visible = True
        self.god.visible = True
        self.room.visible = True
        
        self.network = Network()
        server, port, name = self.input_shi()
        self.network.connect(server, port)
        self.network.send(name)
        self.uid, self.lst = self.network.receive_first()
        
        
        lamp_light = ur.AmbientLight(parent=self.lamp, shadows=False, color=ur.color.white.tint(-0.7), y=0.21, scale=(0.1, 0.1, 0.1))
        lamp_light.look_at(ur.Vec3(0, -1, 0))
        lamp_light = ur.AmbientLight(parent=self.lamp, shadows=False, color=ur.color.brown.tint(-0.6), y=0.21, scale=(0.1, 0.1, 0.1))
        lamp_light.look_at(ur.Vec3(0, -1, 0))
        # lamp_light = ur.AmbientLight(parent=lamp, shadows=False, color=ur.color.yellow.tint(-0.95), y=0.21, scale=(0.1, 0.1, 0.1))
        # lamp_light.look_at(ur.Vec3(0, -1, 0))
        
        
        #ent = ur.Entity(parent=lamp, model="cube", position=(0, -1, 0))
        
        self.ui = UI(ur.camera.ui)
        self.uid = int(self.uid)
        x = 0.55 if self.aspect_ratio == (16, 10) else 0.65
        self.ui.wp.position = (x, -0.35)
        
        self.ui.text.text = f"{self.ui.count}/{self.ui.max_player}"
        
        self.app.icon = "textures/Leserunde.ico"
        for i in self.lst:
            self.spawn_people(i)
        th.Thread(target=self.wait, daemon=True).start()
        #ur.invoke(kb.press_and_release, "alt+tab", delay=0.5)
        ur.invoke(self.is_ready, delay=3)
        
        
    def is_ready(self):
        if self.player_ready:
            self.ui.count -= 1
            self.player_ready = False
            #self.ui.wp.enable()
        else:
            self.ui.count += 1
            self.player_ready = True
        self.ui.text.text = f"{self.ui.count}/{self.ui.max_player}"
        self.network.send(str(self.player_ready))
    
            
    def input(self, key):
        '''
        handle the inputs
        '''
        # print("key: ", key)
        # print("state: ", self.state)
        # print("current state: ", self.current_state)
        if key == 'control':
            try:
                self.network.disconnect()
            except AttributeError:
                print("Network not initialized")
            os.system("taskkill /F /IM cmd.exe")
            os.system("taskkill /F /IM python.exe")         
            exit()
              
        if (key == "f3" or key == "3") and self.current_state == "pre_game":
            '''
            ready up
            '''
            self.is_ready()
        
        if key == "enter" and self.lobby.start_button.hovered and self.current_state == "lobby":
            '''
            exit the lobby
            '''
            self.start()

        if key == "left arrow" and self.state and self.current_state == "game":
            '''
            select cards
            '''
            self.player.select_cards(-1)
        
        if key == "right arrow" and self.state and self.current_state == "game":
            '''
            select cards
            '''
            self.player.select_cards(+1)

        if key == "enter" and self.state and self.current_state == "game":
            '''
            pick card
            '''
            self.player.pick_card()

        if key == "e" and self.state and self.current_state == "game":
            '''
            throw cards
            '''
            self.throw_cards()

        if key == "space" and self.state and self.current_state == "game":
            '''
            LIAR
            '''
            if len(self.table.children) > 0:
                self.network.send("liar")
            
        if key == "ö":
            '''
            weapon to head
            '''
            self.player.gun.gun_to_head()
            for i in self.positions.values():
                for j in i:
                    if isinstance(j, Opponent):
                        if j.visible_self:
                            j.gun.gun_to_head()
            
        if key == "ü":
            '''
            reset gun
            '''
            self.player.gun.reset()
            for i in self.positions.values():
                for j in i:
                    if isinstance(j, Opponent):
                        j.gun.reset()
        

    def spawn_people(self, player):
        '''
        spawn the enemy
        '''
        print(player)
        uid, name, skin = player[0], player[1], player[2]
        self.ui.max_player += 1
        uid = int(uid)
        
        if uid == self.uid:
            self.player = Player(self.positions, uid, self.table)
            self.ui.text.text = f"{self.ui.count}/{self.ui.max_player}"
            self.opponents.append(self.player)
            self.positions[uid][2] = self.player 
            self.player.position = self.positions[uid][0]+(0, -0.7, 0)
            return
        
        self.opponent = Opponent(self.positions, uid, skin, self.table, scale=(0.5, 0.5, 0.5))
        self.opponents.append(self.opponent)
        self.opponent.name_tag.text = name 
        self.positions[uid][2] = self.opponent
        self.opponent.name_tag.text = name
        
    def wait(self): 
        self.current_state = "pre_game"
        while True:
            dic = self.network.pre_game()
            self.ui.count = 0
            if type(dic) == int:
                self.ui.wp.disable()
                self.game_start(dic)
                break
            else:
                for i in dic:
                    if i != "":
                        uid, name, skin, ready = i[0], i[1], i[2], i[3]
                        uid = int(uid)
                        self.ui.count += 1 if ready == "True" else 0
                        if uid != self.uid and self.positions[uid][2] == "not used":
                            self.spawn_people((uid, name, skin))
                self.ui.text.text = f"{self.ui.count}/{self.ui.max_player}"
    
    def game_start(self, dic):
        
        if not self.fault:
            self.network.send("Start")
            '''
            Send the start signal to the network just the first time
            '''
        self.fault = True
        cards = self.network.recv_cards()
        cards.reverse()
        self.current_state = "game"
        if dic == self.uid:
            state = True
        else:
            state = False
        self.state = state

        for seating in self.positions.values():
            if seating[2] == "not used":
                continue
            seating[2].spawn_cards(cards)
        print(cards)
        print(state)
        self.show_tablecard()
        self.game_loop()
        
    def game_loop(self):
        while  True:
            print("WAITING TO RECEIVE")
            last_player = self.network.recv()
            self.fault = True
            if last_player.startswith("liar"):
                liar, uid = last_player.split(",")
                self.liar(uid)          
                break
            last_player = int(last_player)
            
            print("last player: ", last_player)
            self.current_player = last_player + 1
            if self.current_player == len(self.opponents):
                self.current_player = 0
            self.recv = self.network.recv()
            self.delete_cards()      
            print("recv: ", self.recv)  
            print("current player: ", self.current_player)
            print("uid: ", self.uid)    
            
            self.recv = int(self.recv)
            self.cards_dropped_amount = self.recv
            self.cards_dropped = 0
            print("cards dropped amount: ", self.cards_dropped_amount)
            print("cards dropped: ", self.cards_dropped)
            #print("cards: ", self.opponents[self.current_player].cards)
            print("len of list", len(self.opponents[last_player].cards))
            print("picked cards: ", self.opponents[last_player].cards)

            for i in range(self.cards_dropped_amount):
                card = self.opponents[last_player].cards[-1]
                print("picked card: ", card[1]) 
                self.opponents[last_player].cards.remove(card)  
                card[0].throw_cards_on_table(self.cards_dropped_amount, self.cards_dropped)
                
                
                
                if self.cards_dropped == self.cards_dropped_amount:
                    break
                self.cards_dropped += 1
                    
                
            if self.current_player == self.uid:
                self.state = True
                self.player.select_cards(0)
                print("EXITING SELECT CARDS")
                #self.state = False
                    
    def reveal_cards(self, cards):
        '''
        reveal the cards on the table
        '''

        for i, child in enumerate(self.table.children):
            child.reveal_card(cards[i])


    def liar(self, uid):
        cards = self.network.recv()
        str = self.network.recv()
        print("Receive in liar: ", str)
        print("cards: ", cards)
        gun, uid, bullet = str.split(",")
        self.reveal_cards(cards)
        self.opponents[int(uid)].gun.gun_to_head()
        time.sleep(2)
        if bullet == "live":
            self.opponents[int(uid)].gun.shoot()
            self.opponents.remove(self.opponents[int(uid)])
        self.opponents[int(uid)].gun.reset()
        self.delete_cards(all=True)
        print("cards deleted")
        uid = self.network.recv()
        print("uid: ", uid)
        self.game_start(int(uid))

    def delete_cards(self, all=False):
        '''
        delete cards from the player's hand
        '''
        print("Deleting cards")
        print(self.table.children)
        
        if all:
            for i in self.opponents:
                for j in i.cards:
                    try:
                        j[0].mover.update = None
                    except AttributeError:
                        pass
                    ur.destroy(j[0])

        for i in self.table.children:
            try:
                i.mover.update = None
            except AttributeError:
                pass
            ur.destroy(i)


    def throw_cards(self):
        '''
        throw cards on the table
        '''
        self.cards_dropped = 0
        self.cards_dropped_amount = 0
        p = []
        picked_cards = "["
        for i in self.player.cards:
            if i[0].locked == "locked":
                picked_cards += str(self.player.cards.index(i)) + ","
                self.cards_dropped_amount += 1
        if self.cards_dropped_amount == 0:
            return
        self.delete_cards()
        for i in self.player.cards:
            if i[0].locked == "locked":
                self.cards_dropped += 1  
                i[0].throw_cards_on_table(self.cards_dropped_amount, self.cards_dropped)
                p.append(i)
        for i in p:
            self.player.cards.remove(i)
        
        if picked_cards:
            picked_cards = picked_cards[:-1] + "]"
        print("picked cards: ", picked_cards)
        self.network.send(picked_cards)
        self.state = False
        #th.Thread(target=self.game_loop).start()

    
    def show_tablecard(self):
        '''
        show the card round
        '''
        print("wait for table card")
        card = self.network.recv()
        print(f"Table card: {card}")
        self.tablecard = ur.Entity(model=f"{card}.glb", position=(0, 2.5, 0), scale=8, color=ur.color.white.tint(-0.2), shader=unlit_shader, rotation_x=90)
        self.mover = ur.Entity(update=self.move_card)
        
        self.rot_to_achieve = 360
        self.condition = 1.0

    def move_card(self):
        '''
        move the card to the table
        '''   
        self.tablecard.rotation_y += 90 * ur.time.dt
        if self.tablecard.rotation_y >= self.rot_to_achieve:
            self.tablecard.rotation_y = self.rot_to_achieve
            ur.destroy(self.mover)
            self.mover = None
            if self.state:
                self.player.select_cards(0)
            self.tablecard.parent = ur.camera.ui
            self.tablecard.position = (0, 0)
            # Make the card look at the camera/player
            self.tablecard.look_at(ur.camera)
            # Optionally, adjust rotation_x if needed for correct facing
            self.tablecard.rotation_x = -90
            return

    '''
    send indexes of cards picked by player
    server sends amount of cards picked by player to everyone. Place cards in the middle of the table and delete them from opponents hands
        player gets 'now' when its his turn
    player gets prompt to call liar or place new cards
    '''  
    
        

   
main = Main()
main.window()
main.app.run()