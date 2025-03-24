from ursina import *
import time
from ursina.prefabs.first_person_controller import FirstPersonController
import main 

class UI:
    def __init__(self):
        window.borderless = True
        self.start_round = False 
        self.text_label = Text(text='Enter your name:', origin=(0, 0.5), position=(-0.3, 0.4))
        self.input_field = InputField(default_value='', origin=(0, 0.5), position=(0.3, 0.4))
        submit_button = Button(text='Submit', origin=(0, 0.5), position=(0, 0.2), on_click=self.button_action, scale=(0.1, 0.05))
        start_button = Button(text='start', origin=(0, 0.5), position=(0, -0.2), on_click=self.start)
        self.result_text = Text(text='', origin=(0, 0.5), position=(0, 0))

    def button_action(self):
        name = self.input_field.text
        print(f'Hello, {name}!')
        self.result_text.text = f'Hello, {name}!'

    def start(self):
        self.start_round = True
        entities_copy = scene.entities[:]
        for entity in entities_copy:
            if entity != scene: #prevent the scene itself from being destroyed.
                destroy(entity)
                
        
                


