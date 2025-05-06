import ursina as ur
from ursina.shaders import unlit_shader
class Card(ur.Entity):
    def __init__(self, parent, name, position, rotation):
        super().__init__(
            parent=parent,
            model="cube",
            position=position,
            rotation=rotation,
            scale=(0.001, 0.2, 0.1),
            color=ur.color.white.tint(-0.2),
            shader=unlit_shader
        )
        self.name = name
        self.mover = None
        self.locked = "not locked"
        
    def pick_card(self)  :
        '''
        handle the logic for picking cards
        '''
        if hasattr(self, 'mover') and self.mover:
            ur.destroy(self.mover)
        print("is locked: ", self.locked)
        if self.locked == "not locked":
            print("not locked")
            self.color = ur.color.green.tint(-0.2)
            self.locked = "locked"
            self.card_to_move = self
            self.pos_to_achieve = 0.95
            self.condition = self.pos_to_achieve - self.card_to_move.y
        else:
            self.color = ur.color.yellow.tint(-0.2)
            self.locked = "not locked"
            self.card_to_move = self
            self.pos_to_achieve = 0.9
            self.condition = self.card_to_move.y - self.pos_to_achieve
        self.mover = ur.Entity(update=self.move_card)
        self.rot_to_achieve = 720
        self.condition = 1.0
    
    def move_card(self):
        self.card_to_move.y = ur.lerp(self.card_to_move.y, self.pos_to_achieve, 4 * ur.time.dt)
        if (self.condition) < 0.01:
            print(self.condition)
            ur.destroy(self.mover)
            self.mover = None
            return