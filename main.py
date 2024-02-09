TILESIZE = 48
WIDTH = TILESIZE * 11
HEIGHT = TILESIZE * 9

walls = []
floors = []
boxes = []
targets = []

# 玩家移动方向
dirs = { "east":(1,0), "west":(-1,0), "north":(0,-1), "south":(0,1), "none":(0,0) }

finished = False
gameover = False

# 读取关卡
def loadmap(level):
    global gameover
    try:
        mapdata = loadfile("maps/map"+str(level)+".txt")
    except FileNotFoundError:
        gameover = True
    else:
        initLevel(mapdata)
        #print("after init level. level=", level, "finished=", finished, "gameover=", gameover)

def loadfile(file):
    mapfile = open(file, "r")
    map_array = []
    while True:
        line = mapfile.readline()
        if line == "":
            break
        line = line.replace("\n", "")
        line = line.replace(" ", "")
        map_array.append(line.split(","))
    mapfile.close()
    return map_array

def initLevel(mapdata):
    global walls, floors, boxes, targets, player
    walls = []
    floors = []
    boxes = []
    targets = []
    for row in range(len(mapdata)):
        for col in range(len(mapdata[row])):
            x = col * TILESIZE
            y = row * TILESIZE
            c = mapdata[row][col]
            if c >= '0' and c != '1':
                floors.append(Actor("pushbox_floor", topleft=(x, y)))
            if c == '1':
                walls.append(Actor("pushbox_wall", topleft=(x, y)))
            elif c == '2':
                box = Actor("pushbox_box", topleft=(x, y))
                box.placed = False
                boxes.append(box)
            elif c == '4':
                targets.append(Actor("pushbox_target", topleft=(x, y)))
            elif c == '6':
                targets.append(Actor("pushbox_target", topleft=(x, y)))
                box = Actor("pushbox_box_hit", topleft=(x, y))
                box.placed = True
                boxes.append(box)
            elif c == '3':
                player = Actor("pushbox_right", topleft=(x, y))

def setlevel():
    global finished, level
    finished = False
    level += 1
    #print("before load map. level=", level, "finished=", finished, "gameover=", gameover)
    loadmap(level)
    #print("after loadmap. level=", level, "finished=", finished, "gameover=", gameover)

def levelUp():
    for b in boxes:
        if not b.placed:
            return False
    return True

level = 1
loadmap(level)

# 玩家碰撞
def player_collision():
    # 玩家与墙壁的碰撞
    if player.collidelist(walls) != -1:
        player.x = player.oldx
        player.y = player.oldy
        return
    # 玩家与箱子碰撞
    index = player.collidelist(boxes)
    if index == -1:
        return
    box = boxes[index]
    if box_collision(box):
        player.x = player.oldx
        player.y = player.oldy
        return
    sounds.fall.play()

def box_collision(box):
    box.oldx = box.x
    box.oldy = box.y
    dx, dy = dirs[player.direction]
    box.x += dx * TILESIZE
    box.y += dy * TILESIZE
    if box.collidelist(walls) != -1:
        box.x = box.oldx
        box.y = box.oldy
        return True
    for b in boxes:
        if box == b:
            continue
        if box.colliderect(b):
            box.x = box.oldx
            box.y = box.oldy
            return True
    check_target(box)
    return False

def check_target(box):
    if box.collidelist(targets) != -1:
        box.image = "pushbox_box_hit"
        box.placed = True
    else:
        box.image = "pushbox_box"
        box.placed = False

def update():
    global finished
    if finished or gameover:
        return
    if levelUp():
        finished = True
        sounds.win.play()
        clock.schedule(setlevel, 5)

def draw():
    screen.fill((200, 255, 255))
    if gameover:
        screen.draw.text("Game Over", (WIDTH//2,HEIGHT//2), fontsize=60, color="red")
        return

    for f in floors:
        f.draw()
    for w in walls:
        w.draw()
    for t in targets:
        t.draw()
    for b in boxes:
        b.draw()
    player.draw()
    screen.draw.text("Level " + str(level), topleft=(20,20), fontsize=30, color="black")
    if finished:
        screen.draw.text("Level Up", (WIDTH//2,HEIGHT//2), fontsize=60, color="blue")


def on_key_down(key):
    if finished or gameover:
        #print("finished=", finished, "gameover=", gameover)
        return
    if key == keys.R:
        loadmap(level)
        return
    if key == keys.RIGHT:
        player.direction = "east"
        player.image = "pushbox_right"
    elif key == keys.LEFT:
        player.direction = "west"
        player.image = "pushbox_left"
    elif key == keys.DOWN:
        player.direction = "south"
        player.image = "pushbox_down"
    elif key == keys.UP:
        player.direction = "north"
        player.image = "pushbox_up"
    else:
        player.direction = "none"
    player_move()
    player_collision()

def player_move():
    player.oldx = player.x
    player.oldy = player.y
    dx, dy = dirs[player.direction]
    player.x += dx * TILESIZE
    player.y += dy * TILESIZE


