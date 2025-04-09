"""
creating and handling of gun
"""
import ursina as ur
import time
class Gun(ur.Entity):
    def __init__(self, master, pos, rot):
        super().__init__(
            parent = master,
            model = 'gun.glb',
            scale = (0.001, 0.001, 0.001),
            #origin = (1, 1, 1),
            
            rotation = rot,
            position = pos
        )
        #self.updates()
        
    def gun_to_head(self):
        self.rot_to_achieve = self.rotation + ur.Vec3(0, -180, 90)
        self.pos_to_achieve = ur.Vec3(0.25, 1.35, 0)
        #+ ur.Vec3(-0.1, 0.5, -0.3)
        if hasattr(self, 'mover') and self.mover:
            ur.destroy(self.mover)
        self.mover = ur.Entity(update=self.update_pos)
        
    def update_pos(self):
        self.rotation = ur.lerp(self.rotation, self.rot_to_achieve, 4 * ur.time.dt)
        self.position = ur.lerp(self.position, self.pos_to_achieve, 4 * ur.time.dt)
        if (self.rotation - self.rot_to_achieve).length() < 0.01 and (self.position - self.pos_to_achieve).length() < 0.01:
            ur.destroy(self.mover)
            self.mover = None
            return
    
    def reset(self):
        self.pos_to_achieve = (0.6, 0.833, -0.1)
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

if __name__ == '__main__':
    import main