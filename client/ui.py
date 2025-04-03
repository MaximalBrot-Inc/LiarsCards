'''
Ui for the player, for example, the voting
'''
import ursina as ur

class UI:
    def __init__(self, master, *args, **kwargs):

        self.master = master
        # Use a container for custom positioning
        container = ur.Entity()
        ur.Text('Ready:', parent=container, position=(-3.5, 0.4), scale=50)
        ur.Text('3/3', parent=container, position=(1.5, 0.4), scale=50)
        wp = ur.WindowPanel(
            title='Press F3 to ready up',
            content=(container,),  # Wrapped container in a tuple
            popup=False,
            position=(0.55, -0.35)
        )
        
        def input(key):
            if key == "f3":
                print("Ready up!")


if __name__ == '__main__':
    import main
