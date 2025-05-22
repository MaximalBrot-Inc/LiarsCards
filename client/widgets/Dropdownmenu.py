import ursina as ur
class DropdownMenu(ur.Entity):
    """
    A dropdown menu for selecting options.
    
    Scale behaves kinda weird. it's a 4:1 ratio, so if you want a 1:1 scale, set it to (0.25, 0.0625)

    :text: The text displayed on the main button.
    :options: A list of options to display in the dropdown.
    :commands: A list of functions to execute when an option is selected, if not given, it will print the selected option.
    :position: The position of the dropdown menu in the world.
    :scale: The scale of the dropdown menu.
    :bg_color: The background color of the dropdown menu.
    :fg_color: The foreground color of the dropdown menu.
    :primary_color: The primary color of the options in the dropdown menu.
    :secondary_color: The secondary color of the options in the dropdown menu.
    :highlight_color: The color of the button when hovered over.
    :border: Whether to add a border around the dropdown menu.
    :lr_border: Whether to add a border on the left and right side of the dropdown menu. Is ignored if border is set to True.
    :change_color: Whether to change the color of the options in the dropdown menu. If set to True, it will alternate between #262626 and #333333.
    """
    def __init__(self, parent:ur.Entity=ur.camera.ui, text:str="Select Option", text_size:float=None, options:list=["Option1", "Option2"], commands:list=[], position:tuple|int=(0, 0), scale:tuple|int=(0.4, 0.1), highlight_color:str="#5e5e5e", bg_color:str="#5e5e5e", fg_color:str="#333333", primary_color:str="#262626", secondary_color:str="#333333", border:bool=True, lr_border:bool=True, change_color:bool=True, **kwargs):
        super().__init__(parent=parent, position=position)
        if type(position) == int or type(position) == float:
            position = (position, position)
        else:
            if len(position) == 1:
                position = (position[0], position[0])
                
        if type(scale) == int or type(scale) == float:
            scale = (scale, scale/4)
        else:
            if len(scale) == 1:
                scale = (scale[0], scale[0]/4)  
                
        if scale[0] != 0 and scale[1] != 0:
            self.x_scale = scale[0]
            self.y_scale = scale[1]
        else:
            self.x_scale = 1
            self.y_scale = self.x_scale / 4
        
        self.text_size = text_size
        self.scales = (self.x_scale, self.y_scale)
        self.button_text = text  # Store the text for the button
        self.border_value = border
        self.lr_border = lr_border
        self.options = options
        self.commands = commands
        color = primary_color
        self.highlight_color = highlight_color
        x = self.x_scale * 4
        scale = x if x < self.y_scale else self.y_scale
        if self.text_size == None:
            self.text_size = self.y_scale*16
            
        else:
            self.text_size = scale*(4/scale)*self.text_size
        self.icon_scale = scale*5
        self.widget(fg_color, bg_color)
        # Create dropdown menu as a local entity with zero position offset
        # This ensures consistent positioning regardless of the parent's position
        self.dropdown_menu = ur.Entity(parent=self, enabled=False, position=(0, 0, 0), scale=(self.x_scale/4, self.y_scale))

        while len(self.options) > len(self.commands):
            self.commands.append(None)
        if len(self.options) < len(self.commands):
            raise ValueError("More commands than options")
        for x, i in enumerate(map(lambda x, y: (x, y), self.options, self.commands)):
            if change_color:
                color = primary_color if color == secondary_color else secondary_color
            c = ur.color.hex(color)
            self.add_option(i[0], i[1], x, c)
        num_options = len(self.options)
        
        if self.border_value:
            self.border((4, 0.1), (0.055, -0.7, -0.01))
            self.border((4, 0.1), (0.055, 0.1-(num_options + .8), -0.01)) 
            self.border((0.1, num_options), (-4/2 + 0.095, -(num_options - 0.6)/2 - 1, -0.01))
            self.border((0.1, num_options), (4/2+0.005, -(num_options - 0.6)/2 - 1, -0.01))
            
        if not self.border_value and self.lr_border:
            self.border((0.1, num_options), (-4/2 + 0.095, -(num_options - 0.6)/2 - 1, -0.01))
            self.border((0.1, num_options), (4/2+0.005, -(num_options - 0.6)/2 - 1, -0.01))


    def widget(self, fg_color, bg_color):
        bg = ur.Entity(parent=self, model=ur.Quad(aspect=1, radius=self.y_scale*0.2, scale=(self.scales[0], self.scales[1])), color=bg_color, position=(0, 0, 0))
        fg = ur.Entity(parent=self, model=ur.Quad(aspect=1, radius=self.y_scale*0.2, scale=(self.scales[0]-self.x_scale*0.02, self.scales[1]-self.x_scale*0.02)), color=fg_color, position=(0, 0, -0.001))
        self.text = ur.Text(
            parent=self,
            text=self.button_text,  # Use the text from the constructor
            color=ur.color.white,
            position=(self.x_scale*-0.425, self.y_scale*-0.2, -0.002),
            origin=(-.5, 0),
            scale=self.text_size,
        )
        self.text.align()
        self.text.default_resolution = 1080 * self.text.size
        button = ur.Button(
            parent=bg,
            model=ur.Quad(aspect=1, radius=self.x_scale*0.05, scale=(self.scales[0]/4, self.scales[1])),
            icon='arrow_down.png',
            icon_world_scale=self.icon_scale*4,
            text_size=self.x_scale*0.375,
            position=(self.x_scale/2.5, 0, -0.002),
            color=bg_color,
            on_click=self.toggle,
            highlight_color=ur.color.hex(self.highlight_color),
        )
        
        

    def add_option(self, text, on_click, i, color):
        # Create a button for each option
        ur.Button(
            text=text,
            text_size=self.text_size,
            parent=self.dropdown_menu,
            position=(0.05, -(i + 1.2), 0),  # Original button positioning
            scale=(3.8, 1),
            model='quad',
            color=color,  # Button color
            on_click=lambda text=text, on_click=on_click: self.on_option_selected(text, on_click),
        )

    def toggle(self):
        # Toggle the dropdown menu visibility
        self.dropdown_menu.enabled = not self.dropdown_menu.enabled
        
    def border(self, scale, position):
        """Create a border around the dropdown menu options"""

        border = ur.Entity(
            parent=self.dropdown_menu,
            model='quad',
            color=ur.color.white,
            scale=scale,  # Make it thicker for visibility
            position=position
        )
        
       
    def on_option_selected(self, option, command):
        # Execute the corresponding command if it exists
        index = self.options.index(option)
        if index < len(self.commands) and self.commands[index]:
            self.commands[index]()
        # Close the dropdown menu after selection
        self.text.text = option
        self.dropdown_menu.enabled = False
        if command is not None:
            command()
        self.current_selected = option
        self.text.align()

    def get_selected(self):
        # Return the currently selected option
        return self.current_selected if hasattr(self, 'current_selected') else None
    
    def set_selected(self, option):
        # Set the currently selected option
        if option in self.options:
            self.current_selected = option
            self.text.text = option
        else:
            raise ValueError(f"Option '{option}' not found in the dropdown menu.")
        
if __name__ == '__main__':
    app = ur.Ursina()
    ur.window.title = 'Dropdown Menu Example'
    main_button = DropdownMenu(
        text="Select Option",
        options=["Option 1", "Option 2", "Option 3", "Option 4"],
        commands=[
            lambda: print("Option 1 selected"),
            lambda: print("Option 2 selected"),
            lambda: print("Option 3 selected"),
            lambda: print("Option 4 selected"),

        ],
        position=(0.2, 0.2),
        scale=(0.2, 0.05),
        color="#555555",
        border=True,
        lr_border=True,
    )
    main_button = DropdownMenu(
        text="Select Option",
        options=["Option 1", "Option 2", "Option 3", "Option 4"],
        commands=[
            lambda: print("Option 1 selected"),
            lambda: print("Option 2 selected"),
            lambda: print("Option 3 selected"),
            lambda: print("Option 4 selected"),

        ],
        position=(0),
        scale=(0.4, 0.1),
        color="#555555",
        border=False,
        lr_border=True,
        change_color=False,

    )

    app.run()
