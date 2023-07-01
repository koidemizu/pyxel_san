import pyxel

class Lavaeye:
    def __init__(self, x, y):
        self.x = x
        self.y = y        
        self.move_parmit_count_max = 30 * 10

    def update(self):
        self.move_parmit_count_max -= 1
        if self.move_parmit_count_max < 1:
            self.move_parmit_count_max = 30 * 10
            return True
        else:
            False