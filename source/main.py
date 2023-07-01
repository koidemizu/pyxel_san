import pyxel
import json
from module import player_class, human_class, selectbox_class, water_class, map_create, lava_class, watereye_class, \
                   watermonster_class, lavaeye_class, lavarmonster_class

class App:
    def __init__(self):
        # 画面の初期化
        pyxel.init(232, 256, fps = 30,)
       
        self.set_assets()

        # リソースの読み込み
        pyxel.load("assets/assets.pyxres")        
    
        self.set_common_status()
        self.set_status()        
        self.map_reset()

        # ゲームループの開始
        pyxel.run(self.update, self.draw)

    def set_assets(self):
        #音楽データの読み込み
        with open(f"assets/music.json", "rt",encoding="utf-8") as fin:
            self.music = json.loads(fin.read())
        #チャンネルにセット        
        for ch, sound in enumerate(self.music):                
            pyxel.sound(ch).set(*sound)

    def music_play(self):
        #再生
        pyxel.play(0, 0, loop=True)                 
        pyxel.play(1, 1, loop=True)        
        pyxel.play(2, 2, loop=True)        

    def music_stop(self):
        #停止
        pyxel.stop(0)                 
        pyxel.stop(1)                 
        pyxel.stop(2)                              

    def set_common_status(self):
        self.game_status = 0
        self.msgbox_flag = False
        self.msgbox_select = 1     
        self.game_mode = 1           

    def set_status(self):
        #各種変数・インスタンスの準備
        self.tb1g = pyxel.rndi(5, 15)
        self.tb2g = pyxel.rndi(5, 15)
        self.player = player_class.Player(1, 1)
        self.gems = [9, 9, 9, 9, 9]
        self.gem_tiles = ((0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9) )
        self.humans = []
        self.humans_u = []
        self.humans_count = 0
        self.humans_num = 0
        self.stop_flag = False
        self.select_input_flag = False       
        self.indestructible = ((0, 5), (0, 3))   #破壊不可なブロック、ビルドメニューからの操作もできない
        self.rock = ((0, 0), (1, 0), (2, 0)) 
        self.move_parmit = ((0, 6),
                            (0, 7), (1, 7), (2, 7), (3, 7),
                            (0, 8), (1, 8), (2, 8), (3, 8),
                            (0, 9), (1, 9), (2, 9))
        self.move_parmit_toclass = ((0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6),
                                    (0, 7), (1, 7), (2, 7), (3, 7),
                                    (0, 8), (1, 8), (2, 8), (3, 8),
                                    (0, 9), (1, 9), (2, 9), (3, 9), (4, 9)) 
        self.creation_det = ""
        self.kinoko = True
        self.kinoko2 = True
        self.kinoko_list = ((0, 7), (1, 7), (2, 7),
                            (0, 8), (1, 8), (2, 8), (4, 8), (5, 8), (6, 8))
        self.kusa_list = ((4, 8), (5, 8), (6, 8))        
        self.effects = []
        self.g_pos = []
        self.waters = []
        self.water_eyes = []
        self.water_monsters = []
        self.lavas = []
        self.lava_eyes = []
        self.lava_monsters = []
        self.show_range = 64       


    def map_reset(self):
        #マップデータの作成
        self.map_data = map_create.MAP_CREATE()
        for m1 in range(len(self.map_data)):
            for m2 in range(len(self.map_data[m1])):
                if self.map_data[m1][m2] == (0, 2):
                    new_water = water_class.Water(m2, m1, self.move_parmit_toclass)
                    self.waters.append(new_water)
                if self.map_data[m1][m2] == (1, 2):
                    new_lava = lava_class.Lava(m2, m1, self.move_parmit_toclass)
                    self.lavas.append(new_lava)

                pyxel.tilemap(0).pset(m2, m1, self.map_data[m1][m2])
   
        #埋蔵物があるマスを設定
        g_cnt = 0
        while g_cnt < 5:
            g_pos1 = pyxel.rndi(5, 22)
            g_pos2 = pyxel.rndi(5, 22)
            if pyxel.tilemap(0).pget(g_pos1, g_pos2) == (0, 0):                   
                new_g_pos = [g_pos1, g_pos2]
                self.g_pos.append(new_g_pos)
                g_cnt += 1                

    def update(self):        
        #タイトル画面
        if self.game_status == 0:
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):    
                if self.game_mode == 2:
                    self.game_mode = 1                       
                
            elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):          
                if self.game_mode == 1:
                    self.game_mode = 2

            #ゲームスタート
            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):                 
                self.game_status = 1
                self.set_assets()
                self.set_status()
                self.map_reset()                
                self.music_play()
                if self.game_mode == 1:
                    self.player.cost = 1000
        #ゲーム画面
        elif self.game_status == 1:
            if self.msgbox_flag == True:
                self.msgbox_update()
            else:
                self.game_update()

    def msgbox_update(self):
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):    
            if self.msgbox_select == 2:
                self.msgbox_select = 1                       
                
        elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):          
            if self.msgbox_select == 1:
                self.msgbox_select = 2

        if pyxel.btnp(pyxel.KEY_N) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X): 
            self.msgbox_flag = False
            #タイトルへ戻る
            if self.msgbox_select == 1:
                self.music_stop()
                self.game_status = 0
                self.game_mode = 1
            self.msgbox_select = 1            

    def game_update(self):
        if pyxel.btnp(pyxel.KEY_C):  
            g = 0
            for gt in self.g_pos:
                print(pyxel.tilemap(0).pget(gt[0], gt[1]))
                if pyxel.tilemap(0).pget(gt[0], gt[1]) in self.gem_tiles:
                    self.gems[g] = pyxel.tilemap(0).pget(gt[0], gt[1])[0]
                g += 1
            print(self.gems)

        if pyxel.btnp(pyxel.KEY_A):  
            self.set_assets()
            self.set_status()
            self.map_reset()

        if pyxel.btnp(pyxel.KEY_B):  
            print(self.water_eyes)

 
        #描画範囲調整用
        gc = 0
        for gm in self.gems:
            if gm < 9:
                gc += 10
        lc = len(self.lavas)

        self.show_range = 64 + self.humans_num + gc + lc


        if self.select_input_flag == False:
            #フリーモードのみコストの自動回復あり
            if pyxel.frame_count % 150 == 0:
                self.player.add_cost(1)

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
                if pyxel.tilemap(0).pget(self.player.x, self.player.y) == (0, 10):
                    self.msgbox_flag = True                    
                else:
                    pyxel.play(3, 12)
                    items = [[("Ground", 10), ("Flag1", 1), ("Flag2", 1), ("Flag3", 1)] ,
                            [("Rock1", 10), ("Rock2", 10), ("Water", 5), ("Lava", 5)],
                            [("Human", 25), ("Stop", 1), ("", 0), ("", 0)]]
                    if self.kinoko == True:
                        items[2][2] = ("Mushroom1", 15)
                    if self.kinoko2 == True:
                        items[2][3] = ("Mushroom2", 15)

                    self.select_box = selectbox_class.SelectBox(self.player.x, self.player.y, items)
                    self.select_input_flag = True
                    self.creation_det = self.select_box.creation_det

            #エフェクトのアップデート
            self.effect_update()
            
            #人間のアップデート
            self.stop_flag = False
            for st1 in range(32):
                for st2 in range(32):
                    if pyxel.tilemap(0).pget(st1, st2) == (2, 6):
                        self.stop_flag = True
            
            #負荷を下げるためにhumansを5つごとに分割して処理する。
            self.humans_count += 1
            self.humans_num = len(self.humans)
            if self.humans_count * 5 > len(self.humans):
                self.humans_count = 0
            if self.stop_flag == False:
                self.human_update()
            
            #水のアップデート
            self.water_update()

            #溶岩のアップデート
            self.lava_update()            

            #宝石確認
            self.gem_chk()
                
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
                pyxel.play(3, 13)
                self.creation_det = ""
                del self.select_box                
           
            if pyxel.btnp(pyxel.KEY_N) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A): 
                item = self.select_box.items[self.select_box.select_y][self.select_box.select_x][0]
                item_cost = self.select_box.items[self.select_box.select_y][self.select_box.select_x][1]
                #Humanの投下
                if item == "Human":                    
                    if pyxel.tilemap(0).pget(self.player.x, self.player.y) in self.move_parmit:
                        if self.player.check_cost(item_cost):
                            new_human = human_class.Human(self.player.x, self.player.y, pyxel.rndi(1, 28), pyxel.rndi(1, 28), self.move_parmit_toclass)
                            self.humans.append(new_human)
                            self.player.use_cost(item_cost)
                            pyxel.play(3, 11)
                #道の設置
                elif item == "Ground":
                    if pyxel.tilemap(0).pget(self.player.x, self.player.y) in self.indestructible:
                        pass
                    else:
                        if self.player.check_cost(item_cost):
                            self.water_chk(self.player.x, self.player.y)
                            pyxel.tilemap(0).pset(self.player.x, self.player.y, (0, 6))
                            self.player.use_cost(item_cost)
                            for gp in self.g_pos:
                                if gp == [self.player.x, self.player.y]:         
                                    grl = []
                                    for gr1 in range(28):
                                        for gr2 in range(28):
                                            if pyxel.tilemap(0).pget(gr1, gr2) == (0, 0):
                                                grl.append((gr1, gr2))
                                    gpc = pyxel.rndi(0, len(grl))
                                    gp[0] = grl[gpc][0]
                                    gp[0] = grl[gpc][1]                                    
                
                #きのこ土地(赤)の設置
                elif item == "Mushroom1":
                    if pyxel.tilemap(0).pget(self.player.x, self.player.y) in self.move_parmit:
                        if self.player.check_cost(item_cost):
                            self.water_chk(self.player.x, self.player.y)
                            pyxel.tilemap(0).pset(self.player.x, self.player.y, (pyxel.rndi(0, 2), 7))
                            self.player.use_cost(item_cost)                 
                #きのこ土地(緑)の設置
                elif item == "Mushroom2":
                    if pyxel.tilemap(0).pget(self.player.x, self.player.y) in self.move_parmit:
                        if self.player.check_cost(item_cost):
                            self.water_chk(self.player.x, self.player.y)
                            pyxel.tilemap(0).pset(self.player.x, self.player.y, (pyxel.rndi(0, 2), 8))
                            self.player.use_cost(item_cost)                                                        
                #岩の設置
                elif item == "Rock1":
                    if pyxel.tilemap(0).pget(self.player.x, self.player.y) in self.indestructible:
                        pass
                    else:
                        if self.player.check_cost(item_cost):
                            self.water_chk(self.player.x, self.player.y)
                            pyxel.tilemap(0).pset(self.player.x, self.player.y, (0, 0))
                            self.player.use_cost(item_cost)
                #壊せない岩の設置
                elif item == "Rock2":                    
                    if pyxel.tilemap(0).pget(self.player.x, self.player.y) in self.indestructible:
                        pass
                    else:
                        if self.player.check_cost(item_cost):
                             self.water_chk(self.player.x, self.player.y)
                             pyxel.tilemap(0).pset(self.player.x, self.player.y, (1, 0))        
                             self.player.use_cost(item_cost)
                             for gp in self.g_pos:
                                if gp == [self.player.x, self.player.y]:         
                                    grl = []
                                    for gr1 in range(28):
                                        for gr2 in range(28):
                                            if pyxel.tilemap(0).pget(gr1, gr2) == (0, 0):
                                                grl.append((gr1, gr2))
                                    gpc = pyxel.rndi(0, len(grl))
                                    gp[0] = grl[gpc][0]
                                    gp[0] = grl[gpc][1]                       

                #旗の設置
                elif item == "Flag1":                    
                    if pyxel.tilemap(0).pget(self.player.x, self.player.y) in self.move_parmit:
                        if self.player.check_cost(item_cost):
                            self.water_chk(self.player.x, self.player.y)
                            pyxel.tilemap(0).pset(self.player.x, self.player.y, (3, 6))                               
                            self.player.use_cost(item_cost)
                elif item == "Flag2":                    
                    if pyxel.tilemap(0).pget(self.player.x, self.player.y) in self.move_parmit:
                        if self.player.check_cost(item_cost):
                            self.water_chk(self.player.x, self.player.y)
                            pyxel.tilemap(0).pset(self.player.x, self.player.y, (4, 6))                               
                            self.player.use_cost(item_cost)
                elif item == "Flag3":                    
                    if pyxel.tilemap(0).pget(self.player.x, self.player.y) in self.move_parmit:
                        if self.player.check_cost(item_cost):
                            self.water_chk(self.player.x, self.player.y)
                            pyxel.tilemap(0).pset(self.player.x, self.player.y, (5, 6))                               
                            self.player.use_cost(item_cost)

                #ストップマークの設置
                elif item == "Stop":                    
                    if pyxel.tilemap(0).pget(self.player.x, self.player.y) in self.move_parmit:
                        if self.player.check_cost(item_cost):
                            self.water_chk(self.player.x, self.player.y)
                            pyxel.tilemap(0).pset(self.player.x, self.player.y, (2, 6))                               
                            self.player.use_cost(item_cost)

                #水の設置
                elif item == "Water":                    
                    if pyxel.tilemap(0).pget(self.player.x, self.player.y) in self.move_parmit:
                        if self.player.check_cost(item_cost):
                            pyxel.tilemap(0).pset(self.player.x, self.player.y, (0, 2))       
                            self.player.use_cost(item_cost)                          
                            new_water = water_class.Water(self.player.x, self.player.y, self.move_parmit_toclass)  
                            self.waters.append(new_water)

                #溶岩の設置
                elif item == "Lava":                    
                    if pyxel.tilemap(0).pget(self.player.x, self.player.y) in self.move_parmit:
                        if self.player.check_cost(item_cost):
                            pyxel.tilemap(0).pset(self.player.x, self.player.y, (1, 2))       
                            self.player.use_cost(item_cost)                          
                            new_lava = lava_class.Lava(self.player.x, self.player.y, self.move_parmit_toclass)  
                            self.lavas.append(new_lava)                            
                                    
        self.player.update()


    def gem_chk(self):
        g = 0
        g2 = 0
        #宝石のあるマスを最新化
        for gt in self.g_pos:            
            if pyxel.tilemap(0).pget(gt[0], gt[1]) in self.gem_tiles:
                self.gems[g] = pyxel.tilemap(0).pget(gt[0], gt[1])[0]
                g2 += 1
            g += 1     
        if g2 > 4:
            print("OOO")
          
        if pyxel.frame_count % 30 == 0:
            w_c = 0
            #白のhumanをカウント
            for wh in self.humans:
                if wh.type == 3:
                    if w_c < 10:
                        w_c += 1
            #ランダムで宝石のあるマスにエフェクトを出す。白人間が多い方が高確率。
            if pyxel.rndi(0, 11 - w_c) == 0:
                for gpos in self.g_pos:
                    for ge in range(w_c):
                        if pyxel.tilemap(0).pget(gpos[0], gpos[1]) == (0, 0):
                            self.effects.append(human_class.Effect(gpos[0], gpos[1], 7, 2))             

    def human_update(self):
        #人間のアップデート
        hu = self.humans_count * 5
        #負荷を下げるためにhumansを5つごとに分割して処理する。
        for i in self.humans[hu: hu+5]:
            #岩と重なっている場合はHumanを削除
            if pyxel.tilemap(0).pget(i.x, i.y) in self.rock:
                self.humans.remove(i)
            #水と重なっている場合はHumanを削除
            if pyxel.tilemap(0).pget(i.x, i.y) == (0, 2):
                #緑人間は泳げる
                if i.type == 2:
                    pass
                else:
                    self.humans.remove(i)
            #溶岩と重なっている場合はHumanを削除
            if pyxel.tilemap(0).pget(i.x, i.y) == (1, 2):
                self.humans.remove(i)


            i.update(self.player, self.effects, self.g_pos, self.humans_num / 5)       
            #きのこを食べるとHumanが増える
            if pyxel.tilemap(0).pget(i.x, i.y) in self.kinoko_list:
                new_human = human_class.Human(i.x, i.y, pyxel.rndi(1, 28), pyxel.rndi(1, 28), self.move_parmit_toclass)
                #半分の確率できのこ人間になる
                if pyxel.rndi(0, 1) == 0:
                    tgt_ms = pyxel.tilemap(0).pget(i.x, i.y)[1]                    
                    if tgt_ms == 7:
                        #赤人間に
                        new_human.type = 1
                    elif tgt_ms == 8:
                        #緑人間に
                        new_human.type = 2                
                        new_human.move_parmit = ((0, 2), (0, 6), (1, 6), (2, 6),
                                   (0, 7), (1, 7), (2, 7), (3, 7),
                                   (0, 8), (1, 8), (2, 8), (3, 8))              
                        #緑人間は動きが遅い
                        new_human.move_parmit_count_max = pyxel.rndi(50, 90)                             

                    #元々のhumanが緑か赤だった場合は、さらに半分の確率で白にする。
                    if i.type == 1 or i.type == 2:   
                        if pyxel.rndi(0, 1) == 0:
                            new_human.type = 3
                            new_human.move_parmit = self.move_parmit_toclass
                            new_human.move_parmit_count_max = pyxel.rndi(20, 50)
                self.humans.append(new_human)
                pyxel.tilemap(0).pset(i.x, i.y, (0, 6))

            if self.kinoko == True:
                pass
            else:
                if i.kinoko_chk():
                    self.kinoko = True
                    pyxel.tilemap(0).pset(i.x, i.y, (0, 6))

            if self.kinoko2 == True:
                pass
            else:
                if i.kinoko_chk2():
                    self.kinoko2 = True
                    pyxel.tilemap(0).pset(i.x, i.y, (0, 6))
   
    def water_update(self):
        #水のアップデート
        for w in self.waters:
            if pyxel.tilemap(0).pget(w.x, w.y) in ((0, 2), (0, 3), (4, 7), (5, 7), (6, 7), (4, 8), (5, 8), (6, 8)):
                pass
            else:
                self.waters.remove(w)            
            nw = w.update()
            if nw:
                if pyxel.tilemap(0).pget(nw[0], nw[1],) == (0, 3):
                    new_watereye = watereye_class.Watereye(nw[0], nw[1])
                    self.water_eyes.append(new_watereye)
                
                new_water = water_class.Water(nw[0], nw[1], self.move_parmit_toclass)
                self.waters.append(new_water)
        #水の目のアップデート
        for we in self.water_eyes:
            if we.update():
                pyxel.tilemap(0).pset(we.x, we.y, (0, 2))
                #水の目は消えるときに水モンスターを作成する
                new_watermonster = watermonster_class.Watermonster(we.x, we.y)
                self.water_monsters.append(new_watermonster)
                self.water_eyes.remove(we)            

        #水モンスターのアップデート
        for wm in self.water_monsters:
            nwm = wm.update()
            if nwm:                
                new_water = water_class.Water(nwm[0], nwm[1], self.move_parmit_toclass)
                self.waters.append(new_water)
                for e in range(10):
                    self.effects.append(human_class.Effect(nwm[0], nwm[1], 6, 7))  
                self.water_monsters.remove(wm)


    def lava_update(self):
        #溶岩のアップデート
        for l in self.lavas:
            if pyxel.tilemap(0).pget(l.x, l.y) in ((1, 2), (1, 3)):
                pass
            else:
                self.lavas.remove(l)
            nl = l.update(self.g_pos)
            if nl:
                if pyxel.tilemap(0).pget(nl[0], nl[1],) == (1, 3):                                    
                    new_lavaeye = lavaeye_class.Lavaeye(nl[0], nl[1])
                    self.lava_eyes.append(new_lavaeye)
                new_lava = lava_class.Lava(nl[0], nl[1], self.move_parmit_toclass)
                self.lavas.append(new_lava)           

        #溶岩の目のアップデート
        for le in self.lava_eyes:
            if le.update():
                pyxel.tilemap(0).pset(le.x, le.y, (1, 2))
                #水の目は消えるときに水モンスターを作成する
                new_lavamonster = lavarmonster_class.Lavamonster(le.x, le.y)
                self.lava_monsters.append(new_lavamonster)
                self.lava_eyes.remove(le)                                 
                
        #溶岩モンスターのアップデート
        for lm in self.lava_monsters:
            nlm = lm.update()
            if nlm:                
                new_lava = lava_class.Lava(nlm[0], nlm[1], self.move_parmit_toclass)
                self.lavas.append(new_lava)
                for e in range(10):
                    self.effects.append(human_class.Effect(nlm[0], nlm[1], 8, 10))  
                self.lava_monsters.remove(lm)

    def effect_update(self):
        #エフェクトアップデート
        for e in self.effects:
            e.update()
            if e.ef_t < 0:
                self.effects.remove(e)


    def water_chk(self, x, y):
        if pyxel.tilemap(0).pget(x, y) == (0, 2):
            for cw in self.waters:
                if cw.x == x and cw.y == y:
                    self.waters.remove(cw)

    def draw(self):
        #タイトル画面
        if self.game_status == 0:
            # 画面のクリア
            pyxel.cls(0)
 
            for tb3 in range(18):
                pyxel.blt(210, 240 - 15 * tb3, 1, 0, 8, 24, 24, 15)
                pyxel.blt(0, 240 - 15 * tb3, 1, 0, 8, 24, 24, 15)
            

            for tb1 in range(20):
                g = 0
                if tb1 == self.tb1g:
                    g = 32                    
                    pyxel.blt(-15 + tb1 * 15, 0, 1, 0, 8 + g, 24, 24, 15)
                    g2 = pyxel.frame_count % 10
                    pyxel.blt(-15 + tb1 * 15, 0, 1, 32 + g2 * 16, 0, 16, 16, 15)
                else:
                    pyxel.blt(-15 + tb1 * 15, 0, 1, 0, 8 + g, 24, 24, 15)
            for tb2 in range(20):
                g = 0
                if tb2 == self.tb2g:
                    g = 64
                    pyxel.blt(-15 + tb2 * 15, 232, 1, 0, 8 + g, 24, 24, 15)     
                    g2 = pyxel.frame_count % 10
                    pyxel.blt(-15 + tb2 * 15, 232, 1, 32 + g2 * 16, 0, 16, 16, 15)                               
                else:
                    pyxel.blt(-15 + tb2 * 15, 232, 1, 0, 8 + g, 24, 24, 15)                
            
            
            
            pyxel.text(30, 30, "pyxel_sandbox", 7)
            pyxel.text(30, 40, "game_mode:", 7)
            pyxel.text(40, 50, "free mode", 7)
            pyxel.text(40, 60, "adventure mode", 7)
            pyxel.blt(30, 40 + 10 * self.game_mode, 0, 0, 64, 8, 8, 0)

            pyxel.text(30, 80, "Press KEY_SPACE or GAMEPAD_BUTTON_X", 7)            

      
            txt1 = "*** Game Rules ***"
            if self.game_mode == 2:
                txt2 = "Discover the five gems."
                txt3 = "Note that few resources are available."        
            elif self.game_mode == 1:
                txt2 = "Play freely with a large amount of resources."
                txt3 = ""
            pyxel.text(30, 100, txt1, 7)
            pyxel.text(30, 110, txt2, 7)
            pyxel.text(30, 120, txt3, 7)


        #ゲーム画面
        elif self.game_status == 1:
            self.game_draw()
            if self.msgbox_flag == True:
                self.msgbox_draw()

    def msgbox_draw(self):                                
        #ウィンドウのベース
        pyxel.rect(2, 2, 60, 30, 0)               
        pyxel.rectb(2, 2, 60, 30, 8)               
        pyxel.text(5, 4, "return title?", 7)
        pyxel.text(15, 14, "Yes", 7)
        pyxel.text(15, 24, "No", 7)
        pyxel.blt(4, 3 + 10 * self.msgbox_select, 0, 0, 64, 8, 8, 0)

    def game_draw(self):
        # 画面のクリア
        pyxel.cls(0)

        #画面描画の制限
        if self.game_mode == 2:
            crw = self.show_range / 2
            pyxel.clip(self.player.x * 8 - crw, self.player.y * 8 - crw, self.show_range, self.show_range)

        # マップの描画
        pyxel.bltm(0, 0, 0, 0, 0, 29 * 3 * 8, 32 * 8)
      
        #humanの描画
        for i in self.humans:
            pyxel.blt(i.x * 8, i.y * 8, 0, 0 + 8 * i.type, 0, 8, 8, 0)

        #水モンスターの描画
        for wm in self.water_monsters:
            pyxel.blt(wm.x * 8, wm.y * 8, 0, 8, 16, 8, 8, 0)

        #溶岩モンスターの描画
        for lm in self.lava_monsters:
            pyxel.blt(lm.x * 8, lm.y * 8, 0, 0, 16, 8, 8, 0)

        #エフェクトの描画
        for e in self.effects:            
            pyxel.rect(e.ef_x * 8, e.ef_y * 8, 2, 2, e.col)
            pyxel.rectb(e.ef_x * 8, e.ef_y * 8, 3, 3, e.ef_v)

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
            
            #ウィンドウのベース
            pyxel.rect(ix * 8, iy * 8 - 24, 32, 24, 0)                        
            
            #1段目
            pyxel.blt(ix * 8, iy * 8 - 24, 2, 0, 48, 8, 8, )
            pyxel.blt(ix * 8 + 8, iy * 8 - 24, 2, 24, 48, 8, 8, )       
            pyxel.blt(ix * 8 + 16, iy * 8 - 24, 2, 32, 48, 8, 8, )       
            pyxel.blt(ix * 8 + 24, iy * 8 - 24, 2, 40, 48, 8, 8, )       

            #2段目
            pyxel.blt(ix * 8, iy * 8 - 16, 2, 0, 0, 8, 8, )
            pyxel.blt(ix * 8 + 8, iy * 8 - 16, 2, 8, 0, 8, 8, )
            pyxel.blt(ix * 8 + 16, iy * 8 - 16, 2, 0, 16, 8, 8, )
            pyxel.blt(ix * 8 + 24, iy * 8 - 16, 2, 8, 16, 8, 8, )

            #3段目
            pyxel.blt(ix * 8, iy * 8 - 8, 0, 0, 0, 8, 8, 0)
            pyxel.blt(ix * 8 + 8, iy * 8 - 8, 2, 16, 48, 8, 8, 0)
            #きのこFLAGがONの場合
            if self.kinoko == True:
                pyxel.blt(ix * 8 + 16, iy * 8 - 8, 2, 0, 56, 8, 8, )
            if self.kinoko2 == True:
                pyxel.blt(ix * 8 + 24, iy * 8 - 8, 2, 0, 64, 8, 8, )                     

            #囲いの枠
            pyxel.rectb(ix * 8, iy * 8 - 24, 32, 24, 7)
            pyxel.rectb(ix * 8 + self.select_box.select_x * 8, 
                        iy * 8 + self.select_box.select_y * 8 - 24, 8, 8, 8)
        
        #画面描画制限###############
        if self.game_mode == 2:
            pyxel.clip()
            crw = self.show_range / 2
            pyxel.circb(self.player.x * 8, self.player.y * 8, crw, 8) 
            for c in range(20):
                pyxel.circb(self.player.x * 8, self.player.y * 8, crw + c, 0) 
            pyxel.circ(self.player.x * 8 - crw, self.player.y * 8 - crw, crw/3, 0) 
            pyxel.circ(self.player.x * 8 - crw, self.player.y * 8 + crw, crw/3, 0) 
            pyxel.circ(self.player.x * 8 + crw, self.player.y * 8 - crw, crw/3, 0) 
            pyxel.circ(self.player.x * 8 + crw, self.player.y * 8 + crw, crw/3, 0) 
        ###################################                

        #情報ウィンドウの描画        
        pyxel.rect(0, 8 * 30, 232, 16, 0)
        pyxel.rectb(0, 8 * 30, 232, 16, 7)
        if self.player.cost < 1:
            cost_col = 8
        else:
            cost_col = 7
        pyxel.text(3, 8 * 30 + 5, "Creation Points: " + str(self.player.cost), cost_col)       

        if self.select_input_flag == False:
            for g in range(5):
                pyxel.text(90, 8 * 30 + 5, "Gems:", 7)
                pyxel.blt(110 + g * 10, 8 * 30 + 3, 2, 40, 72, 8, 8)
                if self.gems[g] < 9:
                    pyxel.blt(110 + g * 10, 8 * 30 + 3, 2, 0 + 8 * self.gems[g], 72, 8, 8, 1)
        else:            
            pyxel.text(90, 8* 30 + 5, self.creation_det, 7)         



App()
