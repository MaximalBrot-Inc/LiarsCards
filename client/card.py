import ursina as ur
from ursina.shaders import unlit_shader
class Card(ur.Entity):
    def __init__(self, parent, name, position, rotation, model, table):
        super().__init__(
            parent=parent,
            model=model+".glb",
            #model="gun.glb",
            position=position,
            rotation=rotation,
            #scale=(0.001, 0.2, 0.1),
            scale=2,
            color=ur.color.white.tint(-0.2),
            shader=unlit_shader
        )
        self.table = table
        self.name = name
        self.mover = None
        self.locked = "not locked"
        self.add_width = 0.2
        self.border = ur.Entity(
            parent=self,
            model="Border.obj",
            #wireframe=True,
            scale=1,
            #color=ur.color.clear,
            #double_sided=True,
            shader=unlit_shader,
            always_on_top=True,
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
            self.pos_to_achieve = (0, .83, 0)
        if amount == 2:
            self.pos_to_achieve = (0, .83, -0.3)
        if amount == 3:
            self.pos_to_achieve = (0, .83, -0.4)
        if amount == 4:
            self.pos_to_achieve = (0, .83, -0.6)
        if amount == 5:
            self.pos_to_achieve = (0, .83, -0.7)
        self.rot_to_achieve = (0, -90, -180)
        self.pos_to_achieve = ur.Vec3(self.pos_to_achieve[0], self.pos_to_achieve[1], self.pos_to_achieve[2] + (self.add_width * current_amount))
        pos = self.world_position
        rot = self.world_rotation
        scale = self.world_scale
        self.parent = self.table
        print(pos, rot)
        self.world_position = pos
        self.world_rotation = rot
        if hasattr(self, 'mover') and self.mover:
            ur.destroy(self.mover)

        self.mover = ur.Entity(update=self.update_pos_reset)
    
    def update_pos_reset(self):
        try:
            self.rotation = ur.lerp(self.rotation, self.rot_to_achieve, 4 * ur.time.dt)
            self.position = ur.lerp(self.position, self.pos_to_achieve, 2 * ur.time.dt)
            if (self.rotation - self.rot_to_achieve).length() < 0.01 and (self.position - self.pos_to_achieve).length() < 0.01:
                ur.destroy(self.mover)
                self.mover = None
                return
        except AssertionError:
            print("Card already destroyed")
            ur.destroy(self.mover)
            self.mover = None
            return
        

if __name__ == '__main__':
    import main