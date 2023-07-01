import pyxel

class SelectBox:
    def __init__(self, x, y, items):
        self.x = x
        self.y = y
        self.select_x = 0
        self.select_y = 0
        self.sel = 1
        self.items = items       
        self.creation_det = self.items[self.select_y][self.select_x][0] + ", Need Creation Points: " + \
                                str(self.items[self.select_y][self.select_x][1])        

    def move_up(self):        
        if self.select_y > 0:
            pyxel.play(3,10)
            self.select_y -= 1
            self.creation_det = self.items[self.select_y][self.select_x][0] + ", Need Creation Points: " + \
                                str(self.items[self.select_y][self.select_x][1])
        if self.items[self.select_y][self.select_x][0] == "":
            self.creation_det = ""
        return self.creation_det

    def move_down(self):        
        if self.select_y < 2:
            pyxel.play(3,10)
            self.select_y += 1
            self.creation_det = self.items[self.select_y][self.select_x][0] + ", Need Creation Points: " + \
                                str(self.items[self.select_y][self.select_x][1])       
        if self.items[self.select_y][self.select_x][0] == "":
            self.creation_det = ""                        
        return self.creation_det            

    def move_left(self):        
        if self.select_x > 0:
            pyxel.play(3,10)
            self.select_x -= 1
            self.creation_det = self.items[self.select_y][self.select_x][0] + ", Need Creation Points: " + \
                                str(self.items[self.select_y][self.select_x][1])       
        if self.items[self.select_y][self.select_x][0] == "":
            self.creation_det = ""                        
        return self.creation_det            

    def move_right(self):        
        if self.select_x < 3:
            pyxel.play(3,10)
            self.select_x += 1
            self.creation_det = self.items[self.select_y][self.select_x][0] + ", Need Creation Points: " + \
                                str(self.items[self.select_y][self.select_x][1])       
        if self.items[self.select_y][self.select_x][0] == "":
            self.creation_det = ""            
        return self.creation_det            