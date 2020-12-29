import pygame
import random
import pygame_gui
import os
import sys

# class Ball(pygame.sprite.Sprite):
#     def __init__(self, radius, x, y):
#         super().__init__(all_sprites)
#         self.radius = radius
#         self.image = pygame.Surface((2 * radius, 2 * radius),
#                                     pygame.SRCALPHA, 32)
#         pygame.draw.circle(self.image, pygame.Color("green"),
#                            (radius, radius), radius)
#         self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
#         self.vx, self.vy = 0, 0
#         while int(self.vx) == 0 or int(self.vy) == 0:
#             self.vx = random.randint(-10, 10)
#             self.vy = random.randint(-10, 10)
#
#     def update(self):
#         self.rect = self.rect.move(self.vx, self.vy)
#         if self.rect.y <= 0 or self.rect.y >= height:
#             self.vy = -self.vy
#         if self.rect.x <= 0 or self.rect.x >= width:
#             self.vx = -self.vx
# all_sprites = pygame.sprite.Group()
# for i in range(10):
#     Ball(20, 100, 100)
# pygame.sprite.Group.empty(all_sprites)
# all_sprites.draw(screen)
# all_sprires.update()


class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.image = load_image(r'dino\dino1_a.png', -1)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() + 30,
                                                         self.image.get_height() + 30))
        self.jump = 0
        self.rect = self.image.get_rect().move(
            90, height - height // 6 - self.image.get_height() + 25)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.jump > 0:
            self.rect = self.rect.move(0, -5)
            self.jump -= 3
            if self.jump <= 0:
                self.jump = -170
        elif self.jump < 0:
            self.rect = self.rect.move(0, 5)
            self.jump += 3
            if self.jump >= 0:
                self.jump = 0


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = images['grass']
        self.image = pygame.transform.scale(self.image, (width, height // 6))
        self.rect = self.image.get_rect()
        self.rect.bottom = height


class Cactus(pygame.sprite.Sprite):
    def __init__(self, bot):
        super().__init__(enemy_group, all_sprites)
        self.image = images['cactus']
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 4,
                                                         random.randint(100, 200)))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.bottom = bot + 10
        self.rect.left = width

    def update(self):
        self.rect.x -= 3
        if self.rect.x < 0:
            self.kill()
            print(1)
        if pygame.sprite.collide_mask(self, dino):
            print(100)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def generate_start():
    fon = load_image('fon.jpg')
    begin_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 180), (300, 75)),
                                                text='Начать игру',
                                                manager=manager)

    continue_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 300), (300, 75)),
                                                   text='Продолжить игру',
                                                   manager=manager)
    records_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 420), (300, 75)),
                                                  text='Ваши рекорды',
                                                  manager=manager)
    end_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 540), (300, 75)),
                                              text='Выйти из игры',
                                              manager=manager)
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('sitkasmallsitkatextbolditalicsitkasubheadingbolditalicsitkaheading'
                               'bolditalicsitkadisplaybolditalicsitkabannerbolditalic', 70)
    text = font.render('Dino Game', 1, (255, 0, 0))
    screen.blit(text, (305, 60))


def game():
    global running
    global dino
    run = True
    TIMER_EVENT_TYPE = pygame.USEREVENT + 1
    TIMER_EVENT_CAKTUS = TIMER_EVENT_TYPE + 1
    pygame.time.set_timer(TIMER_EVENT_TYPE, 1000)
    pygame.time.set_timer(TIMER_EVENT_CAKTUS, 1)
    dino = Dino()
    ground = Ground()
    manager.clear_and_reset()
    clock2 = pygame.time.Clock()
    time_day = 0
    while run:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                run = False
                running = False
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_w or events.key == pygame.K_SPACE:
                    if dino.jump == 0:
                        dino.jump = 170
            if events.type == TIMER_EVENT_TYPE:
                font = pygame.font.Font(None, 30)
                text = font.render(f'Ваш счёт: {pygame.time.get_ticks() // 1000}', 1, (255, 0, 0))
                screen.fill((0, 190, 255), (20, 20, text.get_width(), text.get_height()))
                screen.blit(text, (20, 20))
            if events.type == TIMER_EVENT_CAKTUS:
                Cactus(ground.rect.top)
                pygame.time.set_timer(TIMER_EVENT_CAKTUS, random.randint(1500, 2000))
        time_day += clock2.tick(fps)
        screen.fill((255, 255, 255))
        desert = images['desert']
        desert = pygame.transform.scale(desert, (width, height))
        screen.blit(desert, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        dino.x, dino.y = 0, 0
        if time_day >= 2000:
            pass


pygame.init()
pygame.display.set_caption('Dino')
dino = None
width, height = 1000, 650
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
screen = pygame.display.set_mode((width, height))
images = {'grass': load_image('grass1.png'),
          'cactus': load_image('cactus.png'),
          'desert': load_image('desert.jpg'),
          'fon': load_image('fon.jpg')}
running = True
fps = 100
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((width, height))
generate_start()
while running:
    timedelta = clock.tick(600) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element.text == 'Начать игру':
                    game()
                elif event.ui_element.text == 'Продолжить игру':
                    print('Продолжить игру')
                elif event.ui_element.text == 'Ваши рекорды':
                    print('Ваши рекорды')
                elif event.ui_element.text == 'Выйти из игры':
                    running = False
        manager.process_events(event)
    manager.update(timedelta)
    manager.draw_ui(screen)
    pygame.display.flip()