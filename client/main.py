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
            0: [(0, 0, -3), (0, 0, 0), (0, 1, -3), (0, 0, 0), ur.color.red],
            1: [(0, 0, 3), (0, 180, 0), (0, 1, 3), (0, 180, 0), ur.color.blue],
            2: [(-3, 0, -1.5), (0, 65, 0), (-3, 1, -1.5), (0, 300, 0), ur.color.green], 
            3: [(3, 0, 1.5), (0, 245, 0), (3, 1, 1.5), (0, 120, 0), ur.color.yellow],
            4: [(-3, 0, 1.5), (0, 115, 0), (-3, 1, 1.5), (0, 240, 0), ur.color.pink],
            5: [(3, 0, -1.5), (0, 295, 0), (3, 1, -1.5), (0, 60, 0), ur.color.orange]
        }
        self.index = 0
        
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
        self.network = Network()
        self.network.connect("127.0.0.1", 8000)
        self.network.receive()
        sky = ur.Sky()
        for i in self.positions:
            print(self.positions[i][4])
        table = ur.Entity(
            model="untitled",
            position=(0, 0, 0),
            scale=1.5,
            shader=lit_with_shadows_shader
        )
        #tabletop = ur.Entity(model='circle', color="#5C4033", position=(0, 1.1, 0), rotation=(90, 0, 0), scale=(4, 4, 4))
        player = Player(table, self.positions[3])
        floor = ur.Entity(model='plane', scale=(100, 1, 100), color=ur.color.white.tint(-0.2), texture='white_cube', texture_scale=(100, 100), collider='box')

        
        #self.app.icon = "textures/Leserunde.ico"
        ur.invoke(self.spawn_enemy, delay=2)

    def spawn_enemy(self):
        '''
        spawn the enemy
        '''
        i = self.index
        if i == len(self.positions):
            return
        enemy = Opponent(position=self.positions[i][0], scale=(0.5, 0.5, 0.5), rotation = self.positions[i][1])
        self.index += 1
        #ur.invoke(self.spawn_enemy, delay=1)
        self.spawn_enemy()
    

main = Main()
main.window()
main.app.run()