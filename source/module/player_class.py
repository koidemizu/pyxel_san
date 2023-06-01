import pyxel

class Player:
    def __init__(self, x, y,):
        self.x = x
        self.y = y
        self.col_count = 0
        self.col_flag = 1
        self.col_count_max = 40
        self.move_limit = 0
        self.move_limit_flag = False
        self.move_limit_x = 28
        self.move_limit_y = 29
        self.cost = 899

    def update(self):
        if pyxel.frame_count % 300 == 0:
            self.add_cost(1)
        self.move_limit += 1
        if self.move_limit > 6:
            self.move_limit_flag = True
        self.col_count += 1
        if self.col_count > self.col_count_max:
            self.col_flag += 1
            self.col_count = 0
   
    def check_cost(self, n):
        if self.cost - n >= 0:
            return True
        else:
            return False 

    def add_cost(self, n):
        self.cost += n

    def use_cost(self, n):
        self.cost -= n

    def move_up(self):        
        if self.y > 0 and self.move_limit_flag == True:
            self.y -= 1
            self.move_limit = 0
            self.move_limit_flag = False
            pyxel.play(3,0)

    def move_down(self):        
        if self.y < self.move_limit_y and self.move_limit_flag == True:
            self.y += 1
            self.move_limit = 0
            self.move_limit_flag = False
            pyxel.play(3,0)

    def move_left(self):        
        if self.x > 0 and self.move_limit_flag == True:
            self.x -= 1
            self.move_limit = 0
            self.move_limit_flag = False
            pyxel.play(3,0)

    def move_right(self):        
        if self.x < self.move_limit_x and self.move_limit_flag == True:
            self.x += 1
            self.move_limit = 0
            self.move_limit_flag = False
            pyxel.play(3,0)