"""
The enemy class will be used to create enemies that the player will play against.
"""

import ursina as ur 
from gun import Gun
class Opponent(ur.Entity):
    def __init__(self, master, pos, model,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.pos = pos
        self.gun = Gun(master, self.pos[2], self.pos[3], ur.color.green)
        #self.direction = ur.Vec3(0, 0, 0)
        

if __name__ == '__main__':
    import main