import pyxel

class Human:
    def __init__(self, x, y, tx, ty, mp):
        self.x = x
        self.y = y
        self.target_x = tx
        self.target_y = ty
        self.rock = ((0, 0), (0, 1), (2, 0), (3, 0), (3, 1), (3, 2))        
        self.move_parmit = mp
        self.move_parmit_count = 0
        self.move_parmit_count_max = pyxel.rndi(30, 60)
        self.kinoko_rock = 0
        self.fail_count = 0
        self.fail_max = 2
        self.mine_pow = 1
        self.insight = pyxel.rndi(0, 5)
        self.flag_p = []
        self.type = 0
        self.flag_chk()
        
      
    def target_set(self, tx, ty):
        self.target_x = tx
        self.target_y = ty

    def flag_chk(self):        
        if self.type == 0:
            flag_type = (3, 6)
        elif self.type == 1:
            flag_type = (4, 6)
        elif self.type == 2:
            flag_type = (5, 6)
        else:
            flag_type = (99, 99)
        for i1 in range(32):
            for i2 in range(32):
                if pyxel.tilemap(0).pget(i1, i2) == flag_type:
                    self.flag_p = [i1, i2]
                    return True
        self.flag_p = []
        return False
                

    def flag_end_chk(self):        
        if pyxel.tilemap(0).pget(self.x, self.y) in ((3, 6), (4, 6), (5, 6)):
            pyxel.tilemap(0).pset(self.x, self.y, (0, 6))

    def kinoko_chk(self):        
        if pyxel.tilemap(0).pget(self.x, self.y) == (3, 7):
            return True            
        
    def kinoko_chk2(self):        
        if pyxel.tilemap(0).pget(self.x, self.y) == (3, 8):
            return True                    

    def update(self, player, effect, g_pos, num):
        #普通のHumanの場合----------------------------------------------------
        if self.type == 0:
            self.flag_end_chk()

            if ((self.target_x == self.x and self.target_y == self.y) or
                (self.fail_count > self.fail_max)):            
                if self.flag_chk():
                    #旗がある場合の目的地設定
                    x1 = self.flag_p[0] - self.insight
                    y1 = self.flag_p[1] - self.insight
                    x2 = self.flag_p[0] + self.insight
                    y2 = self.flag_p[1] + self.insight
                else:
                    #通常の目的地再設定
                    x1 = 1
                    y1 = 1
                    x2 = 28
                    y2 = 28
                self.target_set(pyxel.rndi(x1, x2), pyxel.rndi(y1, y2))

            self.move_parmit_count += 1
            if self.move_parmit_count + num > self.move_parmit_count_max:
                if self.x < self.target_x:
                    self.move_right(player, effect, g_pos)
                elif self.x > self.target_x:
                    self.move_left(player, effect, g_pos)

                if self.y < self.target_y:
                    self.move_down(player, effect, g_pos)
                elif self.y > self.target_y:
                    self.move_up(player, effect, g_pos)
        #赤のHumanの場合--------------------------------------------------------------
        elif self.type == 1:
            self.flag_end_chk()
            #赤のHumanは直感とパワーを高に
            self.insight = 0
            self.mine_pow = pyxel.rndi(15, 25)
            if ((self.target_x == self.x and self.target_y == self.y) or
                (self.fail_count > self.fail_max)):            
                if self.flag_chk():
                    #旗がある場合の目的地設定
                    x1 = self.flag_p[0] - self.insight
                    y1 = self.flag_p[1] - self.insight
                    x2 = self.flag_p[0] + self.insight
                    y2 = self.flag_p[1] + self.insight
                else:
                    #通常の目的地再設定
                    x1 = 1
                    y1 = 1
                    x2 = 28
                    y2 = 28
                self.target_set(pyxel.rndi(x1, x2), pyxel.rndi(y1, y2))

            self.move_parmit_count += 1
            if self.move_parmit_count + num > self.move_parmit_count_max:
                if self.x < self.target_x:
                    self.move_right_red(player, effect, g_pos)
                elif self.x > self.target_x:
                    self.move_left_red(player, effect, g_pos)

                if self.y < self.target_y:
                    self.move_down_red(player, effect, g_pos)
                elif self.y > self.target_y:
                    self.move_up_red(player, effect, g_pos)
        #緑のHumanの場合---------------------------------------------------------------            
        elif self.type == 2:
            self.flag_end_chk()

            if ((self.target_x == self.x and self.target_y == self.y) or
                (self.fail_count > self.fail_max)):            
                if self.flag_chk():
                    #旗がある場合の目的地設定
                    x1 = self.flag_p[0] - self.insight
                    y1 = self.flag_p[1] - self.insight
                    x2 = self.flag_p[0] + self.insight
                    y2 = self.flag_p[1] + self.insight
                else:
                    #通常の目的地再設定
                    x1 = 1
                    y1 = 1
                    x2 = 28
                    y2 = 28
                self.target_set(pyxel.rndi(x1, x2), pyxel.rndi(y1, y2))

            self.move_parmit_count += 1
            if self.move_parmit_count + num > self.move_parmit_count_max:
                if self.x < self.target_x:
                    self.move_right(player, effect, g_pos)
                elif self.x > self.target_x:
                    self.move_left(player, effect, g_pos)

                if self.y < self.target_y:
                    self.move_down(player, effect, g_pos)
                elif self.y > self.target_y:
                    self.move_up(player, effect, g_pos)
        #白のHumanの場合---------------------------------------------------------------            
        elif self.type == 3:
            self.flag_end_chk()

            if ((self.target_x == self.x and self.target_y == self.y) or
                (self.fail_count > self.fail_max)):            
                if self.flag_chk():
                    #旗がある場合の目的地設定
                    x1 = self.flag_p[0] - self.insight
                    y1 = self.flag_p[1] - self.insight
                    x2 = self.flag_p[0] + self.insight
                    y2 = self.flag_p[1] + self.insight
                else:
                    #通常の目的地再設定
                    x1 = 1
                    y1 = 1
                    x2 = 28
                    y2 = 28
                self.target_set(pyxel.rndi(x1, x2), pyxel.rndi(y1, y2))

            self.move_parmit_count += 1
            if self.move_parmit_count + num > self.move_parmit_count_max:
                if self.x < self.target_x:
                    self.move_right(player, effect, g_pos)
                elif self.x > self.target_x:
                    self.move_left(player, effect, g_pos)

                if self.y < self.target_y:
                    self.move_down(player, effect, g_pos)
                elif self.y > self.target_y:
                    self.move_up(player, effect, g_pos)                    



    def move_common(self, n1, n2, player, effect, g_pos):
        #進行可能な場合
        if (pyxel.tilemap(0).pget(self.x + n1, self.y + n2)) in self.move_parmit:
            return True
        #障害物がある場合
        else:
            self.fail_count += 1
            #ランダム確立で岩を壊せる。mine_powが高いほど壊しやすくなる。
            #埋蔵物があるかの判定を一括してここで行う
            g_pos_flag = False
            if [self.x + n1, self.y + n2] in g_pos:
                g_pos_flag = True
            if (pyxel.tilemap(0).pget(self.x + n1, self.y + n2)) in self.rock:
                if pyxel.rndi(0, 50) <= self.mine_pow:
                    self.fail_count = 0
                    #通常の岩
                    if pyxel.tilemap(0).pget(self.x + n1, self.y + n2) == (0, 0):
                        for ea in range(5):
                            effect.append(Effect(self.x + n1, self.y + n2, 13))                        
                        pyxel.tilemap(0).pset(self.x + n1, self.y + n2, (0, 1))  
                    elif pyxel.tilemap(0).pget(self.x + n1, self.y + n2) == (0, 1):  
                        if g_pos_flag == False:
                            pyxel.tilemap(0).pset(self.x + n1, self.y + n2, (0, 6))
                        else:
                            pyxel.tilemap(0).pset(self.x + n1, self.y + n2, (pyxel.rndi(0, 4), 9))
                        for ea in range(5):
                            effect.append(Effect(self.x + n1, self.y + n2, 13))  
                    #泥の岩                            
                    elif pyxel.tilemap(0).pget(self.x + n1, self.y + n2) == (2, 0):  
                        if g_pos_flag == False:
                            pyxel.tilemap(0).pset(self.x + n1, self.y + n2, (0, 6))      
                        else:
                            pyxel.tilemap(0).pset(self.x + n1, self.y + n2, (pyxel.rndi(0, 4), 9))      
                        for ea in range(5):
                            effect.append(Effect(self.x + n1, self.y + n2, 4))                                                
                    #溶岩が冷えた岩
                    elif pyxel.tilemap(0).pget(self.x + n1, self.y + n2) == (3, 0):  
                        pyxel.tilemap(0).pset(self.x + n1, self.y + n2, (3, 1))      
                        for ea in range(5):
                            effect.append(Effect(self.x + n1, self.y + n2, 1))                                
                    elif pyxel.tilemap(0).pget(self.x + n1, self.y + n2) == (3, 1):  
                        pyxel.tilemap(0).pset(self.x + n1, self.y + n2, (3, 2))      
                        for ea in range(5):
                            effect.append(Effect(self.x + n1, self.y + n2, 1))                                                            
                    elif pyxel.tilemap(0).pget(self.x + n1, self.y + n2) == (3, 2):  
                        pyxel.tilemap(0).pset(self.x + n1, self.y + n2, (0, 6))     
                        if pyxel.rndi(1, 3) == 1:
                            for ea in range(pyxel.rndi(5, 10)):
                                effect.append(Effect(self.x + n1, self.y + n2, pyxel.rndi(9, 10))) 
                                player.cost += 5 
                        else:
                            for ea in range(5):
                                effect.append(Effect(self.x + n1, self.y + n2, 1))                          
                    #岩を壊すとプレイヤーのコストが回復
                    player.cost += 5
                    #mine_powが上がる(上限40)
                    if self.mine_pow < 40:
                        self.mine_pow += pyxel.rndi(1, 5)
                    #行動までの待機時間が下がる(上限15)
                    if self.move_parmit_count_max > 15:
                        self.move_parmit_count_max -= 1                            
            return False

    #通常のHuman行動ロジック
    def move_up(self, player, effect, g_pos):
        self.move_parmit_count = 0
        if self.move_common(0, -1, player, effect, g_pos):
            self.y -= 1

    def move_down(self, player, effect, g_pos):
        self.move_parmit_count = 0
        if self.move_common(0, 1, player, effect, g_pos):
            self.y += 1

    def move_left(self, player, effect, g_pos):
        self.move_parmit_count = 0
        if self.move_common(-1, 0, player, effect, g_pos):
            self.x -= 1

    def move_right(self, player, effect, g_pos):
        self.move_parmit_count = 0
        if self.move_common(1, 0, player, effect, g_pos):
            self.x += 1

    #赤のHuman行動ロジック
    def move_up_red(self, player, effect, g_pos):
        self.move_parmit_count = 0
        if self.move_common(0, -1, player, effect, g_pos):
            if pyxel.rndi(0, 4 + self.kinoko_rock) == 0:
                if [self.x, self.y] in g_pos:
                    pass
                else:
                    pyxel.tilemap(0).pset(self.x, self.y, (2, 0))
                self.kinoko_rock += 2
            self.y -= 1

    def move_down_red(self, player, effect, g_pos):
        self.move_parmit_count = 0
        if self.move_common(0, 1, player, effect, g_pos):
            if pyxel.rndi(0, 4 + self.kinoko_rock) == 0:
                if [self.x, self.y] in g_pos:
                    pass
                else:
                    pyxel.tilemap(0).pset(self.x, self.y, (2, 0))
                self.kinoko_rock += 2
            self.y += 1

    def move_left_red(self, player, effect, g_pos):
        self.move_parmit_count = 0
        if self.move_common(-1, 0, player, effect, g_pos):
            if pyxel.rndi(0, 4 + self.kinoko_rock) == 0:
                if [self.x, self.y] in g_pos:
                    pass
                else:
                    pyxel.tilemap(0).pset(self.x, self.y, (2, 0))
                self.kinoko_rock += 2
            self.x -= 1

    def move_right_red(self, player, effect, g_pos):
        self.move_parmit_count = 0
        if self.move_common(1, 0, player, effect, g_pos):
            if pyxel.rndi(0, 4 + self.kinoko_rock) == 0:
                if [self.x, self.y] in g_pos:
                    pass
                else:
                    pyxel.tilemap(0).pset(self.x, self.y, (2, 0))
                self.kinoko_rock += 2
            self.x += 1            
    #緑のHuman行動ロジック

class Effect:
    def __init__(self, x, y, c, v=0):
        self.ef_x = x
        self.ef_y = y
        self.ef_x2 = pyxel.rndi(-10, 10)
        self.ef_y2 = pyxel.rndi(-10, 10)
        self.ef_t = 10
        self.ef_v = v
        self.col = c
        
    def update(self):
        self.ef_t -= 1
        self.ef_x += self.ef_x2 / 100
        self.ef_y += self.ef_y2 / 100           