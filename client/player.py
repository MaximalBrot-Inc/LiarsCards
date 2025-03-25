'''
create a player class that will create the player
'''
import ursina as ur 
from ursina.prefabs.first_person_controller import FirstPersonController
from gun import Gun


class Player(FirstPersonController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.disable_movement()
        
        self.gun = Gun(, (10, 10, 0), ur.color.green)
        self.gun_position = self.gun.position  # Store initial gun position

    def update(self):
        super().update()
        self.gun.position = self.gun_position  # Keep gun at initial position

    def disable_movement(self):
        self.speed = 0
        self.jump_height = 0
        self.gravity = 0
        
    def input(self, key):
        if key == "alt":
            exit()











