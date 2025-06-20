"""
creating and handling of gun
"""
import ursina as ur
import random
from ursina.shaders import lit_with_shadows_shader
class Gun(ur.Entity):
    def __init__(self, master, pos, rot, position, opp, name):
        super().__init__(
            parent = master,
            model = ur.load_model('gun.glb', use_deepcopy=True),
            scale = 0.001,
            #origin = (1, 1, 1),
            rotation = rot,
            position = pos,
            #color=ur.color.white.tint(-0.2),
            shader=lit_with_shadows_shader,
        )
        self.name = name
        self.opp = opp
        #self.updates()
        self.drum = 5
        self.alive = 1
        
    def gun_to_head(self):
        self.rot_to_achieve = self.rotation + ur.Vec3(0, -180, 90)
        self.pos_to_achieve = ur.Vec3(0.3, 1.35, 0)
        
        #+ ur.Vec3(-0.1, 0.5, -0.3)
        if hasattr(self, 'mover') and self.mover:
            ur.destroy(self.mover)
        self.mover = ur.Entity(update=self.update_pos)
    #     choice = self.empty_or_loaded()
    #     if choice[0] == 'loaded':
    #         self.shoot()
    
    # def empty_or_loaded(self):
    #     choice = random.choices(['empty', 'loaded'], [self.drum, 1])
    #     print(self.drum)
    #     self.drum -= 1
    #     return choice

    def update_pos(self):
        self.rotation = ur.lerp(self.rotation, self.rot_to_achieve, 4 * ur.time.dt)
        self.position = ur.lerp(self.position, self.pos_to_achieve, 4 * ur.time.dt)
        if (self.rotation - self.rot_to_achieve).length() < 0.01 and (self.position - self.pos_to_achieve).length() < 0.01:
            ur.destroy(self.mover)
            self.mover = None
            return
    
    def reset(self):
        self.pos_to_achieve = (0.6, 0.75, -0.1)
        self.rot_to_achieve = (0, 90, -90)
        if hasattr(self, 'mover') and self.mover:
            ur.destroy(self.mover)
        self.mover = ur.Entity(update=self.update_pos_reset)
    
    def update_pos_reset(self):
        self.rotation = ur.lerp(self.rotation, self.rot_to_achieve, 4 * ur.time.dt)
        self.position = ur.lerp(self.position, self.pos_to_achieve, 4 * ur.time.dt)
        if (self.rotation - self.rot_to_achieve).length() < 0.01 and (self.position - self.pos_to_achieve).length() < 0.01:
            ur.destroy(self.mover)
            self.mover = None
            return
    
    def shoot(self):
        print("bang")   
        self.opp.visible_self = False
        self.alive = 0
        try:
            self.opp.name_tag.text += "dead"
        except:
            print("player dead")
            self.opp.blackout()
        print("players alive:", self.position)
        


        
if __name__ == '__main__':
    import main