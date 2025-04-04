"""
The enemy class will be used to create enemies that the player will play against.
"""

import ursina as ur 
from gun import Gun
class Opponent(ur.Entity):
    def __init__(self, master, pos, model,*args, **kwargs):
        super().__init__(position=pos[0], rotation=pos[1], *args, **kwargs)
        self.model = model
        self.gun = Gun(master, pos[2], pos[3])
        self.chair = ur.Entity(model="chair", 
                               position=self.position+(0, -1, 0), 
                               rotation=self.rotation+(0, -90, 0), 
                               scale=1.5
                            )
        
        self.name_tag = ur.Text(
            parent=self,
            text="username",
            position=ur.Vec3(0, 2, 0),
            scale=ur.Vec2(5, 3),
            billboard=True,
            origin=ur.Vec2(0, 0)
                                )
        
        #self.direction = ur.Vec3(0, 0, 0)

    


if __name__ == '__main__':
    import main