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
        self.positions = {      # pos: [(position), (rotation), (gun_pos), (gun_rot)] of all players
            0: [(0, 1, -3), (0, 0, 0), (0.1, 0.833, -1.4), (0, 0, -90), ur.color.red],
            1: [(0, 1, 3), (0, 180, 0), (-0.1, 0.833, 1.4), (0, 180, -90), ur.color.blue],
            2: [(-3, 1, -1.5), (0, 65, 0), (-1.2, 0.833, -0.75), (0, 65, -90), ur.color.green], 
            3: [(3, 1, 1.5), (0, 245, 0), (1.2, 0.833, 0.7), (0, 240, -90), ur.color.yellow],
            4: [(-3, 1, 1.5), (0, 115, 0), (-1.3, 0.833, 0.55), (0, 117, -90), ur.color.pink],
            5: [(3, 1, -1.5), (0, 295, 0), (1.3, 0.833, -0.55), (0, 297, -90), ur.color.orange]
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
        # self.network = Network()
        # self.network.connect("127.0.0.1", 8000)
        # uid, lst = self.network.receive()
        
        
        uid = 0
        
        
        lst = [(0, "Player 1", "default"), (1, "Hello world", "hatsune_miku.glb"), (2, "Player 1", "default"), (3, "Player 1", "default"), (4, "Player 1", "default"), (5, "Player 1", "default")]
        self.table = ur.Entity(
            model="table",
            position=(0, 0, 0),
            scale=1.5,
            #shader=lit_with_shadows_shader
        )
        
        sky = ur.Sky()
        
        
        #tabletop = ur.Entity(model='circle', color="#5C4033", position=(0, 1.1, 0), rotation=(90, 0, 0), scale=(4, 4, 4))
        floor = ur.Entity(model='plane', 
                        scale=(100, 1, 100), 
                        color=ur.color.white.tint(-0.2), 
                        texture='white_cube', 
                        texture_scale=(100, 100), 
                        collider='box'
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
            self.player.gun_to_head()
            #self.ui.wp.disable()
            #self.ui.text.text = "Ready"
            #self.network.send(True)

    def spawn_people(self, player, uid_self):
        '''
        spawn the enemy
        '''
        uid, name, skin = player[0], player[1], player[2]
        self.ui.max_player += 1
        if skin == "default":
            skin = "sphere"
        if uid == uid_self:
            self.player = Player(self.table, self.positions[uid])
            return
        self.opponent = Opponent(self.table, self.positions[uid], model=skin, scale=(0.5, 0.5, 0.5))
        self.opponent.name_tag.text = name    
            

        

   
main = Main()
main.window()
main.app.run()