import pyxel
import numpy as np
import random
import sys
import math
import time

# 色の概念を一旦考えない
# 0：動いていない
# 1：動作中
# 2：ドロップ済み
# dropした時に値を0に変更してサーチから逃れる

mino_color = []

class Mino:
    def __init__(self):
        minos = {
                "I":[1,1,1,1],
                "J":[[2,0,0,0],[2,2,2,2]],
                "L":[[0,0,0,3],[3,3,3,3]],
                "O":[[4,4],[4,4]],
                "S":[[0,5,5],[5,5,0]],
                "Z":[[6,6,0],[0,6,6]],
                "T":[[0,7,0],[7,7,7]]
        }
        minos = [
                [[0,0,0,1,1,1,1,0,0,0]],
                [[0,0,0,1,0,0,0,0,0,0],[0,0,0,1,1,1,0,0,0,0]],
                [[0,0,0,0,0,1,0,0,0,0],[0,0,0,1,1,1,0,0,0,0]],
                [[0,0,0,0,1,1,0,0,0,0],[0,0,0,0,1,1,0,0,0,0]],
                [[0,0,0,0,1,1,0,0,0,0],[0,0,0,1,1,0,0,0,0,0]],
                [[0,0,0,0,1,1,0,0,0,0],[0,0,0,0,0,1,1,0,0,0]],
                [[0,0,0,0,0,1,0,0,0,0],[0,0,0,0,1,1,1,0,0,0]]
        ]
        Z_mino_patterns = [
            [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
        ]
        mino_types = ["I","J","L","O","S","Z","T"]
        mino_colors = [12,5,9,10,11,8,2]
        self.mino_center_indexs = {
            "I":[2,1,1,2],
            "J":[1,0,2,3],
            "L":[3,2,0,1],
            "O":None,
            "S":[3,1,0,2],
            "Z":[1,2,2,1],
            "T":[2,1,1,2]
        }
        self.rotate_cnt = 0
        random_num = random.randint(0,6)
        mino_color.append(mino_colors[random_num])
        print(mino_color)
        #random_num = 3
        self.mino = minos[random_num]
        self.mino_type = mino_types[random_num]
        self.mino_center_index = self.mino_center_indexs[self.mino_type]

class Field:
    def __init__(self):
        self.row_size = 20
        self.column_size = 10

        # フィールドをリセットする:
        self.field = []
        self.reset_field()

        # 座標を計算する
        self.cords = [] # x y w h
        self.calc_cords()

        # move_dのためのフレーム情報
        self.frames = 0 # 何フレームごとにmove_dするかで速度を変える

    def reset_field(self):
        for row in range(self.row_size):
            tmp = []
            for j in range(self.column_size):
                tmp.append(0)
            self.field.append(tmp)

    def calc_cords(self):
        x_start = 0
        y_start = 0
        step = 10 
        hight = 9
        width = 9
        x_offset = 0
        y_offset = 46
        for row in range(self.row_size):
            tmp = []
            for column in range(self.column_size):
                tmp.append([x_offset+row*step, y_offset+column*step, hight, width])
            self.cords.append(tmp)

    def put_mino(self, mino): # recv mino instance
        # 行ごと書き換える
        print("put_mino")
        self.mino = mino
        self.mino_type = self.mino.mino_type
        self.mino_center_index = self.mino.mino_center_index
        for i in range(len(mino.mino)):
            self.field[i] = mino.mino[i]

    def move_mino_d(self):
        # 毎回呼ばれる、フレームカウントを行う
        self.frames += 1

        """
        active_mino = self.get_active_mino()
        for block in active_mino:
            row = block[0]
            column = block[1]
            self.field[row][column] = 0
        """
        active_mino = self.get_active_mino()

        if self.collide_down(active_mino):
            for block in active_mino:
                row = block[0]
                column = block[1]
                self.field[row][column] = 2
            # 新しいミノを作る
            mino = Mino()
            self.put_mino(mino)
        else:
            for block in active_mino:
                row = block[0]
                column = block[1]
                self.field[row][column] = 0
            # ミノの部分を黒くする
            for block in active_mino:
                row = block[0] + 1
                column = block[1]
                self.field[row][column] = 1

    def collide_down(self, active_mino):
        # 一番下のブロックのどれかしらの次のコードが2（ドロップ済みミノ）だったら衝突
        # 衝突:True 非衝突:False
        # 一番rowが大きいのが一番下
        # 一番下にあるブロックは全てチェックしないといけない→biggest_rowと同一でも確認候補になる
        biggest_row = None
        biggest_row_column = None
        check_list = []
        for block in active_mino:
            row = block[0]
            if biggest_row == None: # first commitment
                biggest_row = row
                biggest_row_column = block[1]
                check_list.append([biggest_row, biggest_row_column])
            else:
                if row == biggest_row: # 同じだったらこいつも入れる
                    check_list.append([row, block[1]])
                if row > biggest_row: # 新しく大きいのが出たら初期化して足す
                    check_list = []
                    biggest_row = row
                    biggest_row_column = block[1]
                    check_list.append([biggest_row, biggest_row_column])

        # rowを一段下げた（row+1）したcolumnの値を確認する
        # フィールドの一番下にきた場合、indexerrorになるので対処する
        #print(type(biggest_row), biggest_row)
        if biggest_row < 19: # 最底部まで行っていない場合はtarget_valueで判断
            collide_other_mino = False
            for block in check_list: # どれか一つでも衝突したらTrue
                row = block[0] + 1
                column = block[1]
                if self.field[row][column] == 2: # 衝突
                    return True
        else: # 最底部まで言っていた場合その時点で衝突判定
            return True

        return False # ミノ衝突判定のfalse

    def get_active_mino(self):
        active_mino = []
        for row in range(self.row_size):
            for column in range(self.column_size):
                if self.field[row][column] == 1:
                    active_mino.append([row, column])
        return active_mino

    def get_left_blocks(self, active_mino):
        # 最も左にあるブロックのインデックスを返す(左の壁かブロックに衝突する可能性があるもの)
        # 一番columnが小さいところ
        smallest_column = None
        left_blocks = []
        for block in active_mino:
            row = block[0]
            column = block[1]
            if smallest_column == None: # first commit
                smallest_column = column
                left_blocks.append([row,column])
            else:
                if column == smallest_column:
                    smallest_column = column
                    left_blocks.append([row, column])
                if column < smallest_column:
                    smallest_column = column
                    left_blocks = []
                    left_blocks.append([row, column])

        return left_blocks

    def get_right_blocks (self, active_mino):
        # 最も右にあるブロックのインデックスを返す(左の壁かブロックに衝突する可能性があるもの)
        biggest_column = None
        right_blocks = []
        for block in active_mino:
            row = block[0]
            column = block[1]
            if biggest_column == None: # first commit
                biggest_column = column
                right_blocks.append([row,column])
            else:
                if column == biggest_column:
                    biggest_column = column
                    right_blocks.append([row, column])
                if column > biggest_column:
                    biggest_column = column
                    right_blocks = []
                    right_blocks.append([row, column])

        return right_blocks

    def move_mino_r(self):
        active_mino = self.get_active_mino() 
        # 確保した座標のcolumnを1増やして１に書き換える
        if not self.collide_right_wall(active_mino) and not self.collide_right_mino(active_mino):
            # 短縮できそうだが下手にいじると、うまく動かないのでこれでいく
            for block in active_mino:
                row = block[0]
                column = block[1]
                self.field[row][column] = 0
            for block in active_mino:
                row = block[0]
                column = block[1] + 1
                self.field[row][column] = 1
        else:
            pass

    def move_mino_l(self):
        active_mino = self.get_active_mino()
        # フィールドのactive_minoだけをリセットする
        # 確保した座標のcolumnを1減らして１に書き換える
        if not self.collide_left_wall(active_mino) and not self.collide_left_mino(active_mino):
            for block in active_mino:
                row = block[0]
                column = block[1]
                self.field[row][column] = 0
            for block in active_mino:
                row = block[0]
                column = block[1] - 1
                self.field[row][column] = 1
        else:
            pass

    def collide_left_mino(self, active_mino):
        left_blocks = self.get_left_blocks(active_mino)
        for left_block in left_blocks:
            row = left_block[0]
            column = left_block[1]
            target_value = self.field[row][column-1]
            if target_value == 2:
                return True
        return False

    def collide_right_mino(self, active_mino):
        right_blocks = self.get_right_blocks(active_mino)
        for right_block in right_blocks:
            row = right_block[0]
            column = right_block[1]
            target_value = self.field[row][column+1]
            if target_value == 2:
                return True
        return False

    def collide_left_wall(self, active_mino):
        # mino_cordsを受け取って左の壁に衝突していないか判定する
        # 衝突:True 非衝突:False
        # columnが一番小さいのが一番左
        smallest_column = None
        for block in active_mino:
            column = block[1]
            if smallest_column == None:
                smallest_column = column
            else:
                if column < smallest_column:
                    smallest_column = column
        # 壁の衝突判定
        if smallest_column == 0:
            return True
        else:
            return False

    def collide_right_wall(self, active_mino):
        # mino_cordsを受け取って右の壁に衝突していないか判定する
        # 衝突:True 非衝突:False
        # columnが一番大きいのが一番右
        right_blocks = self.get_right_blocks(active_mino)
        bigggest_column = None
        for block in active_mino:
            column = block[1]
            if bigggest_column == None:
                bigggest_column = column
            else:
                if column > bigggest_column:
                    bigggest_column = column
        if bigggest_column == 9:
            return True
        else:
            return False

    def check(self):
        cnt = 0
        for row in self.field:
            print(row)
        print()

    def get_clear_line_rows(self):
        # allは[2,2,1]でもTrueになってしまうので使えない
        # 全てのcolumnが2のrow_indexを返す 
        clear_lines = []
        for i in range(self.row_size):
            if all([column==2 for column in self.field[i]]):
                clear_lines.append(i)
        return clear_lines 

    def diff_to_theta(self, diffs): #recv array
        ret = []
        for diff in diffs:
            if diff == 0:
                ret.append("=")
            elif diff < 0:
                ret.append("-")
            else:
                ret.append("+")

        diff_to_theta = {
            0:["=", "+"],
            45:["+", "+"],
            90:["+", "="],
            135:["+", "-"],
            180:["=", "-"],
            225:["-", "-"],
            270:["-", "="],
            315:["-", "+"]
        }
        for theta in diff_to_theta.keys():
            pattern = diff_to_theta[theta]
            if pattern == ret:
                return theta
        return False

    def diff_to_radius(self, diffs):
        # 半径は正になるので、符号はあまり気にせず絶対値として考える
        # 対角線上を取るパターンはZとSの時だけ

        # 対角線上のパターン
        if all(diffs):
            return math.sqrt(2)
        else:
        # 対角線上ではないパターン
            return max(map(abs, diffs)) #diffsは負の数を含むことがあるため、絶対値を取っておく

    def rotate_r(self):
        active_mino = self.get_active_mino()
        #print(active_mino)
        #mino_center_index = self.mino_center_index
        try:
            mino_center_index = self.mino.mino_center_indexs[self.mino.mino_type][self.mino.rotate_cnt]
            mino_center_block = active_mino[mino_center_index]
        except TypeError: # in case of O mino, skip
            return 
        #print("mino_center_index:{}".format(mino_center_index))

        center_row = mino_center_block[0]
        center_col = mino_center_block[1]
        center_diffs = []
        rotated = []
        for index, block in enumerate(active_mino):
            row = block[0]
            col = block[1]
            if index != mino_center_index:
                row_diff = row - center_row
                col_diff = col - center_col
                # calc diffs
                diffs = [row_diff, col_diff]
                # calc theta
                theta = self.diff_to_theta(diffs)
                # calc radius
                radius = self.diff_to_radius(diffs)
                # rotate
                theta_dst = theta + 90
                # angle adjustment
                if theta_dst >= 360:
                    theta_dst = theta_dst - 360
                # calc cord after rotation
                if theta in [0,90,180,270]:
                    x_delta = abs( int( pyxel.cos(theta_dst) * radius ) )
                    y_delta = abs( int( pyxel.sin(theta_dst) * radius ) )
                    if theta == 0:
                        col = center_col - x_delta
                        row = center_row + y_delta
                    elif theta == 90:
                        col = center_col - x_delta
                        row = center_row - y_delta
                    elif theta == 180:
                        col = center_col + x_delta
                        row = center_row - y_delta
                    elif theta == 270:
                        row = center_row + y_delta
                        col = center_col + x_delta
                elif theta in [45,135,225,315]:
                    x_delta = abs( int( pyxel.cos(theta_dst) * radius * math.sqrt(2) ) )
                    y_delta = abs( int( pyxel.sin(theta_dst) * radius * math.sqrt(2) ) )
                    if theta == 45:
                        col = center_col - x_delta
                        row = center_row + y_delta
                    elif theta == 135:
                        col = center_col - x_delta
                        row = center_row - y_delta
                    elif theta == 225:
                        col = center_col + x_delta
                        row = center_row - y_delta
                    elif theta == 315:
                        row = center_row + y_delta
                        col = center_col + x_delta
                else:
                    x_delta = None
                    y_delta = None 
                #print(block, center_block, "theta:{}, theta_dst:{}, radius:{}, diffs:[{},{}], x_delta:{}, y_delta:{}".format(theta, theta_dst, radius, diffs[0], diffs[1], x_delta, y_delta))
                rotated.append([row, col])
            else:
                rotated.append([row, col])

        # rotation available judge
        # if dst value is lower than 0 -> False
        for block in rotated:
            row = block[0]
            col = block[1]
            if (col >= 0 and col < 10) and (row >= 0 and row < 20):
                # other blocks collision
                if self.field[row][col] == 2:
                    return
            else: # rotation not available
                print(row,col,"rotate is not available")
                return
        # 描画 
        # active_minoを消して新しい座標を更新する
        for block in active_mino:
            row = block[0]
            column = block[1]
            self.field[row][column] = 0
        # draw rotated blocks
        for block in rotated:
            row = block[0]
            column = block[1]
            self.field[row][column] = 1
        # update rorate_cnt
        self.mino.rotate_cnt += 1
        if self.mino.rotate_cnt == 4: # maxium 4 times -> max 3 for index
            self.mino.rotate_cnt = 0

# 動くミノは一つだけ
# 着地したものはミノとは別の扱いをする

class App:
    def __init__(self):
        pyxel.init(200,200)

        # change color
        # pyxel.colors[12] = 0x82FC10

        self.row_size = 20
        self.column_size = 10

        # field
        self.field = Field()
        #print(self.field.cords)
        # self.field.reset_field()

        # frame info
        self.current_frame = 0

        #mino = Mino()
        #self.field.put_mino(mino)
        #self.field.check()

        # speed variables
        self.refresh_speed = 10
        self.operation_speed = 3

        # score
        self.score = 0
        self.bonus_type = None
        self.bonus_types = {
            0:[None,0],
            1:["single",100],
            2:["double",200*2],
            3:["triple",300*3],
            4:["tetris",400*4]
        }
        self.bonus_frames = 0
        self.cleared_lines = 0

        self.game_over = False
        self.game_clear = False
        self.start_screen = True

        pyxel.run(self.update, self.draw)

    def update(self):
        if self.start_screen:
            # wait for enter to start game
            pass
        else:
            if not self.game_over and not self.game_clear:
                #self.field.check()
                self.current_frame += 1 
                # move mino
                if self.current_frame % self.refresh_speed == 0:
                    self.field.move_mino_d() #  drop
                    clear_line_rows = self.field.get_clear_line_rows() # row index
                    self.cleared_lines += len(clear_line_rows)
                    print("cleared_line",self.cleared_lines)
                    # clear lines
                    bonus = self.bonus_types[len(clear_line_rows)]
                    self.bonus_type = bonus[0]
                    for clear_line_row in clear_line_rows:
                        self.field.field.pop(clear_line_row)
                        self.field.field.insert(0, [0 for i in range(10)])
                        # update score
                        self.score += bonus[1] # 100 points for each line

                if self.current_frame % self.operation_speed == 0:
                    if pyxel.btn(pyxel.KEY_RIGHT):
                        self.field.move_mino_r()
                    elif pyxel.btn(pyxel.KEY_LEFT):
                        self.field.move_mino_l()
                    elif pyxel.btn(pyxel.KEY_UP):
                        #print("rotate_r")
                        self.field.rotate_r()
                    elif pyxel.btn(pyxel.KEY_DOWN):
                        #print("pressed")
                        self.refresh_speed = 2
                    elif not pyxel.btn(pyxel.KEY_DOWN):
                        #print("released")
                        self.refresh_speed = 10

                # game clear judge
                if self.cleared_lines >= 2:
                    self.game_clear = True

                # game over judge
                # if block exist in first 3 arrays game over
                for i in range(3):
                    row = self.field.field[i]
                    if 2 in row:
                        self.game_over = True

        """
        elif pyxel.btn(pyxel.KEY_SPACE):
            self.change_mino()
        """

    def draw(self):
        pyxel.cls(7)
        if self.start_screen:
            # wait for enter key to start game
            # draw tetris
            cnt = 0
            for i in range(2):
                self.field.field[i] = [0 for i in range(10)]

            for row in range(self.row_size):
                for column in range(self.column_size):
                    cord = self.field.cords[row][column]
                    color = self.field.field[row][column]
                    color = pyxel.rndi(0,10)
                    # draw blocks
                    pyxel.rect(cord[1], cord[0], cord[2], cord[3], color)
                cnt += 1
            pyxel.text(85, 100, "TETRIS", 0)
            pyxel.text(60, 120, "Press Enter To Start", 0)
            if pyxel.btnp(pyxel.KEY_SPACE):
                print("space")
                self.start_screen = False
                mino = Mino()
                self.field.put_mino(mino)
        else:
            if not self.game_clear and not self.game_over:
                # draw score
                pyxel.text(1,1, "SCORE:\n{}".format(self.score),0)
                # draw field
                cnt = 0
                for row in range(self.row_size):
                    for column in range(self.column_size):
                        cord = self.field.cords[row][column]
                        color = self.field.field[row][column]
                        if color == 1:
                            color = mino_color[-1]
                        elif color == 2:
                            color = 13
                        # draw blocks
                        pyxel.rect(cord[1], cord[0], cord[2], cord[3], color)
                    cnt += 1

                # draw over line
                x = 46
                y = 29
                pyxel.line(x,y,x+99,y, 8)

                # bonus cut-in
                if self.bonus_type != None:
                    # show cut-in text for 5 frames
                    pyxel.text(90,100, self.bonus_type, 8)
                    self.bonus_frames += 1
                    if self.bonus_frames == 1000:
                        self.bonus_frames = 0
                        self.bonus_type = None

            elif self.game_over:
                pyxel.text(100,100, "GAME OVER",0)
            elif self.game_clear:
                pyxel.text(100,100, "GAME CLEAR",0)


if __name__ == "__main__":
    App()
