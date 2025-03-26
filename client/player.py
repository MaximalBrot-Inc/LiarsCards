"""
create a player class that will create the player
"""
import ursina as ur 
from ursina.prefabs.first_person_controller import FirstPersonController
from gun import Gun


class Player(FirstPersonController):
    def __init__(self, master, pos, *args, **kwargs):
        super().__init__(position=pos[0], rotation=pos[1], *args, **kwargs)
        # pos: [(position), (rotation), (gun_pos), (gun_rot)] of opponents
        self.pos = pos
        #self.disable_movement()
        self.gun = Gun(master, self.pos[2], self.pos[3], ur.color.green)
        self.gun_position = self.pos[2]  # Store initial gun position
        self.gravity = 0
    
    def disable_movement(self):
        self.speed = 0
        self.jump_height = 0
        self.gravity = 0
        
    def input(self, key):
        if key == "alt":
            exit()


if __name__ == '__main__':
    import main








