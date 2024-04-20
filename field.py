import pyxel
import configparser 

from block import Block

config = configparser.ConfigParser()
config.read("config.ini")

BLOCK_SIZE = int(config["BLOCK"]["SIZE"])
ROW_SIZE = int(config["FIELD"]["ROW_SIZE"])
COL_SIZE = int(config["FIELD"]["COL_SIZE"])
X_OFFSET = int(config["FIELD"]["X_OFFSET"])
Y_OFFSET = int(config["FIELD"]["Y_OFFSET"])


class Field:
    def __init__(self):
        self.field = self.reset_field()

    def reset_field(self) -> list:
        field = []
        for row in range(ROW_SIZE):
            tmp = []
            for col in range(COL_SIZE):
                tmp.append(Block(row, col, 0))
            field.append(tmp)
        return field
    
    def get_block(self, row, col) -> Block:
        return self.field[row][col]

    def fix_mino(self, mino) -> None:
        for block in mino.blocks:
            self.field[block.row][block.col] = block

    def draw(self) -> None:
        for row in range(ROW_SIZE):
            for col in range(COL_SIZE):
                self.field[row][col].draw()
