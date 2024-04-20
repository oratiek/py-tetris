import pyxel
import configparser 

config = configparser.ConfigParser()
config.read("config.ini")

BLOCK_SIZE = int(config["BLOCK"]["SIZE"])
ROW_SIZE = int(config["FIELD"]["ROW_SIZE"])
COL_SIZE = int(config["FIELD"]["COL_SIZE"])
X_OFFSET = int(config["FIELD"]["X_OFFSET"])
Y_OFFSET = int(config["FIELD"]["Y_OFFSET"])

class Block:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.size = BLOCK_SIZE
        self.color = color

    def go_down(self) -> None:
        self.row += 1

    def collide_bellow(self, field) -> None:
        if self.collide_bellow_wall():
            print("bellow_wall", True)
            return True
        elif self.collide_bellow_block(field):
            print("bellow_block", True)
            return True
        return False

    def collide_bellow_wall(self) -> None:
        if self.row == ROW_SIZE - 1:
            return True
        return False

    def collide_bellow_block(self, field) -> None:
        # FIXME インデックスエラーの可能性あり。collide_bellowで短絡評価されてここに来るときはindexerrorにならない場所のはずなんだけどな
        bellow_block = field.get_block(self.row + 1, self.col) 
        return bellow_block.color != 0
    
    # COLLIDE RIGHT
    def collide_right(self, field) -> None:
        if self.collide_right_wall() or self.collide_right_block(field):
            return True
        return False

    def collide_right_wall(self) -> None:
        return self.col >= COL_SIZE - 1
    
    def collide_right_block(self, field) -> None:
        right_block = field.get_block(self.row, self.col + 1)
        return right_block.color != 0 # TODO マジックナンバーの解消

    def go_right(self) -> None:
        self.col += 1

    # COLLIDE LEFT
    def collide_left(self, field) -> None:
        if self.collide_left_wall() or self.collide_left_block(field):
            return True
        return False

    def collide_left_wall(self) -> None:
        return self.col < 0

    def collide_left_block(self, field) -> None:
        left_block = field.get_block(self.row, self.col - 1)
        return left_block.color != 0 # TODO マジックナンバー解消
    
    def go_left(self) -> None:
        self.col -= 1

    def draw(self) -> None:
        x = X_OFFSET + (self.col * self.size)
        y = Y_OFFSET + (self.row * self.size)
        pyxel.rect(x, y, self.size, self.size, self.color)
