import pyxel
import time
import sys

from tetris.mino import Mino
from tetris.field import Field

class App:
    def __init__(self):
        pyxel.init(200,200, fps=10)

        # initialize Field
        self.field = Field()
        self.mino = Mino()

        pyxel.run(self.update, self.draw)

    def update(self):
        self.field.check()

        # controller
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.mino.go_right(self.field)
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.mino.go_left(self.field)
        
        if pyxel.btn(pyxel.KEY_UP):
            self.mino.rotate_right(self.field)
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.mino.rotate_left(self.field)

        # mino go down
        self.mino.go_down(self.field)
        
        # check floor collision
        if self.mino.collide_bellow(self.field):
            # fix to field 
            self.field.fix_mino(self.mino) # fieldにminoを渡す

            # check and clear lines
            self.field.clear_lines()
            
            # renew mino
            self.mino = Mino()
   
    def draw(self):
        pyxel.cls(0)

        self.field.draw()
        self.mino.draw()
