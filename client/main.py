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
  
debug = True
class Main(ur.Entity):
    def __init__(self):
        super().__init__()
        '''
        initialize the main class
        '''
        
        self.player_ready = False
        self.positions = {
            0: [(3.5, 0.9, 0.0), (0, -90, 0)],
            1: [(1.75, 0.9, 3.031), (0, 210, 0)],
            2: [(-1.75, 0.9, 3.031), (0, 150, 0)],
            3: [(-3.5, 0.9, 0.0), (0, 90, 0)],
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
        

            
    def threed(self):
        '''
        starts the 3D game
        '''
        #self.Lobby.start()
        #self.network = Network()
        #self.network.connect("127.0.0.1", 8000)
        #uid, lst = self.network.receive()
        
        
        uid = 0
        
        
        lst = [(0, "Player 1", "default"), (1, "Hello world", "hatsune_miku.glb"), (2, "Player 1", "skin1"), (3, "Player 2", "skin2"), (4, "Player 3", "skin3"), (5, "Player 4", "default")]
        
        
        #sky = ur.Sky()
        
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
        
        for i in lst:
            self.spawn_people(i, uid)
        self.ui.text.text = f"{self.ui.count}/{self.ui.max_player}"
        
        #self.app.icon = "textures/Leserunde.ico"
        
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
        if key == 'alt':
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

    def spawn_people(self, player, uid_self):
        '''
        spawn the enemy
        '''
        uid, name, skin = player[0], player[1], player[2]
        self.ui.max_player += 1
        if uid == uid_self:
            self.player = Player(self.positions, uid)
            return
        self.opponent = Opponent(self.positions, uid, skin, scale=(0.5, 0.5, 0.5))
        self.opponent.name_tag.text = name 
        self.positions[uid].append(self.opponent)   
            

        

   
main = Main()
main.window()
main.app.run()