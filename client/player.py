"""
create a player class that will create the player
"""
import ursina as ur 
from ursina.prefabs.first_person_controller import FirstPersonController
from gun import Gun
from ursina import camera, color


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
        self.blackout()
        
    
    def disable_movement(self):
        self.speed = 0
        self.jump_height = 0
        self.gravity = 0
        
    def dead(self):
        ur.camera.overlay.texture = "Leserunde.png"
        ur.camera.overlay.color = ur.color.white.tint(-0.2)
        ur.camera.overlay.alpha_setter(0.2)
        ur.camera.overlay.scale = (2, 2)

        
    def blackout(self):
        ur.camera.overlay.color = ur.color.black
        ur.camera.overlay.scale = 2
        # font: Adobe Garamond Pro Bold
        ur.Text(
            parent=ur.camera.overlay,
            text="YOU DIED",
            position=ur.Vec2(-0.24,  0.05),
            scale=ur.Vec2(4, 4),
            color=ur.color.red,
        )
        ur.invoke(self.dead, delay=4)



if __name__ == '__main__':
    import main








