import pygame
import os
import random

pygame.init()
pygame.display.set_caption('Стихийные лабиринты')
weight = 700
height = 700
name_lavel = ''
screen = pygame.display.set_mode((weight, height))
fl_lavels_or_maze = True
icon = pygame.image.load('data/icon.jpg')
pygame.display.set_icon(icon)


class Levels(pygame.sprite.Sprite):  #класс уровней
    def __init__(self, group, im, pos, level):
        super().__init__(group)
        self.image = im
        self.rect = self.image.get_rect().move(pos)
        self.level = level

    def update(self, *args):
        global name_lavel, fl_lavels_or_maze
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            name_lavel = self.level
            fl_lavels_or_maze = False


image_water = pygame.image.load('data/water.jpg')
image_fire = pygame.image.load('data/fire.jpg')
image_air = pygame.image.load('data/air.jpg')
image_terra = pygame.image.load('data/terra.jpg')
image_door = pygame.image.load('data/close.jpg')


def load_image(name, color_key=None):  #класс загрузки изображения
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image

#словари для каждого уровня с изображениями для него
tile_images_fire = {
    'wall': load_image('fire_level.png'),
    'empty': load_image('fire_level2.png')}
tile_images_water = {
    'wall': load_image('water_level.png'),
    'empty': load_image('water_level2.png')}
tile_images_air = {
    'wall': load_image('air_level.png'),
    'empty': load_image('air_level2.png')}
tile_images_terra = {
    'wall': load_image('terra_level.png'),
    'empty': load_image('terra_level2.png')}
player_image = load_image('mar.png')
tile_width = 50
tile_height = 50


def start_screen():  #создание стартового окна
    global running
    intro_text = ["ЛАБИРИНТЫ СТИХИЙ", "",
                  "Проходи лабиринты разной сложности"]
    fullname = os.path.join('data', 'fon.jpg')
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    fon = pygame.transform.scale(image, (700, 700))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 20
        intro_rect.top = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for v in pygame.event.get():
            if v.type == pygame.QUIT:
                end_screen()
                running = False
            elif v.type == pygame.KEYDOWN or \
                    v.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def finish_screen():  #окно с поздравление о прохождении лабиринта
    global running
    intro_text = ["ПОЗДРАВЛЯЮ!", "",
                  "Ты прошел лабиринт"]
    fullname = os.path.join('data', 'win.jpg')
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    fon = pygame.transform.scale(image, (700, 700))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 550
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for v in pygame.event.get():
            if v.type == pygame.QUIT:
                end_screen()
                running = False
            elif v.type == pygame.KEYDOWN or \
                    v.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def end_screen():  #окно при выходе из приложения
    global running
    intro_text = ["До новых встреч!", ""]
    fullname = os.path.join('data', 'end.jpg')
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    fon = pygame.transform.scale(image, (700, 700))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 350
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for v in pygame.event.get():
            if v.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif v.type == pygame.KEYDOWN or \
                    v.type == pygame.MOUSEBUTTONDOWN:
                running = False
                pygame.quit()
        pygame.display.flip()


class SpriteGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):  #класс плиток в уровне
    def __init__(self, tile, tile_type, pos_x, pos_y, group):
        super().__init__(group)
        self.image = tile[tile_type]
        x = tile_width * pos_x
        y = tile_width * pos_y
        self.rect = self.image.get_rect().move(x, y)
        self.abs_pos = (self.rect.x, self.rect.y)


class Player(Sprite):  #класс для создания игрока на уровне
    def __init__(self, pos_x, pos_y, group2):
        super().__init__(group2)
        self.image = player_image
        x = tile_width * pos_x + 15
        y = tile_height * pos_y + 5
        self.rect = self.image.get_rect().move(x, y)
        self.pos = (pos_x, pos_y)

    def move(self, x, y, group, name):
        x2 = tile_width * (x - self.pos[0])
        y2 = tile_height * (y - self.pos[1])
        vid_pos[name][0] -= x2
        vid_pos[name][1] -= y2
        self.pos = (x, y)
        camera.dx = vid_pos[name][0]
        camera.dy = vid_pos[name][1]
        for sprite in group:
            camera.apply(sprite)


