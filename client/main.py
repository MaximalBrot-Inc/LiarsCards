'''
main Program
'''
import sys
import os
import time
import threading as th
import ursina as ur  
from ursina.shaders import lit_with_shadows_shader
import shutil  # Add this import
import math

from player import Player
from opponent import Opponent
from network import Network
from ui import UI
from lobby import Lobby


# delete model_compressed folder
models_compressed_path = os.path.join("Client", "models_compressed")
if os.path.exists(models_compressed_path):
    print("Deleting models_compressed folder")
    for i in range(10):
        print(" ")
    shutil.rmtree(models_compressed_path)  # Use shutil.rmtree instead of os.system
  
debug = False
class Main(ur.Entity):
    def __init__(self):
        super().__init__()
        '''
        initialize the main class
        '''
        
        self.player_ready = False
        self.positions = {
            0: [(3.5, 0.9, 0.0), (0, -90, 0)],
            1: [(-3.5, 0.9, 0.0), (0, 90, 0)],
            2: [(1.75, 0.9, 3.031), (0, 210, 0)],
            3: [(-1.75, 0.9, 3.031), (0, 150, 0)],
            4: [(-1.75, 0.9, -3.031), (0, 30, 0)],
            5: [(1.75, 0.9, -3.031), (0, 330, 0)]
        }

        
    def window(self):
        '''
        create the window
        '''
        self.app = ur.Ursina(icon="rsz_leserunde.ico", window_title="3D Game", development_mode=debug)
        width, height = ur.window.size
        
        gcd = math.gcd(int(width), int(height))

        self.aspect_ratio = (width // gcd, height // gcd)
        if self.aspect_ratio == (8, 5):
            self.aspect_ratio = (16, 10)
        

        #self.ui = UI()
        self.threed()
        
    def input_shi(self, var=True):
        if var:
            server = input("Enter server ip: ")
            port = input("Enter server port: ")
            name = input("Enter your name: ")
            skin = input("Enter your skin: ")
            return server, int(port), name + skin
        else:
            return "127.0.0.1", 8000, "Play with my balls,skin2"
            return "10.5.5.58", 8000, "Play with my balls,skin2"
            
    def threed(self):
        '''
        starts the 3D game
        '''
        #self.Lobby.start()
        # self.network = Network()
        # var = False
        # server, port, name = self.input_shi(var)
        # self.network.connect(server, port)
        # self.network.send(name)
        # self.uid, self.lst = self.network.receive_first()
        
        
        self.uid = 0
        
        
        self.lst = [(0, "Player 1", "default", False), (1, "Hello world", "hatsune_miku.glb", False), (2, "Player 1", "skin1", False), (3, "Player 2", "skin2", False), (4, "Player 3", "skin3", False), (5, "Player 4", "default", False)]  # Uncomment and update lst
        
        
        #sky = ur.Sky()
        self.uid = int(self.uid)
        self.table = ur.Entity(
            model="table",
            position=(0, 0, 0),
            scale=(1.75, 1.5, 1.75),
            #shader=lit_with_shadows_shader
            )
        
        # floor = ur.Entity(model='plane', 
        #                 scale=(100, 1, 100), 
        #                 color=ur.color.white.tint(-0.2), 
        #                 texture='white_cube', 
        #                 texture_scale=(100, 100), 
        #                 collider='box'
        #                 )
        room = ur.Entity(model="room.glb", 
                        scale=1, 
                        position=(0, 0, 0), 
                        shader=lit_with_shadows_shader,
                        ) 
        
        god = ur.Entity(model='hatsune_miku',  
                        scale=200,
                        color=ur.color.white.tint(-0.2), 
                        collider='box', 
                        position=(0, 300, -300), 
                        rotation=(-90, -180, 0), 
                        shader=lit_with_shadows_shader
                        )
        
        
        self.ui = UI(ur.camera.ui)
        x = 0.55 if self.aspect_ratio == (16, 10) else 0.65
        self.ui.wp.position = (x, -0.35)
        
        self.ui.text.text = f"{self.ui.count}/{self.ui.max_player}"
        
        self.app.icon = "textures/Leserunde.ico"
        for i in self.lst:
            self.spawn_people(i)
        #th.Thread(target=self.wait, daemon=True).start()
        self.player.dead()
        
    def is_ready(self):
        if self.player_ready:
            self.ui.count -= 1
            self.player_ready = False
            #self.ui.wp.enable()
            #self.ui.text.text = "Not ready"
            #self.network.send(False)
        else:
            self.ui.count += 1
            self.player_ready = True
        self.ui.text.text = f"{self.ui.count}/{self.ui.max_player}"
        #self.network.send(self.player_ready)
    
            
    def input(self, key):
        '''
        handle the inputs
        '''
        if key == 'control':
            self.network.disconnect()
            exit()
            
        if key == "f3":
            '''
            ready up
            '''
            self.is_ready()
            #self.ui.wp.disable()
            #self.ui.text.text = "Ready"
            #self.network.send(True)
            
        # if key == "space":
        #     '''
        #     weapon to head
        #     '''
        #     self.player.gun.gun_to_head()
        #     for i in self.positions.values():
        #         for j in i:
        #             if isinstance(j, Opponent):
        #                 if j.visible_self:
        #                     j.gun.gun_to_head()
            
        # if key == "control":
        #     '''
        #     reset gun
        #     '''
        #     self.player.gun.reset()
        #     for i in self.positions.values():
        #         for j in i:
        #             if isinstance(j, Opponent):
        #                 j.gun.reset()

    def spawn_people(self, player):
        '''
        spawn the enemy
        '''
        print(player)
        uid, name, skin = player[0], player[1], player[2]
        self.ui.max_player += 1
        uid = int(uid)
        if uid == self.uid:
            self.player = Player(self.positions, uid)
            return
        self.opponent = Opponent(self.positions, uid, skin, scale=(0.5, 0.5, 0.5))
        self.opponent.name_tag.text = name 
        self.positions[uid].append(self.opponent)  
        
    def wait(self): 
        dic = self.network.pre_game()
        if dic == "first":
            self.ui.wp.disable()
        elif dic == "sleep":
            self.ui.wp.disable()
        else:
            for i in dic:
                if i != "":
                    uid, name, skin = i.split(",")
                    uid = int(uid)
                    if uid != self.uid:
                        self.spawn_people((uid, name, skin))
                        self.ui.text.text = f"{self.ui.count}/{self.ui.max_player}"
    
    def game_start(self):
        cards = self.network.recv()
        
        
    
    '''
    send indexes of cards picked by player 
    server sends amount of cards picked by player to everyone. Place cards in the middle of the table and delete them from opponents hands
        player gets 'now' when its his turn
    player gets prompt to call liar or place new cards
    '''  
    
        

   
main = Main()
main.window()
main.app.run()