'''
main Program
'''
import sys
import os
import time
import threading as th
import ursina as ur  

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
            0: [(0, 0, -3), (0, 0, 0), (0, 1, -3), (0, 0, 0)],
            1: [(3, 0, -1.5), (0, 275, 0), (3, 1, -1.5), (0, 60, 0)],
            2: [(3, 0, 1.5), (0, 230, 0), (3, 1, 1.5), (0, 120, 0)],
            3: [(0, 0, 3), (0, 180, 0), (0, 1, 3), (0, 180, 0)],
            4: [(-3, 0, 1.5), (0, 0, 0), (-3, 1, 1.5), (0, 240, 0)],
            5: [(-3, 0, -1.5), (0, 300, 0), (-3, 1, -1.5), (0, 300, 0)]
        }
        
    def window(self):
        '''
        create the window
        '''
        self.app = ur.Ursina(icon="../ASSets/rsz_leserunde.ico", window_title="3D Game", development_mode=debug)
        #self.ui = UI()
        
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
        sky = ur.Sky()
        table = ur.Entity(model='cube', scale=(1, 1, 1), color="#000000", position=(0, 0.5, 0))
        tabletop = ur.Entity(model='circle', color="#5C4033", position=(0, 1.1, 0), rotation=(90, 0, 0), scale=(4, 4, 4))
        player = Player(table, self.positions[4])
        floor = ur.Entity(model='plane', scale=(100, 1, 100), color=ur.color.white.tint(-0.2), texture='white_cube', texture_scale=(100, 100), collider='box')
        #enemy = Opponent(position=(3, 1, 0), scale=(1, 2, 1))
        #enemy2 = Opponent(position=(0, 1, 3), scale=(1, 2, 1))
        
        #self.app.icon = "textures/Leserunde.ico"

    def spawn_enemy(self):
        '''
        spawn the enemy
        '''
        for i in range(6):
            enemy = Opponent(position=self.positions[i][0], scale=(1, 2, 1))
            enemy.rotation = self.positions[i][1]
    

main = Main()
main.window()
main.threed()
main.app.run()