class Camera:  #класс камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x = obj.abs_pos[0] + self.dx
        obj.rect.y = obj.abs_pos[1] + self.dy

    def update(self, target):
        self.dx = 0
        self.dy = 0


class AnimatedSprite(pygame.sprite.Sprite):  #класс спрайтов анимация
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        xx = sheet.get_width() // columns
        yy = sheet.get_height() // rows
        self.rect = pygame.Rect(0, 0, xx, yy)
        for j in range(rows):
            for i in range(columns):
                x2 = self.rect.w * i
                y2 = self.rect.h * j
                frame_location = (x2, y2)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


player = None
running = True
clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()
sprite_group2 = SpriteGroup()
hero_group2 = SpriteGroup()
sprite_group3 = SpriteGroup()
hero_group3 = SpriteGroup()
sprite_group4 = SpriteGroup()
hero_group4 = SpriteGroup()


def load_level(filename):  #загрузка уровня
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def generate_level(im_level, level, group, group_hiro):  #генерация уровня
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile(im_level, 'empty', x, y, group)
            elif level[y][x] == '#':
                Tile(im_level, 'wall', x, y, group)
            elif level[y][x] == '@':
                Tile(im_level, 'empty', x, y, group)
                new_player = Player(x, y, group_hiro)
                level[y][x] = "."
    return new_player, x, y


def move(heros, movement, lmap):  #перемещения игрока на уровне
    x, y = heros.pos
    global hods_levels, red_circle
    a = ''
    g = None
    if name_lavel == 'Fire':
        hods_levels[0] += 1
        a = 'Fire'
        g = sprite_group
    elif name_lavel == 'Water':
        hods_levels[1] += 1
        a = 'Water'
        g = sprite_group2
    elif name_lavel == 'Terra':
        hods_levels[2] += 1
        a = 'Terra'
        g = sprite_group3
    elif name_lavel == 'Air':
        hods_levels[3] += 1
        a = 'Air'
        g = sprite_group4
    if movement == "up":
        if y > 0 and lmap[y - 1][x] == ".":
            y -= 1
            red_circle[a] = (red_circle[a][0], red_circle[a][1] - 5)
    elif movement == "down":
        if y < max_y - 1 and lmap[y + 1][x] == ".":
            y += 1
            red_circle[a] = (red_circle[a][0], red_circle[a][1] + 5)
    elif movement == "left":
        if x > 0 and lmap[y][x - 1] == ".":
            x -= 1
            red_circle[a] = (red_circle[a][0] - 5, red_circle[a][1])
    elif movement == "right":
        if x < max_x - 1 and lmap[y][x + 1] == ".":
            x += 1
            red_circle[a] = (red_circle[a][0] + 5, red_circle[a][1])
    heros.move(x, y, g, a)
    if (x, y) == win_pos[a]:
        finish_screen()


flag_if_level = True
start_screen()
fl1 = True
gruops = {'Fire': sprite_group, 'Water': sprite_group2, 'Terra': sprite_group3, 'Air': sprite_group4}
level_sprites = pygame.sprite.Group()
door_sprite = pygame.sprite.Group()


def creat_levels():  #создание уровней
    Levels(level_sprites, image_water, (50, 170), 'Water')
    Levels(level_sprites, image_fire, (400, 170), 'Fire')
    Levels(level_sprites, image_air, (400, 400), 'Air')
    Levels(level_sprites, image_terra, (50, 400), 'Terra')
    Levels(door_sprite, image_door, (637, 0), 'Door')


