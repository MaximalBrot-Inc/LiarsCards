'''
create a player class that will create the player
'''
import ursina as ur 
from ursina.prefabs.first_person_controller import FirstPersonController


class Player(FirstPersonController):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.disable_movement()

    def disable_movement(self):
        self.speed = 0
        self.jump_height = 0
        self.gravity = 0
        
    def input(self, key):
        if key == "alt":
            exit()

   




