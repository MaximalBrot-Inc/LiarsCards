'''
main Program
'''
import sys
import os
import time
from network import Network
import ursina as ur  # Ensure the 'ursina' module is installed
from player import Player
from enemy import Enemy
import threading as th

app = ur.Ursina()
player = Player(position=(0, 0, -3))

floor = ur.Entity(model='plane', scale=(100, 1, 100), color=ur.color.white.tint(-0.2), texture='white_cube', texture_scale=(100, 100), collider='box')
enemy = Enemy(position=(3, 1, 0))
enemy2 = Enemy(position=(0, 1, 3))
tisch = ur.Entity(model='cube', scale=(1, 1, 1), color="#000000", position=(0, 0.5, 0))
tischplatte = ur.Entity(model='circle', color="#5C4033", position=(0, 1.1, 0), rotation=(90, 0, 0), scale=(4, 4, 4))
app.run()


