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
        
    def updates(self):
        for i in range(10):
            self.position -= ur.Vec3(1, 1, 1)
            ur.invoke(self.updates, delay=0.2)


if __name__ == '__main__':
    import main