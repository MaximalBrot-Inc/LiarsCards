'''
main Program
'''
import sys
import os
import time
import threading as th
import ursina as ur  

from player import Player
from enemy import Enemy
from network import Network
from ui import UI
debug = True
class Main:
    def window(self):
        self.app = ur.Ursina(icon="../ASSets/rsz_leserunde.ico", window_title="3D Game", development_mode=debug)
        #self.ui = UI()
        
    def input(self, key):
        if key == 'alt':
            exit()
            
    def threed(self):
        #self.ui.start()
        player = Player(position=(0, 0, -3))
        floor = ur.Entity(model='plane', scale=(100, 1, 100), color=ur.color.white.tint(-0.2), texture='white_cube', texture_scale=(100, 100), collider='box')
        enemy = Enemy(position=(3, 1, 0), scale=(1, 2, 1))
        enemy2 = Enemy(position=(0, 1, 3), scale=(1, 2, 1))
        table = ur.Entity(model='cube', scale=(1, 1, 1), color="#000000", position=(0, 0.5, 0))
        tabletop = ur.Entity(model='circle', color="#5C4033", position=(0, 1.1, 0), rotation=(90, 0, 0), scale=(4, 4, 4))
        #self.app.icon = "textures/Leserunde.ico"

    
    

main = Main()
main.window()
main.threed()
main.app.run()