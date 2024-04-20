import pyxel
import time

from mino import Mino
from field import Field

class App:
    def __init__(self):
        pyxel.init(200,200, fps=10)

        # initialize Field
        self.field = Field()
        self.mino = Mino()

        pyxel.run(self.update, self.draw)

    def update(self):
        if self.mino.collide_bellow(self.field):
            # fix to field
            self.field.fix_mino(self.mino)

            self.mino = Mino()
        
        # controller
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.mino.go_right(self.field)
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.mino.go_left(self.field)

        # mino go down
        self.mino.go_down(self.field)
   
    def clear(self):
        pyxel.cls(0)

    def draw(self):
        self.clear()

        self.field.draw()
        self.mino.draw()

if __name__ == "__main__":
    App()
