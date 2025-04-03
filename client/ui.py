'''
Ui for the player, for example, the voting
'''
import ursina as ur

class UI:
    def __init__(self, master, *args, **kwargs):
        self.master = master
        self.max_player = 1
        self.count = 0
        container = ur.Entity()
        ur.Text('Ready:', parent=container, position=(-3.5, 0.4), scale=50)
        self.text = ur.Text(f'{self.count}/{self.max_player}', parent=container, position=(1.5, 0.4), scale=50)
        self.wp = ur.WindowPanel(
            title='Press F3 to ready up',
            content=(container,),  # Wrapped container in a tuple
            popup=False,
            position=(0.65, -0.35)
        )
            


if __name__ == '__main__':
    import main
