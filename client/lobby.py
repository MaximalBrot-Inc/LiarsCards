import time
import ursina as ur
from ursina.prefabs.first_person_controller import FirstPersonController
from widgets.Dropdownmenu import DropdownMenu

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
        position=(-0.1, 0.2)
        )
        gradient = ur.Entity(model='quad', texture='vertical_gradient', parent=ur.scene, scale=(ur.camera.aspect_ratio*9.5, 9.5), color=ur.color.hsv(240,.6,.1,.75), position=(0, 0, 0))
        self.heading = ur.Text(text='Leserunde', position=(0, 0.4), texture="rainbow", scale=4, origin=(0, 0))
        self.name = ur.InputField(default_value='', position=(0.5, 0.16), limit_content_to="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ", active=True, character_limit=20)
        self.server_ip = ur.InputField(default_value='', position=(0.5, 0.085), limit_content_to="0123456789.", character_limit=13)
        self.server_port = ur.InputField(default_value='', position=(0.5, 0.01), limit_content_to="0123456789", character_limit=5)

        self.Dropdown = DropdownMenu(text="Select Skin", options=['default', 'Skin 1', 'Skin 2', 'Skin 3'], position=(0.495, -0.084), scale=(0.49, 0.05))
        self.skin = ur.Entity(model=None, color=ur.color.white, position=(-3.75, -3, -1), scale=4, rotation=(0, -90, 0), update=self.update)
        self.start_button = ur.Button(text='start', position=(0.5, -0.4), on_click=exit, scale=(0.5, 0.05), color=ur.color.azure)
        
        self.name.next_field = self.server_ip
        self.server_ip.next_field = self.server_port
        self.server_port.next_field = self.start_button
        self.exit = False
        # self.result_text = ur.Text(text='', position=(0, 0))
        
    
            
    def update(self):
        ur.time.sleep(0.01)
        skin = self.Dropdown.get_selected()
        if skin == None:
            return
    
        self.skin.model = skin.replace(" ", "")
        self.skin.rotation_y += 1
        if self.exit:
            return

if __name__ == '__main__':
    import main