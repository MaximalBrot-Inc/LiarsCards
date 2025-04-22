"""
The enemy class will be used to create enemies that the player will play against.
"""

import ursina as ur 
from gun import Gun
class Opponent(ur.Entity):
    def __init__(self, master, pos, model,*args, **kwargs):
        super().__init__(position=pos[0], rotation=pos[1]+(0, 90, 0), *args, **kwargs)
        self.model = model
        self.scale = 2
        self.chair = ur.Entity(parent=self,
                            model="chair", 
                            position=(0, -0.385, 0), 
                            rotation=(0, 180, 0), 
                            scale=0.75
                            )
        
        self.gun = Gun(self.chair, (0.6, 0.75, -0.1), (0, 90, -90))
        self.name_tag = ur.Text(
            parent=self,
            text="username",
            position=ur.Vec3(0, 1, 0),
            scale=ur.Vec2(5, 3),
            billboard=True,
            color=ur.color.black,
            origin=ur.Vec2(0, 0)
        )
        
        #self.direction = ur.Vec3(0, 0, 0)

    


if __name__ == '__main__':
    import main