red_circle = {'Fire': (351, 351), 'Water': (402, 402), 'Air': (602, 602), 'Terra': (504, 504)}
win_pos = {'Fire': (69, 69), 'Water': (59, 59), 'Air': (19, 19), 'Terra': (39, 39)}
camera = Camera()
level_map = load_level('map_fire.txt')
level_map2 = load_level('map_water.txt')
level_map3 = load_level('map_terra.txt')
level_map4 = load_level('map_air.txt')
hero1, max_x1, max_y1 = generate_level(tile_images_fire, level_map, sprite_group, hero_group)
hero2, max_x2, max_y2 = generate_level(tile_images_water, level_map2, sprite_group2, hero_group2)
hero3, max_x3, max_y3 = generate_level(tile_images_terra, level_map3, sprite_group3, hero_group3)
hero4, max_x4, max_y4 = generate_level(tile_images_air, level_map4, sprite_group4, hero_group4)
hero = None
max_x = None
max_y = None
lmap = ''
vid_pos = {'Fire': [0, 0], 'Water': [0, 0], 'Air': [0, 0], 'Terra': [0, 0]}
camera.update(hero)
creat_levels()
hods_levels = [0, 0, 0, 0]
all_sprites = pygame.sprite.Group()


class Stars(pygame.sprite.Sprite):  #класс летающих звездочек
    def __init__(self, radius, x, y):
        super().__init__(star_sprites)
        self.radius = radius
        self.image = pygame.image.load('data/star.png')
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.randint(1, 15)
        self.vy = random.randrange(1, 15)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
star_sprites = pygame.sprite.Group()


class Border(pygame.sprite.Sprite):  #класс стенок от которых будут отталикиваться звездочки
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


Border(5, 5, 700 - 5, 5)
Border(5, 700 - 5, 700 - 5, 700 - 5)
Border(5, 5, 5, 700 - 5)
Border(700 - 5, 5, 700 - 5, 700 - 5)
for i in range(20):
    Stars(20, 100, 100)


def beautiful_sprite():  #создание анимации рядом с уровнями
    AnimatedSprite(load_image("fire_sprite.png"), 4, 4, 340, -80)
    AnimatedSprite(load_image("aaa.png"), 5, 6, 50, 470)
    AnimatedSprite(load_image("bbb.png"), 5, 6, 400, 470)
    AnimatedSprite(load_image("ggg.png"), 5, 6, 50, -15)

