'''
creating and handling of gun
'''
import ursina as ur
import time
class Gun(ur.Entity):
    def __init__(self, master, ori, color):
        super().__init__(
            parent = master,
            model = 'cube',
            color = color,
            scale = (0.1, 0.1, 0.1),
            #origin = (1, 1, 1),
            
            rotation = (0, 0, 90),
            position = (0, 2, 1)
        )
        #self.updates()
        
    def updates(self):
        for i in range(10):
            self.position -= ur.Vec3(1, 1, 1)
            ur.invoke(self.updates, delay=0.2)


if __name__ == '__main__':
    import main