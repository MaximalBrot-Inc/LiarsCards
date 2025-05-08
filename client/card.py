import ursina as ur
from ursina.shaders import unlit_shader
class Card(ur.Entity):
    def __init__(self, parent, name, position, rotation, model):
        super().__init__(
            parent=parent,
            model=model+".glb",
            #model="cube",
            position=position,
            rotation=rotation,
            #scale=(0.001, 0.2, 0.1),
            scale=2,
            color=ur.color.white.tint(-0.2),
            shader=unlit_shader
        )
        self.name = name
        self.mover = None
        self.locked = "not locked"
        self.add_width = 0.2
        self.border = ur.Entity(
            parent=self,
            model='cube',
            wireframe=True,
            scale=(0.05, 0.0005, 0.08),
            color=ur.color.clear,
            double_sided=True,
            shader=unlit_shader
        )
        
    def pick_card(self):
        '''
        handle the logic for picking cards
        '''
        if hasattr(self, 'mover') and self.mover:
            ur.destroy(self.mover)
        if self.locked == "not locked":
            #self.border.color = ur.color.green
            self.locked = "locked"
            self.card_to_move = self
            self.pos_to_achieve = 0.95
            self.condition = self.pos_to_achieve - self.card_to_move.y
        else:
            #self.border.color = ur.color.clear
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

    def throw_cards_on_table(self, amount, current_amount):
        if amount == 1:
            self.pos_to_achieve = (0, 1.3, 0)
        if amount == 2:
            self.pos_to_achieve = (0, 1.3, -0.3)
        if amount == 3:
            self.pos_to_achieve = (0, 1.3, -0.4)
        if amount == 4:
            self.pos_to_achieve = (0, 1.3, -0.6)
        if amount == 5:
            self.pos_to_achieve = (0, 1.3, -0.7)
        self.rot_to_achieve = (0, 0, 180)
        self.pos_to_achieve = ur.Vec3(self.pos_to_achieve[0], self.pos_to_achieve[1], self.pos_to_achieve[2] + (self.add_width * current_amount))
        pos = self.world_position
        rot = self.world_rotation
        scale = self.world_scale
        self.parent = ur.scene
        print(pos, rot)
        self.position = pos
        self.rotation = rot
        self.scale = scale
        if hasattr(self, 'mover') and self.mover:
            ur.destroy(self.mover)

        self.mover = ur.Entity(update=self.update_pos_reset)
    
    def update_pos_reset(self):
        self.rotation = ur.lerp(self.rotation, self.rot_to_achieve, 3 * ur.time.dt)
        self.position = ur.lerp(self.position, self.pos_to_achieve, 1 * ur.time.dt)
        if (self.rotation - self.rot_to_achieve).length() < 0.01 and (self.position - self.pos_to_achieve).length() < 0.01:
            ur.destroy(self.mover)
            self.mover = None
            return

if __name__ == '__main__':
    import main