import pyxel

class Lavamonster:
    def __init__(self, x, y):
        self.x = x
        self.y = y        
        self.move_parmit_count_max = 30
        self.move_count = 5
        self.rock = (0, 5)

    def update(self):
        self.move_parmit_count_max -= 1
        angle = pyxel.rndi(0, 3)
        if self.move_parmit_count_max < 1:
            self.move_parmit_count_max = 30
            a = angle
            if a == 1:
                if pyxel.tilemap(0).pget(self.x - 1, self.y) == self.rock:
                    pass
                else:
                    self.x -= 1
                    if self.move_count_update():
                        return (self.x, self.y)
            elif a == 2:
                if pyxel.tilemap(0).pget(self.x + 1, self.y) == self.rock:
                    pass
                else:
                    self.x += 1
                    if self.move_count_update():
                        return (self.x, self.y)
            elif a == 3:
                if pyxel.tilemap(0).pget(self.x, self.y - 1) == self.rock:
                    pass
                else:
                    self.y -= 1
                    if self.move_count_update():
                        return (self.x, self.y)
            elif a == 4:
                if pyxel.tilemap(0).pget(self.x, self.y + 1) == self.rock:
                    pass
                else:
                    self.y += 1
                    if self.move_count_update():
                        return (self.x, self.y)

    def move_count_update(self):
        self.move_count -= 1
        if self.move_count < 1:
            #カウントがゼロになった際に自分のいるマスを溶岩に変える
            pyxel.tilemap(0).pset(self.x, self.y, (1, 2))   
            return True
        else:
            return False         
