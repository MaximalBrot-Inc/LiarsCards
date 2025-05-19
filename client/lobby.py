import time
import ursina as ur
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.Dropdownmenu import DropdownMenu

class Lobby:
    def __init__(self):
        ur.window.borderless = False
        # self.start_round = False
        
        self.text_label = ur.Text(text=
        '''
        Enter your name:
        
        
            Enter server ip:
        
        
        Enter server port:
        
        
                   Select Skin:
        ''', 
        position=(-0.3, 0.4)
        )
        self.name = ur.InputField(default_value='', position=(0.3, 0.36))
        self.server_ip = ur.InputField(default_value='', position=(0.3, 0.285))
        self.server_port = ur.InputField(default_value='', position=(0.3, 0.21))
        self.Dropdown = DropdownMenu(text="Select Skin", options=['Skin 1', 'Skin 2', 'Skin 3'], position=(2.75, 1.25), scale=(4.5, 0.5), text_size=5)
        # start_button = ur.Button(text='start', position=(0, -0.2), on_click=self.start, scale=0.2)
        # self.result_text = ur.Text(text='', position=(0, 0))
        



    def start(self):
        self.start_round = True
        entities_copy = ur.scene.entities[:]
        for entity in entities_copy:
            if entity != ur.scene: 
                ur.destroy(entity)
                
                


if __name__ == '__main__':
    import main