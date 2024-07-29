# 教學資源 Make 2048 In Python | Full Python Game Tutorial 
#  link: https://youtu.be/6ZyylFcjfIg?si=VqkVnZHlKgIA4u5I

import pygame
import random
import math

pygame.init()

FPS = 60

width, height = 800, 800  # 面板高度、寬度
ROWS = 4  # 行數
COLS = 4  # 列數

RECT_HEIGHT = height // ROWS
RECT_WIDTH = width // COLS

OUTLINE_COLOR = (187, 173, 160)  # 框線顏色
OUTLINE_THICKNESS = 10  # 厚度
BACKGROUND_COLOR = (205, 192, 180)  # 背景顏色
FONT_COLOR = (119, 110, 101)  # 字體顏色

FONT = pygame.font.SysFont("comicsans", 60, bold=True)
GAME_OVER_FONT = pygame.font.SysFont("comicsans", 100, bold=True)
MOVE_VEL = 20  # 字體設定

WINDOW = pygame.display.set_mode((width, height))  # 高度寬度設定
pygame.display.set_caption("2048")  # 視窗名字設定

# tile函式: 可將指定序列重複進行指定的次數(如:將一個格子複製x次 
class Tile: 
    COLORS = [
        (237, 229, 218), (238, 225, 201),
        (243, 178, 122), (246, 150, 101),
        (247, 124, 95), (247, 95, 59),
        (237, 208, 115), (237, 204, 99),
        (236, 202, 80),
    ]

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT
    
    def get_color(self):  # 取得顏色
        color_index = int(math.log2(self.value)) - 1  # color_index索引用來查找顏色 #以2為這個對數的底 int用來取對數值的整數
        color = self.COLORS[color_index]
        return color

    def draw(self, window):
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        text = FONT.render(str(self.value), 1, FONT_COLOR)  # render 渲染文字用 
        window.blit(  # blit 用來將一個surface放到遊戲視窗上
            text,
            (
                self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
                self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    def set_pos(self, ceil=False):  # 設定位置 #ceil 向上取整數 floor 向下取
        if ceil:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def move(self, delta):  # 想要動的格數
        self.x += delta[0]  # 水平方向移動量
        self.y += delta[1]  # 垂直方向移動量

def draw_grid(window):  # 繪製矩形(外框)
    for row in range(1, ROWS):  # 行
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (width, y), OUTLINE_THICKNESS)

    for col in range(1, COLS):  # 列
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, height), OUTLINE_THICKNESS)
        
    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, width, height), OUTLINE_THICKNESS)

def draw(window, tiles):
    window.fill(BACKGROUND_COLOR)

    for tile in tiles.values():
        tile.draw(window)

    draw_grid(window)
    pygame.display.update()

def random_pos(tiles):  # 隨機位置生成
    row = None
    col = None
    while True:
        row = random.randrange(0, ROWS)  # randrange隨機範圍
        col = random.randrange(0, COLS)  # randrange隨機範圍
        
        if f"{row}{col}" not in tiles:
            break

    return row, col 

def move_tiles(window, tiles, clock, direction):  # direction方向 #ceil用於取得方塊時是往上產生或往下產生
    updated = True
    blocks = set()
    
    if direction == "left":
        sort_func = lambda x: x.col  # lambda函式:「func = lambda 參數1, 參數2, ... : 運算式」類似於def簡潔版
        reverse = False
        delta = (-MOVE_VEL, 0)  # 前值為左右 後值為上下
        bound_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL
        move_check = lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL
        ceil = True 
    
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (MOVE_VEL, 0)  # 前值為左右 後值為上下
        bound_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
        move_check = lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
        ceil = False

    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -MOVE_VEL)
        bound_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
        move_check = lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
        ceil = True 
        
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, MOVE_VEL)
        bound_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
        move_check = lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y
        ceil = False
    
    # 刷新畫面
    while updated:
        clock.tick(FPS)
        updated = False  # 避免無線迴圈
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)  # tiles.values() 取得 tiles 字典中的所有值 #sorted_tiles 排序後的圖塊列表

        # 處理圖塊 根據條件合併或移動
        for i, tile in enumerate(sorted_tiles):
            if bound_check(tile):
                continue

            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks:
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    next_tile.value *= 2
                    sorted_tiles.pop(i)  # pop用於刪除列表中元素
                    blocks.add(next_tile)  # 避免合併兩次
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue  # 跳過 繼續處理下個tile
            
            tile.set_pos(ceil)
            updated = True

        update_tiles(window, tiles, sorted_tiles)

    return end_move(tiles)

def end_move(tiles):
    if len(tiles) == 16:
        return "lost"
    
    row, col = random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"

def update_tiles(window, tiles, sorted_tiles):  # 更新圖塊
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile

    draw(window, tiles)

# 產生tiles圖塊
def gen_tiles():
    tiles = {}  # {}為dict
    for _ in range(2):
        row, col = random_pos(tiles)  # 隨機位置生成函數(行或列)
        tiles[f"{row}{col}"] = Tile(2, row, col)  # f-字串=format

    return tiles

#遊戲結束
def draw_game_over(window):
    text = GAME_OVER_FONT.render("Game Over", 1, FONT_COLOR)
    window.blit(
        text,
        (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2),
    )
    pygame.display.update()

# 視窗
def main(window):
    clock = pygame.time.Clock()
    run = True

    tiles = gen_tiles()  # tiles:用於定位圖塊產生的位置及數字
    game_status = "continue"

    while run:
        clock.tick(FPS) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN and game_status == "continue":
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    game_status = move_tiles(window, tiles, clock, "left")
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    game_status = move_tiles(window, tiles, clock, "right")
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    game_status = move_tiles(window, tiles, clock, "up")
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    game_status = move_tiles(window, tiles, clock, "down")

            draw(window, tiles)

            if game_status == "lost":
                draw_game_over(window)

    pygame.quit()

if __name__ == "__main__":  # __name__模組名稱
    main(WINDOW)
