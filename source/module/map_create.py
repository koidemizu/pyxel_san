import random

def MAP_CREATE():
    
    MAP_WIDTH = 29
    MAP_HEIGHT = 30
    # マップの初期化
    map_data = [[(0, 5) for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

    # 中を破壊可能な岩で埋める
    for y in range(1, MAP_HEIGHT - 1):
        for x in range(1, MAP_WIDTH - 1):
            map_data[y][x] = (0, 0)

    # オブジェクトをランダムな個数配置する
    num_of_objects = random.randint(4, 8)
    for i in range(num_of_objects):
        obj_size_x = random.randint(2, 3)
        obj_size_y = random.randint(2, 3)
        obj_x = random.randint(1, MAP_WIDTH - obj_size_x - 1)
        obj_y = random.randint(1, MAP_HEIGHT - obj_size_y - 1)
        for y in range(obj_y, obj_y + obj_size_y):
            for x in range(obj_x, obj_x + obj_size_x):
                map_data[y][x] = (1, 0)


    # ランダムなサイズの空き地を作成する
    #ここで空き地の環境も決定する。
    room_num = random.randint(8, 12)    

    for r in range(room_num):
        bio_num = random.randint(1, 9)
        
        if bio_num == 1 or bio_num == 2:    
            room_assets = ((0, 7), (1, 7), (2, 7))
        elif bio_num == 2 or bio_num == 3:    
            room_assets = ((0, 8), (1, 8), (2, 8))            
        elif bio_num == 4:
            bn2 = random.randint(0, 2)
            if bn2 == 0:
                room_assets = ((1, 2),)                       
            else:
                room_assets = ((0, 6),)                       
        elif bio_num == 5 or bio_num == 6:
            room_assets = ((0, 2),)                 
        elif bio_num == 7:
            room_assets = ((1, 2),)                 
        else:            
            room_assets = ((0, 6),)

        room_width = random.randint(2, 4)
        room_height = random.randint(2, 4)
        room_x = random.randint(1, MAP_WIDTH - room_width - 2)
        room_y = random.randint(1, MAP_HEIGHT - room_height - 2)
        for y in range(room_y, room_y + room_height):
            for x in range(room_x, room_x + room_width):
                map_data[y][x] = random.choice(room_assets)   
                         
    #spe_obj = spe_obj_old = [0, 0]
    #for sn in range(2):
    #    while spe_obj_old == spe_obj:
    #        spe_obj = [random.randint(5, 24), random.randint(5, 24)]

    #    spe_obj_old = spe_obj        
    #    map_data[spe_obj[0]][spe_obj[1]] = (3, 7 + sn)        
    #    if spe_obj[0] + 1 <= MAP_WIDTH:
    #        map_data[spe_obj[0]+1][spe_obj[1]] = (0, 0)

    #    if spe_obj[0] - 1 >= 0:
    #        map_data[spe_obj[0]-1][spe_obj[1]] = (0, 0)

    #    if spe_obj[1] + 1 <= MAP_HEIGHT:
    #        map_data[spe_obj[0]][spe_obj[1]+1] = (0, 0)

    #    if spe_obj[1] - 1 >= 0:
    #        map_data[spe_obj[0]][spe_obj[1]-1] = (0, 0)    

        map_data[1][1] = (0, 5)
        map_data[0][0] = (0, 10)

    return map_data