#замена стандартного курсора
kursor = pygame.sprite.Group()
cursor_image = load_image("arrow.png")
cursor = pygame.sprite.Sprite(kursor)
cursor.image = cursor_image
cursor.rect = cursor.image.get_rect()
pygame.mouse.set_visible(False)
beautiful_sprite()
clock = pygame.time.Clock()
FPS = 25
running = True
f = pygame.font.SysFont('freesanbold.ttf', 48)
while running:  #цыкл игры
    if fl_lavels_or_maze:
        all_sprites.draw(screen)
        all_sprites.update()
        star_sprites.draw(screen)
        for bomb in star_sprites:
            bomb.update()
        level_sprites.draw(screen)
        t = f.render(str(hods_levels[0]), True, (255, 255, 255))
        screen.blit(t, (400, 260))
        t = f.render(str(hods_levels[1]), True, (255, 255, 255))
        screen.blit(t, (50, 260))
        t = f.render(str(hods_levels[2]), True, (255, 255, 255))
        screen.blit(t, (50, 490))
        t = f.render(str(hods_levels[3]), True, (255, 255, 255))
        screen.blit(t, (400, 490))
    if name_lavel == 'Fire':
        hero = hero1
        max_x = max_x1
        max_y = max_y1
        lmap = level_map
        sprite_group.draw(screen)
        hero_group.draw(screen)
        pygame.draw.rect(screen, (0, 0, 0),
                         (625, 0, 700, 120))
        t = f.render(str(hods_levels[0]), True, (255, 255, 255))
        screen.blit(t, (645, 75))
        im = pygame.image.load('data/maze (4).png')
        maze = pygame.transform.scale(im, (355, 355))
        screen.blit(maze, (345, 345))
        pygame.draw.circle(screen, (255, 0, 0),
                           red_circle['Fire'], 4)
        door_sprite.draw(screen)
    elif name_lavel == 'Water':
        max_x = max_x2
        max_y = max_y2
        hero = hero2
        lmap = level_map2
        sprite_group2.draw(screen)
        hero_group2.draw(screen)
        pygame.draw.rect(screen, (0, 0, 0),
                         (625, 0, 700, 120))
        t = f.render(str(hods_levels[1]), True, (255, 255, 255))
        screen.blit(t, (645, 75))
        im = pygame.image.load('data/maze (3).png')
        maze = pygame.transform.scale(im, (305, 305))
        screen.blit(maze, (395, 395))
        pygame.draw.circle(screen, (255, 0, 0),
                           red_circle['Water'], 4)
        door_sprite.draw(screen)
    elif name_lavel == 'Terra':
        hero = hero3
        max_x = max_x3
        max_y = max_y3
        lmap = level_map3
        sprite_group3.draw(screen)
        hero_group3.draw(screen)
        pygame.draw.rect(screen, (0, 0, 0),
                         (625, 0, 700, 120))
        t = f.render(str(hods_levels[2]), True, (255, 255, 255))
        screen.blit(t, (645, 75))
        im = pygame.image.load('data/maze (2).png')
        maze = pygame.transform.scale(im, (205, 205))
        screen.blit(maze, (495, 495))
        pygame.draw.circle(screen, (255, 0, 0),
                           red_circle['Terra'], 4)
        door_sprite.draw(screen)
    elif name_lavel == 'Air':
        hero = hero4
        max_x = max_x4
        max_y = max_y4
        lmap = level_map4
        sprite_group4.draw(screen)
        hero_group4.draw(screen)
        pygame.draw.rect(screen, (0, 0, 0),
                         (625, 0, 700, 120))
        t = f.render(str(hods_levels[3]), True, (255, 255, 255))
        screen.blit(t, (645, 75))
        im = pygame.image.load('data/maze (1).png')
        maze = pygame.transform.scale(im, (105, 105))
        screen.blit(maze, (595, 595))
        pygame.draw.circle(screen, (255, 0, 0),
                           red_circle['Air'], 4)
        door_sprite.draw(screen)
    elif name_lavel == 'Door' and not fl_lavels_or_maze:
        fl_lavels_or_maze = True
        name_lavel = ''
    for event in pygame.event.get():  #обработка событий
        if event.type == pygame.QUIT:
            end_screen()
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if name_lavel == 'Fire':
                if event.key == pygame.K_UP:
                    move(hero1, "up", lmap)
                elif event.key == pygame.K_DOWN:
                    move(hero1, "down", lmap)
                elif event.key == pygame.K_LEFT:
                    move(hero1, "left", lmap)
                elif event.key == pygame.K_RIGHT:
                    move(hero1, "right", lmap)
            elif name_lavel == 'Water':
                if event.key == pygame.K_UP:
                    move(hero2, "up", lmap)
                elif event.key == pygame.K_DOWN:
                    move(hero2, "down", lmap)
                elif event.key == pygame.K_LEFT:
                    move(hero2, "left", lmap)
                elif event.key == pygame.K_RIGHT:
                    move(hero2, "right", lmap)
            elif name_lavel == 'Terra':
                if event.key == pygame.K_UP:
                    move(hero3, "up", lmap)
                elif event.key == pygame.K_DOWN:
                    move(hero3, "down", lmap)
                elif event.key == pygame.K_LEFT:
                    move(hero3, "left", lmap)
                elif event.key == pygame.K_RIGHT:
                    move(hero3, "right", lmap)
            elif name_lavel == 'Air':
                if event.key == pygame.K_UP:
                    move(hero4, "up", lmap)
                elif event.key == pygame.K_DOWN:
                    move(hero4, "down", lmap)
                elif event.key == pygame.K_LEFT:
                    move(hero4, "left", lmap)
                elif event.key == pygame.K_RIGHT:
                    move(hero4, "right", lmap)
        if event.type == pygame.MOUSEMOTION:
            cursor.rect.topleft = event.pos
        door_sprite.update(event)
        level_sprites.update(event)
    if pygame.mouse.get_focused():
        kursor.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
    screen.fill((0, 0, 0))
pygame.quit()
