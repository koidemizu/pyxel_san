import pyxel
import json
from module import player_class, human_class, selectbox_class, map_create

class App:
    def __init__(self):
        # 画面の初期化
        pyxel.init(232, 256, fps = 30,)
       
        #音楽データの読み込み
        with open(f"assets/music.json", "rt",encoding="utf-8") as fin:
            self.music = json.loads(fin.read())
        #再生
        if pyxel.play_pos(0) is None:
            for ch, sound in enumerate(self.music):                
                pyxel.sound(ch).set(*sound)
                pyxel.play(ch, ch, loop=True)        

        # リソースの読み込み
        pyxel.load("assets/assets.pyxres")        

        #マップデータの作成
        self.map_data = map_create.MAP_CREATE()
        for m1 in range(len(self.map_data)):
            for m2 in range(len(self.map_data[m1])):
                pyxel.tilemap(0).pset(m2, m1, self.map_data[m1][m2])
   
        #各種変数・インスタンスの準備
        self.player = player_class.Player(1, 1)
        self.humans = []
        self.select_input_flag = False       
        self.indestructible = ((0, 5), (3, 7))
        self.rock = ((0, 0), (0, 1), (2, 0)) 
        self.move_parmit = ((0, 6),)
        self.creation_det = ""
        self.kinoko = False
        self.kinoko_list = ((0, 7), (1, 7), (2, 7),
                            (0, 8), (1, 8), (2, 8))
        self.effects = []
        self.g_pos = []
 
        #埋蔵物があるマスを設定
        g_cnt = 0
        while g_cnt < 5:
            g_pos1 = pyxel.rndi(1, 28)
            g_pos2 = pyxel.rndi(1, 28)
            if pyxel.tilemap(0).pget(g_pos1, g_pos2) in self.rock:                   
                new_g_pos = (g_pos1, g_pos2)
                self.g_pos.append(new_g_pos)
                g_cnt += 1        

        # ゲームループの開始
        pyxel.run(self.update, self.draw)

    def update(self):        
        self.game_update()

    def game_update(self):
        if pyxel.btnp(pyxel.KEY_A):  
            print(self.g_pos)

        if self.select_input_flag == False:
            # プレイヤー(カーソル)の移動
            if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):                  
                self.player.move_left()

            elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):            
                self.player.move_right()        

            elif pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):            
                self.player.move_up()            
            
            elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):            
                self.player.move_down()        

            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X): 
                items = [[("Ground", 2), ("Flag", 1), ("", 0)] ,
                         [("Rock1", 2), ("Rock2", 2), ("", 0)],
                         [("Human", 10), ("", 0), ("", 0)]]
                if self.kinoko == True:
                    items[0][2] = ("Mushroom", 5)
                
                self.select_box = selectbox_class.SelectBox(self.player.x, self.player.y, items)
                self.select_input_flag = True
                self.creation_det = self.select_box.creation_det

            for i in self.humans:
                #岩と重なっている場合はHumanを削除
                if pyxel.tilemap(0).pget(i.x, i.y) in self.rock:
                    self.humans.remove(i)
                i.update(self.player, self.effects, self.g_pos)       
                #きのこを食べるとHumanが増える
                if pyxel.tilemap(0).pget(i.x, i.y) in self.kinoko_list:
                    new_human = human_class.Human(i.x, i.y, pyxel.rndi(1, 28), pyxel.rndi(1, 28))
                    if pyxel.rndi(0, 2) == 0:
                        tgt_ms = pyxel.tilemap(0).pget(i.x, i.y)[1]
                        if tgt_ms == 7:
                            new_human.type = 1
                        elif tgt_ms == 8:
                            new_human.type = 2
                    self.humans.append(new_human)
                    pyxel.tilemap(0).pset(i.x, i.y, (0, 6))

                if i.kinoko_chk():
                    self.kinoko = True

            for e in self.effects:
                e.update()
                if e.ef_t < 0:
                    self.effects.remove(e)

        else:
            # アイテムウィンドウの移動            
            if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):                        
                self.creation_det = self.select_box.move_left()

            elif pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):           
                self.creation_det = self.select_box.move_right()        

            elif pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):           
                self.creation_det = self.select_box.move_up()            
            
            elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):          
                self.creation_det = self.select_box.move_down() 

            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X): 
                self.select_input_flag = False
                self.creation_det = ""
                del self.select_box                
           
            if pyxel.btnp(pyxel.KEY_N) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A): 
                item = self.select_box.items[self.select_box.select_y][self.select_box.select_x][0]
                item_cost = self.select_box.items[self.select_box.select_y][self.select_box.select_x][1]
                #Humanの投下
                if item == "Human":                    
                    if pyxel.tilemap(0).pget(self.player.x, self.player.y) in self.move_parmit:
                        if self.player.check_cost(item_cost):
                            new_human = human_class.Human(self.player.x, self.player.y, pyxel.rndi(1, 28), pyxel.rndi(1, 28))
                            self.humans.append(new_human)
                            self.player.use_cost(item_cost)
                #道の設置
                elif item == "Ground":
                    if pyxel.tilemap(0).pget(self.player.x, self.player.y) in self.indestructible:
                        pass
                    else:
                        if self.player.check_cost(item_cost):
                            pyxel.tilemap(0).pset(self.player.x, self.player.y, (0, 6))
                            self.player.use_cost(item_cost)
                #きのこ土地の設置
                elif item == "Mushroom":
                    if pyxel.tilemap(0).pget(self.player.x, self.player.y) in self.move_parmit:
                        if self.player.check_cost(item_cost):
                            pyxel.tilemap(0).pset(self.player.x, self.player.y, (pyxel.rndi(0, 2), 7))
                            self.player.use_cost(item_cost)                            
                #岩の設置
                elif item == "Rock1":
                    if pyxel.tilemap(0).pget(self.player.x, self.player.y) in self.indestructible:
                        pass
                    else:
                        if self.player.check_cost(item_cost):
                            pyxel.tilemap(0).pset(self.player.x, self.player.y, (0, 0))
                            self.player.use_cost(item_cost)
                #壊せない岩の設置
                elif item == "Rock2":                    
                    if pyxel.tilemap(0).pget(self.player.x, self.player.y) in self.indestructible:
                        pass
                    else:
                        if self.player.check_cost(item_cost):
                             pyxel.tilemap(0).pset(self.player.x, self.player.y, (1, 0))        
                             self.player.use_cost(item_cost)
                #旗の設置
                elif item == "Flag":                    
                    if pyxel.tilemap(0).pget(self.player.x, self.player.y) in self.move_parmit:
                        if self.player.check_cost(item_cost):
                            pyxel.tilemap(0).pset(self.player.x, self.player.y, (1, 6))                               
                            self.player.use_cost(item_cost)
                                    
        self.player.update()


        
    def draw(self):
        self.game_draw()

    def game_draw(self):
        # 画面のクリア
        pyxel.cls(0)

        # マップの描画
        pyxel.bltm(0, 0, 0, 0, 0, 29 * 3 * 8, 32 * 8)
      
        #NPCの描画
        for i in self.humans:
            pyxel.blt(i.x * 8, i.y * 8, 0, 0 + 8 * i.type, 0, 8, 8, 0)

        #エフェクトの描画
        for e in self.effects:            
            pyxel.rect(e.ef_x * 8, e.ef_y * 8, 2, 2, e.col)
            pyxel.rectb(e.ef_x * 8, e.ef_y * 8, 3, 3, 0)

        #カーソルの描画
        if self.player.col_flag % 2 == 0:
            pyxel.pal(9, 10)
        pyxel.blt(self.player.x * 8, self.player.y * 8, 0, 0, 8, 8, 8, 0)
        pyxel.pal()

        #アイテムセレクトボックスの描画
        if self.select_input_flag == True:
            ix = self.select_box.x
            iy = self.select_box.y
            ixm = len(self.select_box.items[0])
            iym = len(self.select_box.items)

            if ix + ixm > 27:
                pmx = -1
                ix = ix + pmx * ixm + 1
            else:
                pmx = 0
                ix = ix + pmx * ixm
            
            if iy - iym < 2:
                pmy = 1
                iy = iy + pmy * iym + 1
            else:
                pmy = 0
                iy = iy + pmy * iym
            

            pyxel.rect(ix * 8, iy * 8 - 24, 24, 24, 0)                        
            
            pyxel.blt(ix * 8, iy * 8 - 24, 2, 0, 48, 8, 8, )
            pyxel.blt(ix * 8 + 8, iy * 8 - 24, 2, 8, 48, 8, 8, )
            #きのこFLAGがONの場合
            if self.kinoko == True:
                pyxel.blt(ix * 8 + 16, iy * 8 - 24, 2, 0, 56, 8, 8, )

            pyxel.blt(ix * 8, iy * 8 - 16, 2, 0, 0, 8, 8, )
            pyxel.blt(ix * 8 + 8, iy * 8 - 16, 2, 8, 0, 8, 8, )

            pyxel.blt(ix * 8, iy * 8 - 8, 0, 0, 0, 8, 8, 0)

            pyxel.rectb(ix * 8, iy * 8 - 24, 24, 24, 7)
            pyxel.rectb(ix * 8 + self.select_box.select_x * 8, 
                        iy * 8 + self.select_box.select_y * 8 - 24, 8, 8, 8)
            
        #情報ウィンドウの描画
        pyxel.rect(0, 8 * 30, 232, 16, 0)
        pyxel.rectb(0, 8 * 30, 232, 16, 7)
        if self.player.cost < 1:
            cost_col = 8
        else:
            cost_col = 7
        pyxel.text(3, 8 * 30 + 5, "Creation Points: " + str(self.player.cost), cost_col)       
        pyxel.text(90, 8* 30 + 5, self.creation_det, 7)         



App()
