"""
create a player class that will create the player
"""
import ursina as ur 
from ursina.prefabs.first_person_controller import FirstPersonController
from gun import Gun


class Player(FirstPersonController):
    def __init__(self, pos, uid, *args, **kwargs):
        super().__init__(position=pos[0]+(0, -0.7, 0), rotation=pos[1], *args, **kwargs)
        # pos: [(position), (rotation), (gun_pos), (gun_rot)] of opponents
        self.model = "human"
        self.pos = pos 
        self.gun_pos = (0.6, 0.75, -0.1)
        self.gun_rot = (0, 90, -90)
        self.uid = uid
        #self.gun = Gun(self, pos[2], pos[3])
        self.chair = ur.Entity(model="chair", position=self.position, rotation=self.rotation+(0, -90, 0), scale=1.5)
        self.gun = Gun(self.chair, self.gun_pos, self.gun_rot, self)
        self.gravity = 0
        
    
    def disable_movement(self):
        self.speed = 0
        self.jump_height = 0
        self.gravity = 0

    

        
          # Attach the update function to an entity for continuous updates
    


if __name__ == '__main__':
    import main








