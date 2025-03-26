'''
main Program
'''
import sys
import os
import time
import threading as th
import ursina as ur  
from ursina.shaders import lit_with_shadows_shader

from player import Player
from opponent import Opponent
from network import Network
from ui import UI
debug = True
class Main:
    def __init__(self):
        '''
        initialize the main class
        '''
        self.positions = {      # pos: [(position), (rotation), (gun_pos), (gun_rot)] of opponents
            0: [(0, 0, -3), (0, 0, 0), (0.1, 0.833, -1.4), (0, 0, -90), ur.color.red],
            1: [(0, 0, 3), (0, 180, 0), (-0.1, 0.833, 1.4), (0, 180, -90), ur.color.blue],
            2: [(-3, 0, -1.5), (0, 65, 0), (-1.2, 0.833, -0.75), (0, 65, -90), ur.color.green], 
            3: [(3, 0, 1.5), (0, 245, 0), (1, 0.833, 0.5), (0, 240, -90), ur.color.yellow],
            4: [(-3, 0, 1.5), (0, 115, 0), (-1, 0.833, 0.5), (0, 117, -90), ur.color.pink],
            5: [(3, 0, -1.5), (0, 295, 0), (1, 0.833, -0.5), (0, 297, -90), ur.color.orange]
        }
        
    def window(self):
        '''
        create the window
        '''
        self.app = ur.Ursina(icon="rsz_leserunde.ico", window_title="3D Game", development_mode=debug)
        #self.ui = UI()
        self.threed()
        
    def input(self, key):
        '''
        handle the inputs
        '''
        if key == 'alt':
            exit()
            
    def threed(self):
        '''
        starts the 3D game
        '''
        #self.ui.start()
        # self.network = Network()
        # self.network.connect("127.0.0.1", 8000)
        # uid, lst = self.network.receive()
        uid = 2
        lst = [(0, "Player 1", "default"), (1, "Hello world", "hatsune_miku.glb"), (2, "Player 1", "default"), (3, "Player 1", "default"), (4, "Player 1", "default"), (5, "Player 1", "default")]
        self.table = ur.Entity(
            model="untitled",
            position=(0, 0, 0),
            scale=1.5,
            shader=lit_with_shadows_shader
        )
        for i in lst:
            self.spawn_people(i, uid)
        sky = ur.Sky()
        
        
        #tabletop = ur.Entity(model='circle', color="#5C4033", position=(0, 1.1, 0), rotation=(90, 0, 0), scale=(4, 4, 4))
        floor = ur.Entity(model='plane', scale=(100, 1, 100), color=ur.color.white.tint(-0.2), texture='white_cube', texture_scale=(100, 100), collider='box')

        
        #self.app.icon = "textures/Leserunde.ico"

    def spawn_people(self, player, uid_self):
        '''
        spawn the enemy
        '''
        uid, name, skin = player[0], player[1], player[2]
        if skin == "default":
            skin = "cube"
        if uid == uid_self:
            self.player = Player(self.table, self.positions[uid])
            return
        self.enemy = Opponent(self.table, self.positions[uid], model=skin, position=self.positions[uid][0], scale=(0.5, 0.5, 0.5), rotation = self.positions[uid][1])
        #ur.invoke(self.spawn_enemy, delay=1)
    
main = Main()
main.window()
main.app.run()