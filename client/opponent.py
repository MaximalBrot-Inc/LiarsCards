"""
The enemy class will be used to create enemies that the player will play against.
"""

import ursina as ur 
from gun import Gun
from ursina.shaders import lit_with_shadows_shader
import math
class Opponent(ur.Entity):
    def __init__(self, pos, uid, model,*args, **kwargs):
        super().__init__(position=pos[uid][0], rotation=pos[uid][1]+(0, 90, 0), *args, **kwargs)
        self.model = model
        self.scale = 2
        self.chair = ur.Entity(parent=self,
                            model="chair", 
                            position=(0, -0.385, 0), 
                            rotation=(0, 180, 0), 
                            scale=0.75
                            )
        
        self.gun = Gun(self.chair, (0.6, 0.75, -0.1), (0, 90, -90), pos, self)
        self.name_tag = ur.Text(
            parent=self,
            text="username",
            position=ur.Vec3(0, 1, 0),
            scale=ur.Vec2(5, 3),
            billboard=True,
            color=ur.color.black,
            origin=ur.Vec2(0, 0)
        )
        
    def spawn_cards(self, cards):
        center_pos = (0, 0.9, 0)
        radius = 0.8
        start_angle = -30
        for i, card_data in enumerate(cards):
            angle = start_angle + i * (60 / max(1, (len(cards) - 1)))
            rad = math.radians(angle)
            x = center_pos[0] + radius * math.cos(rad)
            z = center_pos[2] + radius * math.sin(rad)
            card = ur.Entity(
                parent=self.chair,
                model="cube",
                position=(x, center_pos[1], z),
                rotation=(0, -angle, 0),
                scale=(0.001, 0.2, 0.1),
                color=ur.color.white.tint(-0.2),
                shader=lit_with_shadows_shader
            )
        #self.direction = ur.Vec3(0, 0, 0)

    


if __name__ == '__main__':
    import main