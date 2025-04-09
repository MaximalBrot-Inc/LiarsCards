"""
create a player class that will create the player
"""
import ursina as ur 
from ursina.prefabs.first_person_controller import FirstPersonController
from gun import Gun


class Player(FirstPersonController):
    def __init__(self, master, pos, *args, **kwargs):
        super().__init__(position=pos[0]+(0, -1, 0), rotation=pos[1], *args, **kwargs)
        # pos: [(position), (rotation), (gun_pos), (gun_rot)] of opponents
        #self.model = "hatsune_miku"
        self.pos = pos
        self.gun = Gun(master, pos[2], pos[3])
        self.chair = ur.Entity(model="chair", position=self.position, rotation=self.rotation+(0, -90, 0), scale=1.5)
        self.gravity = 0
        
    
    def disable_movement(self):
        self.speed = 0
        self.jump_height = 0
        self.gravity = 0
        
    def gun_to_head(self):
        rot_to_achieve = self.gun.rotation + ur.Vec3(0, -180, 90)
        pos_to_achieve = self.gun.position + ur.Vec3(-0.1, 0.5, -0.3)
        
        def update():
            self.gun.rotation = ur.lerp(self.gun.rotation, rot_to_achieve, 4 * ur.time.dt)
            self.gun.position = ur.lerp(self.gun.position, pos_to_achieve, 4 * ur.time.dt)
            if (self.gun.rotation - rot_to_achieve).length() < 0.01 and (self.gun.position - pos_to_achieve).length() < 0.01:
                return
        
        ur.Entity(update=update)  # Attach the update function to an entity for continuous updates
    


if __name__ == '__main__':
    import main








