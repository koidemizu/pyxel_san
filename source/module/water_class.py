import pyxel

class Water:
    def __init__(self, x, y, mp):
        self.x = x
        self.y = y
        self.move_parmit = mp
        self.move_parmit_count_max = 25

    def update(self):
        self.move_parmit_count_max -= 1
        if self.move_parmit_count_max < 1:
            self.move_parmit_count_max = 25

            if pyxel.tilemap(0).pget(self.x, self.y - 1) in self.move_parmit:
               self.cng_tile((self.x, self.y - 1)) 
               return (self.x, self.y - 1)
           
            if pyxel.tilemap(0).pget(self.x, self.y + 1) in self.move_parmit:
               self.cng_tile((self.x, self.y + 1)) 
               return (self.x, self.y + 1)

            if pyxel.tilemap(0).pget(self.x - 1, self.y) in self.move_parmit:
               self.cng_tile((self.x - 1, self.y)) 
               return (self.x - 1, self.y)

            if pyxel.tilemap(0).pget(self.x + 1, self.y) in self.move_parmit:
               self.cng_tile((self.x + 1, self.y)) 
               return (self.x + 1, self.y)
        else:
            pass

    def cng_tile(self, tile):     
        if pyxel.tilemap(0).pget(tile[0], tile[1]) in ((0, 7), (1, 7), (2, 7),(0, 8), (1, 8), (2, 8)):
            if pyxel.rndi(0, 10) == 10:
                #確率で水の目に変異
                pyxel.tilemap(0).pset(tile[0], tile[1], (0, 3))
            else:
                pyxel.tilemap(0).pset(tile[0], tile[1], (pyxel.rndi(4, 6), 8))            
        else:
            if pyxel.rndi(0, 10) == 10:
                #確率で水の目に変異
                pyxel.tilemap(0).pset(tile[0], tile[1], (0, 3))
            else:
                pyxel.tilemap(0).pset(tile[0], tile[1], (0, 2))
