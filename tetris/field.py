import pyxel
import configparser 
import sys

config = configparser.ConfigParser()
config.read("config.ini")

BLOCK_SIZE = int(config["BLOCK"]["SIZE"])
ROW_SIZE = int(config["FIELD"]["ROW_SIZE"])
COL_SIZE = int(config["FIELD"]["COL_SIZE"])
X_OFFSET = int(config["FIELD"]["X_OFFSET"])
Y_OFFSET = int(config["FIELD"]["Y_OFFSET"])

# 0: None
# 1: Fixed

class Field:
    def __init__(self):
        self.field = self.new_field()

    def check(self):
        output = ""
        for row in self.field:
            row_output = ""
            for block in row:
                if block != 0:
                    row_output += "{:3}".format(1)
                else:
                    row_output += "{:3}".format(0)
            output += "{}\n".format(row_output)
        print("({},{})".format(len(self.field), len(self.field[0])))

        print("\r{}".format(output))

    def new_field(self) -> list:
        field = []
        for row in range(ROW_SIZE):
            tmp = []
            for col in range(COL_SIZE):
                tmp.append(0)# FIXME マジックナンバーの解消
            field.append(tmp)
        return field

    def get_new_row(self, row_index) -> list:
        row = []
        for col in range(COL_SIZE):
            row.append(0)# FIXME マジックナンバーの解消
        return row
    
    def get_block(self, row, col):
        return self.field[row][col]

    def fix_mino(self, mino) -> None:
        for block in mino.blocks:
            self.field[block.row][block.col] = 1 # FIXME マジックナンバーの解消
            block.fix()

    def draw(self) -> None:
        for row in range(ROW_SIZE):
            for col in range(COL_SIZE):
                x = X_OFFSET + (col * BLOCK_SIZE)
                y = Y_OFFSET + (row * BLOCK_SIZE)
                pyxel.rect(x, y, BLOCK_SIZE, BLOCK_SIZE, self.field[row][col])

    def get_clear_line_rows(self) -> list:
        # 0: no block is placed 
        clear_rows = []
        for row in range(ROW_SIZE):
            clear_row_flag = True
            for col in range(COL_SIZE):
                if self.field[row][col] == 0:# FIXME マジックナンバーの解消
                    clear_row_flag = False
            if clear_row_flag:
                clear_rows.append(row)
        
        return clear_rows

    def clear_lines(self):
        clear_line_rows = self.get_clear_line_rows()
        for clear_line_row in clear_line_rows:
            self.clear_line(clear_line_row)

    def clear_line(self, row_index):
        self.drop_row(row_index)
        new_row = self.get_new_row(row_index)
        self.put_row(new_row)

    def drop_row(self, row_index):
        self.field.pop(row_index)

    def put_row(self, row):
        # add row to top of field
        self.field = [row] + self.field
