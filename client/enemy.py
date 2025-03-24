'''
The enemy class will be used to create enemies that the player will play against.
'''

import ursina as ur 

class Enemy(ur.Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.model = 'cube'
        self.color = ur.color.red
        self.scale = (1, 1, 1)
        
        
        self.direction = ur.Vec3(0, 0, 0)