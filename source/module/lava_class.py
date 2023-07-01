import pyxel

class Lava:
    def __init__(self, x, y, mp):
        self.x = x
        self.y = y
        self.move_parmit = mp
        self.move_parmit_count_max = 25
        self.water = (0, 2)

    def update(self, mine):
        self.move_parmit_count_max -= 1
        if self.move_parmit_count_max < 1:
            self.move_parmit_count_max = 25

            if pyxel.tilemap(0).pget(self.x, self.y - 1) in self.move_parmit:
                self.cng_tile((self.x, self.y - 1), 0, mine) 
                return (self.x, self.y - 1)
            elif pyxel.tilemap(0).pget(self.x, self.y - 1) == self.water:
                self.cng_tile((self.x, self.y), 1, mine) 
                return False
           
            if pyxel.tilemap(0).pget(self.x, self.y + 1) in self.move_parmit:
                self.cng_tile((self.x, self.y + 1), 0, mine) 
                return (self.x, self.y + 1)
            elif pyxel.tilemap(0).pget(self.x, self.y + 1) == self.water:
                self.cng_tile((self.x, self.y), 1, mine) 
                return False
            
            if pyxel.tilemap(0).pget(self.x - 1, self.y) in self.move_parmit:
                self.cng_tile((self.x - 1, self.y), 0, mine) 
                return (self.x - 1, self.y)
            elif pyxel.tilemap(0).pget(self.x - 1, self.y) == self.water:
                self.cng_tile((self.x, self.y), 1, mine) 
                return False            

            if pyxel.tilemap(0).pget(self.x + 1, self.y) in self.move_parmit:
                self.cng_tile((self.x + 1, self.y), 0, mine) 
                return (self.x + 1, self.y)
            elif pyxel.tilemap(0).pget(self.x + 1, self.y) == self.water:
                self.cng_tile((self.x, self.y), 1, mine) 
                return False            
        else:
            pass

    def cng_tile(self, tile, t, mine):     
        if t == 0:
            #溶岩を追加
            if pyxel.rndi(0, 10) == 10:
                #確率で溶岩の目に変異
                pyxel.tilemap(0).pset(tile[0], tile[1], (1, 3))
            else:
                pyxel.tilemap(0).pset(tile[0], tile[1], (1, 2))
        elif t == 1:
            #隣接するマスが水の場合は固まる
            pyxel.tilemap(0).pset(tile[0], tile[1], (3, 0))
            
