import pygame
import random
import pygame_gui
import os

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


pygame.init()
pygame.display.set_caption('Dino')
width, height = 1000, 650
screen = pygame.display.set_mode((width, height))
manager = pygame_gui.UIManager((width, height))
fon = load_image('fon.jpg')
running = True
fps = 500
clock = pygame.time.Clock()
screen.blit(fon, (0, 0))
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
font = pygame.font.SysFont('sitkasmallsitkatextbolditalicsitkasubheadingbolditalicsitkaheading'
                           'bolditalicsitkadisplaybolditalicsitkabannerbolditalic', 70)
text = font.render('Dino Game', 1, (255, 0, 0))
screen.blit(text, (305, 60))
print(pygame.font.get_fonts())
while running:
    timedelta = clock.tick(600) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element.text == 'Начать игру':
                    print('Начать игру')
                elif event.ui_element.text == 'Продолжить игру':
                    print('Продолжить игру')
                elif event.ui_element.text == 'Ваши рекорды':
                    print('Ваши рекорды')
                elif event.ui_element.text == 'Выйти из игры':
                    running = False
        manager.process_events(event)
    manager.update(timedelta)
    manager.draw_ui(screen)
    pygame.display.update()