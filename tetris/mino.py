import random
import configparser 

from tetris.field import Field
from tetris.block import Block

config = configparser.ConfigParser()
config.read("config.ini")

COL_SIZE = int(config["FIELD"]["COL_SIZE"])

class Mino:
    minos = [
            [
                [0,0,0,1,1,1,1,0,0,0],
                [0,0,0,0,0,0,0,0,0,0] ],
            [
                [0,0,0,1,0,0,0,0,0,0],
                [0,0,0,1,1,1,0,0,0,0] ],
            [
                [0,0,0,0,0,1,0,0,0,0],
                [0,0,0,1,1,1,0,0,0,0] ],
            [
                [0,0,0,0,1,1,0,0,0,0],
                [0,0,0,0,1,1,0,0,0,0] ],
            [
                [0,0,0,0,1,1,0,0,0,0],
                [0,0,0,1,1,0,0,0,0,0] ],
            [
                [0,0,0,0,1,1,0,0,0,0],
                [0,0,0,0,0,1,1,0,0,0] ],
            [
                [0,0,0,0,0,1,0,0,0,0],
                [0,0,0,0,1,1,1,0,0,0] ]
            ]

    mino_types = ["I","J","L","O","S","Z","T"]
    mino_colors = [12,5,9,10,11,8,2]

    def __init__(self):
        mino_index = random.randint(0,6)
        self.type = Mino.mino_types[mino_index]
        self.color = Mino.mino_colors[mino_index]
        self.mino_template = Mino.minos[mino_index]
        self.blocks = self.initialize()

    def initialize(self):
        mino_blocks = []
        for row in range(2):
            for col in range(COL_SIZE):
                if self.mino_template[row][col] == 1:
                    mino_blocks.append(Block(row, col, self.color))
        return mino_blocks 
    
    def draw(self) -> None:
        for block in self.blocks:
            block.draw()

    # DOWN
    def collide_bellow(self, field) -> None:
        # 床に衝突
        for block in self.blocks:
            if block.collide_bellow(field):
                return True
        return False

    def go_down(self, field):
        if self.collide_bellow(field):
            return False

        for block in self.blocks:
            block.go_down()

    # RIGHT
    def collide_right(self, field) -> None:
        for block in self.blocks:
            if block.collide_right(field):
                return True
        return False

    def go_right(self, field):
        if self.collide_right(field):
            return False
        
        for block in self.blocks:
            block.go_right()
    
    # LEFT
    def collide_left(self, field) -> None:
        for block in self.blocks:
            if block.collide_left_wall() or block.collide_left_block(field):
                return True
        return False

    def go_left(self, field):
        if self.collide_left(field):
            return False

        for block in self.blocks:
            block.go_left()
    
    def rotate_right(self):
        pass

    def rotate_left(self):
        pass
