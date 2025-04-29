"""
create a player class that will create the player
"""
import ursina as ur 
from ursina.prefabs.first_person_controller import FirstPersonController
from gun import Gun
from ursina.shaders import lit_with_shadows_shader
import math



class Player(FirstPersonController):
    def __init__(self, pos, uid, *args, **kwargs):
        super().__init__(position=pos[uid][0]+(0, -0.7, 0), rotation=pos[uid][1], *args, **kwargs)
        # pos: [(position), (rotation), (gun_pos), (gun_rot)] of opponents
        self.model = "human"
        self.pos = pos[uid]
        self.gun_pos = (0.6, 0.75, -0.1)
        self.gun_rot = (0, 90, -90)
        self.uid = uid
        #self.gun = Gun(self, pos[2], pos[3])
        self.chair = ur.Entity(model="chair", position=self.position, rotation=self.rotation+(0, -90, 0), scale=1.5)
        self.gun = Gun(self.chair, self.gun_pos, self.gun_rot, pos, self)
        self.gravity = 0
        self.cards = []
        self.picked_cards = []
        self.card_selected = 0
    
    def disable_movement(self):
        self.speed = 0
        self.jump_height = 0
        self.gravity = 0
        
    def dead(self):
        try:
            ur.destroy(self.death_text)
        except AttributeError:
            pass
        ur.camera.overlay.texture = "dead.png"
        ur.camera.overlay.color = ur.color.white.tint(-0.2)
        ur.camera.overlay.alpha_setter(0.9)
        ur.camera.overlay.scale = (1.75, 1)
        ur.camera.overlay.position = (0, 0)
        
    def blackout(self):
        ur.camera.overlay.color = ur.color.black
        ur.camera.overlay.scale = 2
        # font: Adobe Garamond Pro Bold
        self.death_text = ur.Text(
            parent=ur.camera.overlay,
            text="YOU DIED",
            position=ur.Vec2(-0.24,  0.05),
            scale=ur.Vec2(4, 4),
            color=ur.color.red,
            font="VeraMono.ttf",
        )
        ur.invoke(self.dead, delay=4)
    
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
            self.cards.append((card, card_data))
    
    def select_cards(self):
        '''
        handle the logic for selecting a card
        '''
        
        print(self.cards)
        
    def pick_card(self)  :
        '''
        handle the logic for picking cards
        '''




if __name__ == '__main__':
    import main








