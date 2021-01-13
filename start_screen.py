import os
import random
import sqlite3
import sys
import pygame
import pygame_gui
import pickle


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("green"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx, self.vy = 0, 0
        while int(self.vx) == 0 or int(self.vy) == 0:
            self.vx = random.randint(-30, 30)
            self.vy = random.randint(-30, 30)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if self.rect.y <= 0 or self.rect.y >= height:
            self.vy = -self.vy
        if self.rect.x <= 0 or self.rect.x >= width:
            self.vx = -self.vx


class Scene(object):
    def __init__(self):
        pass

    def render(self, screen):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError


class EndScene(Scene):
    def __init__(self, x, y):
        super().__init__()
        # для работы магазина
        self.time_score = 0
        screen.fill((0, 0, 0))
        all_sprites.empty()
        self.TIMER_EVENT_TYPE1 = pygame.NUMEVENTS - 1
        pygame.time.set_timer(self.TIMER_EVENT_TYPE1, 1000)
        for i in range(50):
            Ball(20, x, y)
        self.font = pygame.font.SysFont('sitkasmallsitkatextbolditalicsitkasubheadingbolditalicsitkaheading'
                                        'bolditalicsitkadisplaybolditalicsitkabannerbolditalic', 70)
        self.text = self.font.render('Game Over', 1, (199, 0, 0))
        self.font1 = pygame.font.SysFont('sitkasmallsitkatextbolditalicsitkasubheadingbolditalicsitkaheading'
                                        'bolditalicsitkadisplaybolditalicsitkabannerbolditalic', 20)
        self.text1 = self.font1.render('Для продолжения нажмите Enter', 1, (199, 0, 0))

    def update(self):
        all_sprites.draw(screen)
        all_sprites.update()

    def handle_events(self, events):
        global scene, gameover
        for e in events:
            if e.type == self.TIMER_EVENT_TYPE1:
                all_sprites.empty()
                screen.fill('green')
                text_x = width // 2 - self.text.get_width() // 2
                text_y = height // 2 - self.text.get_height() // 2
                text_w = self.text.get_width()
                text_h = self.text.get_height()
                screen.blit(self.text, (text_x, text_y))
                pygame.draw.rect(screen, (199, 0, 0), (text_x - 10, text_y - 10,
                                                       text_w + 20, text_h + 20), 5)

                screen.blit(self.text1, (text_x + 10, text_y + text_h + 20))
                gameover = False
            if not gameover and e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    pygame.time.set_timer(self.TIMER_EVENT_TYPE1, 0)
                    scene = MainScene()


class GameScene(Scene):
    global orig_dino, orig_fon, orig_pter, orig_cactus

    def __init__(self):
        super().__init__()
        manager.clear_and_reset()
        # для работы магазина
        self.time_score = 0
        self.new_part = 10
        self.TIMER_EVENT_TYPE = pygame.USEREVENT + 1
        self.TIMER_EVENT_CAKTUS = self.TIMER_EVENT_TYPE + 1
        self.TIMER_EVENT_BIRD = self.TIMER_EVENT_CAKTUS + 1
        pygame.time.set_timer(self.TIMER_EVENT_TYPE, 1000)
        pygame.time.set_timer(self.TIMER_EVENT_CAKTUS, 10)
        pygame.time.set_timer(self.TIMER_EVENT_BIRD, 4000)
        manager.clear_and_reset()
        self.time_day = 0
        self.time_score = 0
        self.font = pygame.font.Font(None, 30)
        self.desert = images['desert']
        self.desert = pygame.transform.scale(self.desert, (width, height))
        self.bird_init = 0
        n = 50
        for i in range(102):
            Ground(height, width - 1000 + n * i)

    def update(self):
        global fps, paused
        if not paused:
            if self.new_part == 10:
                Ground(height, width)
                self.new_part = 0
            else:
                self.new_part += 1
            if self.bird_init == 0:
                self.bird_init = random.randint(2, 7)
            self.time_score += 0.02
            text = self.font.render(f'Ваш счёт: {int(self.time_score // 1)}', 1, (255, 0, 0))
            if int(self.time_score // 1) > 10:
                fps = 90
            self.time_day += 1
            screen.fill((255, 255, 255))
            screen.blit(self.desert, (0, 0))
            all_sprites.update()
            all_sprites.draw(screen)
            screen.blit(text, (20, 20))
            if self.time_day >= 2000:
                pass

    def handle_events(self, e):
        global paused, scene, last_save
        for events in e:
            if events.type == pygame.KEYDOWN:
                if not paused:
                    if events.key == pygame.K_w or events.key == pygame.K_SPACE or events.key == pygame.K_UP:
                        if self.dino.jump == 0:
                            self.dino.jump = 170
                    elif events.key == pygame.K_p:
                        paused = True
                # experimental
                else:
                    paused = False
                if events.key == pygame.K_ESCAPE:
                    with open('data/save.dat', 'wb') as file:
                        scene.dino = None
                        scene.ground = None
                        scene.desert = None
                        scene.font = None
                        pickle.dump(scene, file)
                        last_save = True
                    scene = MainScene()

            if not paused:
                if events.type == self.TIMER_EVENT_CAKTUS:
                    self.bird_init -= 1
                    if orig_cactus:
                        AnimatedCactus(self.ground.rect.top, load_image("CactusOriginalSheet.png"), 4, 1)
                    elif not orig_cactus:
                        Cactus(self.ground.rect.top)
                    if self.bird_init == 0:
                        if orig_pter:
                            Bird(load_image("bird/PterOriginalSheet.png"), 2, 1)
                        elif not orig_pter:
                            Bird(load_image("bird/BluePterSheetReversedDemo.png"), 9, 1)
                        self.bird_init = 0
                        if fps == 60:
                            pygame.time.set_timer(self.TIMER_EVENT_CAKTUS, random.randint(2400, 3400))
                        else:
                            pygame.time.set_timer(self.TIMER_EVENT_CAKTUS, random.randint(1500, 2400))
                    else:
                        if fps == 60:
                            pygame.time.set_timer(self.TIMER_EVENT_CAKTUS, random.randint(2100, 2500))
                        else:
                            pygame.time.set_timer(self.TIMER_EVENT_CAKTUS, random.randint(1300, 1700))


class MainScene(Scene):
    def __init__(self):
        super().__init__()
        self.fon = load_image('fon.jpg')
        self.font = pygame.font.SysFont('sitkasmallsitkatextbolditalicsitkasubheadingbolditalicsitkaheading'
                                        'bolditalicsitkadisplaybolditalicsitkabannerbolditalic', 70)
        self.time_score = 0
        self.shop_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 540), (125, 75)),
                                                         text='Магазин',
                                                         manager=manager)
        self.begin_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 180), (300, 75)),
                                                         text='Начать игру',
                                                         manager=manager)

        self.continue_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 300), (300, 75)),
                                                            text='Продолжить игру',
                                                            manager=manager)

        if not last_save:
            self.continue_button.set_text('Нет сохранений')
            self.continue_button.disable()
        self.records_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 420), (300, 75)),
                                                           text='Ваши рекорды',
                                                           manager=manager)
        self.end_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 540), (300, 75)),
                                                       text='Выйти из игры',
                                                       manager=manager)

        self.player_name = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((380, 135), (250, 200)),
                                                               manager=manager)
        self.rules = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width - 150, 540), (125, 75)),
                                                       text='Правила игры',
                                                       manager=manager)
        self.player_name.set_text('Введите имя игрока')
        self.text = self.font.render('Dino Game', 1, (255, 0, 0))
        self.exit_btn = None
        self.table = None
        self.buttons = [self.begin_button, self.continue_button, self.records_button,
                        self.end_button, self.player_name, self.rules, self.shop_button]

    def update(self):
        screen.blit(self.fon, (0, 0))
        screen.blit(self.text, (305, 50))
        manager.update(timedelta)
        manager.draw_ui(screen)

    def handle_events(self, events):
        global scene, player, money
        for event in events:
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element.text == 'Магазин':
                        scene = ShopScene(money)
                    if event.ui_element.text == 'Начать игру':
                        name = self.player_name.get_text()
                        if name != 'Для игры требуется ввести имя' and name != 'Введите имя игрока' and name:
                            player = name
                            scene = GameScene()
                            if orig_dino:
                                scene.dino = Dino(load_image("dino/DinoOriginalSheet.png"), 5, 1)
                            elif not orig_dino:
                                scene.dino = Dino(load_image("dino/dinosheet.png"), 2, 1)
                            if not orig_fon:
                                scene.desert = images['desert']
                            elif orig_fon:
                                scene.desert = images['orig_fon']
                            scene.ground = Ground(height, width)
                            scene.font = pygame.font.Font(None, 30)
                        else:
                            self.player_name.set_text('Для игры требуется ввести имя')
                    elif event.ui_element.text == 'Продолжить игру':
                        with open('data/save.dat', 'rb') as file:
                            scene = pickle.load(file)
                            scene.dino = player_group.sprites()[0]
                            if not orig_fon:
                                scene.desert = images['desert']
                            elif orig_fon:
                                scene.desert = images['orig_fon']
                            scene.ground = Ground(height, width)
                            scene.font = pygame.font.Font(None, 30)
                    elif event.ui_element.text == 'Ваши рекорды':
                        self.show_records()
                    elif event.ui_element.text == 'Правила игры':
                        self.show_rules()
                    elif event.ui_element.text == 'Выйти из игры':
                        pygame.quit()
                        exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if self.player_name.rect.x <= x <= self.player_name.rect.right and \
                        self.player_name.rect.y <= y <= self.player_name.rect.bottom:
                    self.player_name.set_text('')
            if self.exit_btn:
                if self.exit_btn.check_pressed():
                    self.exit_btn.hide()
                    self.table.hide()
                    for elem in self.buttons:
                        elem.show()
            manager.process_events(event)

    def show_records(self):
        for elem in self.buttons:
            elem.hide()
        self.exit_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (120, 50)),
                                                text='Выйти в меню',
                                                manager=manager)
        data = cur.execute('SELECT name, score FROM records ORDER BY SCORE DESC').fetchall()
        max_size = 0
        for elem, score in data:
            max_size = max(max_size, len(elem + str(score)))
        max_size += 2
        for i, (elem, score) in enumerate(data):
            score = str(score)
            space = ' ' * (max_size - len(elem + score))
            data[i] = elem + space + score
        self.table = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((300, 150), (400, 400)),
                                                         item_list=data, starting_height=222,
                                                         manager=manager)

    def show_rules(self):
        for elem in self.buttons:
            elem.hide()
        self.exit_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (120, 50)),
                                                     text='Выйти в меню',
                                                     manager=manager)
        text = "Добро пожаловать в игру, новичок!<br>" + \
               "Отключали ли когда-то у тебя интернет? Уверен, что да.<br>" + \
               "Значит, ты тоже играл в динозаврика в Google Chrome, не так ли?<br>" + \
               "Перед тобой та самая игра про динозавра - DinoGame!<br>" + \
               "В нашей игре предельно простые правила, а для управления нужна лишь кнопка Space или стрелочки.<br>" + \
               "Пауза включается на английскую P.<br>" + \
               "Цель игры: продержаться как можно дольше, избегая кактусов и птеродактилей.<br>" +\
               "Жизней нет, у тебя один шанс. Удачи!"
        self.table = pygame_gui.elements.UITextBox(html_text=text,
                                                   relative_rect=pygame.Rect((300, 200), (400, 400)),
                                                   manager=manager)


class ShopScene(Scene):
    global orig_fon, orig_dino, orig_pter, orig_cactus, money, dino_bought, cactus_bought, pter_bought, fon_bought,\
        pack_bought

    def __init__(self, money):
        super().__init__()
        manager.clear_and_reset()
        self.dino = pygame.sprite.Sprite(shop_sprites)
        self.dino.image = images['DinoOriginal']
        self.dino.rect = self.dino.image.get_rect()
        self.dino.rect.x = 200
        self.dino.rect.y = 270
        self.cactus = pygame.sprite.Sprite(shop_sprites)
        self.cactus.image = images['CactusOriginal']
        self.cactus.rect = self.cactus.image.get_rect()
        self.cactus.rect.x = 265
        self.cactus.rect.y = 450
        self.pter = pygame.sprite.Sprite(shop_sprites)
        self.pter.image = images['PterOriginal']
        self.pter.rect = self.pter.image.get_rect()
        self.pter.rect.x = 700
        self.pter.rect.y = 270
        self.dino2 = pygame.sprite.Sprite(shop_sprites)
        self.dino2.image = images['DinoOriginal']
        self.dino2.rect = self.dino2.image.get_rect()
        self.dino2.rect.x = 560
        self.dino2.rect.y = 450
        self.cactus2 = pygame.sprite.Sprite(shop_sprites)
        self.cactus2.image = images['CactusOriginal']
        self.cactus2.rect = self.cactus2.image.get_rect()
        self.cactus2.rect.x = 665
        self.cactus2.rect.y = 450
        self.pter2 = pygame.sprite.Sprite(shop_sprites)
        self.pter2.image = images['PterOriginal']
        self.pter2.rect = self.pter2.image.get_rect()
        self.pter2.rect.x = 730
        self.pter2.rect.y = 450
        self.rules_pressed = False
        # self.tick = pygame.sprite.Sprite(all_sprites)
        # self.tick.image = images['tick']
        # self.tick.rect = self.tick.image.get_rect()
        self.fon = load_image('dinos.jpg')
        self.font = pygame.font.SysFont('sitkasmallsitkatextbolditalicsitkasubheadingbolditalicsitkaheading'
                                        'bolditalicsitkadisplaybolditalicsitkabannerbolditalic', 70)
        self.money_font = pygame.font.SysFont('sitkasmallsitkatextbolditalicsitkasubheadingbolditalicsitkaheading'
                                        'bolditalicsitkadisplaybolditalicsitkabannerbolditalic', 40)
        self.rules = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width - 150, 450), (125, 75)),
                                                  text='Руководство',
                                                  manager=manager)
        self.end_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 450), (125, 75)),
                                                       text='Выйти в меню',
                                                       manager=manager)
        self.dino_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 180), (300, 75)),
                                                         text='"Оригинальный" Дино',
                                                         manager=manager)

        self.cactus_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 550), (300, 75)),
                                                            text='"Оригинальный" кактус',
                                                            manager=manager)
        self.pter_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((550, 180), (300, 75)),
                                                           text='"Оригинальный" Птеродактиль',
                                                           manager=manager)
        self.fon_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 280), (300, 75)),
                                                        text='"Оригинальный" фон',
                                                        manager=manager)
        self.pack_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((550, 550), (300, 75)),
                                                       text='"Оригинальный" комплект',
                                                       manager=manager)
        self.buttons = [self.rules, self.end_button, self.dino_button, self.cactus_button,
                        self.pter_button, self.fon_button, self.pack_button]
        self.text = self.font.render('Dino Shop', 1, (255, 0, 0))
        self.price = self.font.render('50', 1, (255, 0, 0))
        self.pack_price = self.font.render('120', 1, (255, 0, 0))
        self.money_text = self.money_font.render(f'Деньги: {int(money)}', 1, (255, 0, 0))
        self.fon_price = self.font.render('20', 1, (255, 0, 0))
        self.exit_btn = None
        self.table = None

    def update(self):
        screen.blit(self.fon, (0, 0))
        screen.blit(self.text, (305, 50))
        if not self.exit_btn:
            screen.blit(self.price, (50, 180))
            screen.blit(self.price, (850, 180))
            screen.blit(self.price, (50, 550))
            screen.blit(self.pack_price, (850, 550))
            screen.blit(self.fon_price, (450, 380))
            screen.blit(self.money_text, (10, 10))
            shop_sprites.draw(screen)
        manager.update(timedelta)
        manager.draw_ui(screen)

    def handle_events(self, events):
        global scene, orig_fon, orig_dino, orig_pter, orig_cactus, money, dino_bought, cactus_bought, pter_bought,\
            fon_bought, pack_bought
        for event in events:
            if event.type == pygame.USEREVENT:
                if self.exit_btn:
                    if self.exit_btn.check_pressed():
                        manager.clear_and_reset()
                        self.__init__(money)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element.text == 'Выйти в меню':
                        for elem in self.buttons:
                            elem.hide()
                        scene = MainScene()
                    if event.ui_element.text == '"Оригинальный" Дино':
                        if not dino_bought:
                            if money >= 50:
                                money = money - 50
                                self.money_text = self.money_font.render(f'Деньги: {money}', 1, (255, 0, 0))
                                dino_bought = True
                        elif dino_bought and not orig_dino:
                            orig_dino = True
                        elif dino_bought and orig_dino:
                            orig_dino = False
                    elif event.ui_element.text == '"Оригинальный" кактус':
                        if not cactus_bought:
                            if money >= 50:
                                money = money - 50
                                self.money_text = self.money_font.render(f'Деньги: {money}', 1, (255, 0, 0))
                                cactus_bought = True
                        elif cactus_bought and not orig_cactus:
                            orig_cactus = True
                        elif cactus_bought and orig_cactus:
                            orig_cactus = False
                    elif event.ui_element.text == '"Оригинальный" Птеродактиль':
                        if not pter_bought:
                            if money >= 50:
                                money = money - 50
                                self.money_text = self.money_font.render(f'Деньги: {money}', 1, (255, 0, 0))
                                pter_bought = True
                        elif pter_bought and not orig_pter:
                            orig_pter = True
                        elif pter_bought and orig_pter:
                            orig_pter = False
                    elif event.ui_element.text == '"Оригинальный" фон':
                        if not fon_bought:
                            if money >= 20:
                                money = money - 20
                                self.money_text = self.money_font.render(f'Деньги: {money}', 1, (255, 0, 0))
                                fon_bought = True
                        elif fon_bought and not orig_fon:
                            orig_fon = True
                        elif fon_bought and orig_fon:
                            orig_fon = False
                    elif event.ui_element.text == '"Оригинальный" комплект':
                        if not pack_bought and money >= 120:
                                money = money - 120
                                dino_bought = True
                                pter_bought = True
                                fon_bought = True
                                cactus_bought = True
                                pack_bought = True
                                self.money_text = self.money_font.render(f'Деньги: {money}', 1, (255, 0, 0))
                        elif pack_bought:
                            if dino_bought and not orig_dino:
                                orig_dino = True
                            elif dino_bought and orig_dino:
                                orig_dino = False
                            if cactus_bought and not orig_cactus:
                                orig_cactus = True
                            elif cactus_bought and orig_cactus:
                                orig_cactus = False
                            if pter_bought and not orig_pter:
                                orig_pter = True
                            elif pter_bought and orig_pter:
                                orig_pter = False
                            if fon_bought and not orig_fon:
                                orig_fon = True
                            elif fon_bought and orig_fon:
                                orig_fon = False
                    elif event.ui_element.text == 'Руководство':
                        self.show_rules()
            manager.process_events(event)

    def show_rules(self):
        manager.clear_and_reset()
        self.exit_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (120, 50)),
                                                     text='Выйти в магазин',
                                                     manager=manager)
        text = "Ого, да вы, похоже, зашли в магазин?!<br>" + \
            "Перед вами находятся товары, а именно скины (облики) для элементов игры.<br>" + \
            "Чтобы их купить, нажмите соответствующую кнопку.<br>" + \
            "Теперь, чтобы использовать скин, нажмите на кнопку снова.<br>" + \
            "Чтобы убрать скин, нажмите на соответствующую кнопку. (удивительно, правда?)<br>" + \
            "Ваш баланс указан в правом верхнем углу."
        self.table = pygame_gui.elements.UITextBox(html_text=text,
                                                   relative_rect=pygame.Rect((300, 200), (400, 400)),
                                                   manager=manager)


class Dino(pygame.sprite.Sprite):
    global orig_dino

    def __init__(self, sheet, columns, rows):
        super().__init__(player_group, all_sprites)
        self.iter_count = 0
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        # self.rect = self.rect.move(x, y)
        # self.image = load_image(r'dino\dino1_a.png', -1)
        # self.image = pygame.transform.scale(self.image, (self.image.get_width() + 30,
        #                                                  self.image.get_height() + 30))
        self.jump = 0
        if orig_dino:
            self.rect = self.image.get_rect().move(
                90, height - height // 6 - self.image.get_height() + 20)
            self.mask = pygame.mask.from_surface(self.image)
        elif not orig_dino:
            self.rect = self.image.get_rect().move(
                90, height - height // 6 - self.image.get_height() + 45)
            self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.iter_count == 15:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.iter_count = 0
        else:
            self.iter_count += 1
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
    def __init__(self, y, x):
        super().__init__(all_sprites)
        if not orig_fon:
            self.grass_parts = [images['grass1'], images['grass2'], images['grass3'], images['grass4']]
        elif orig_fon:
            self.grass_parts = [images['orig_ground']]
        self.image = random.choice(self.grass_parts)
        # self.image = pygame.transform.scale(self.image, (width, height // 6))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.left = x

    def update(self):
        self.rect.x -= 3
        if self.rect.right < 0:
            self.kill()


class Bird(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows):
        super().__init__(enemy_group, all_sprites)
        self.iter_count = 0
        self.frames = []
        self.speed = [3, 5, 7]
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.top = 150
        self.rect.left = width + 200

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        global gameover
        if self.iter_count == 15:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.iter_count = 0
        else:
            self.iter_count += 1
        self.rect.x -= 3
        if self.rect.x < 0:
            self.kill()
            print(1)
        if pygame.sprite.collide_mask(self, scene.dino):
            gameover = True


class Cactus(pygame.sprite.Sprite):
    def __init__(self, bot):
        super().__init__(enemy_group, all_sprites)
        self.image = images['cactus']
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 5,
                                                         random.randint(90, 170)))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.bottom = bot + 10
        self.rect.left = width
        self.speed = [3, 4, 5]

    def update(self):
        global gameover
        self.rect.x -= 3
        if self.rect.x < 0:
            self.kill()
        if pygame.sprite.collide_mask(self, scene.dino):
            gameover = True


class AnimatedCactus(pygame.sprite.Sprite):
    def __init__(self, bot, sheet, columns, rows):
        super().__init__(enemy_group, all_sprites)
        self.iter_count = 0
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.bottom = bot + 10
        self.rect.left = width
        self.speed = [3, 4, 5]

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        global gameover
        if self.iter_count == 15:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.iter_count = 0
        else:
            self.iter_count += 1
        self.rect.x -= 3
        if self.rect.x < 0:
            self.kill()
        if pygame.sprite.collide_mask(self, scene.dino):
            gameover = True


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
money = 120
pygame.display.set_caption('Dino')
# dino = None
width, height = 1000, 650
shop_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
world_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
screen = pygame.display.set_mode((width, height))
images = {'grass': load_image('grass1.png'),
          'cactus': load_image('cactus.png'),
          'desert': load_image('desert.jpg'),
          'fon': load_image('fon.jpg'),
          'grass1': load_image('grass_part1.png'),
          'grass2': load_image('grass_part2.png'),
          'grass3': load_image('grass_part3.png'),
          'grass4': load_image('grass_part4.png'),
          'DinoOriginal': load_image('dino/DinoOriginal.png'),
          'CactusOriginal': load_image('CactusOriginal.png'),
          'PterOriginal': load_image('bird/PterOriginal.png'),
          'tick': load_image('tick.png'),
          'orig_fon': load_image('original_background.png'),
          'orig_ground': load_image('OriginalGround.png')}
dino_bought = False
pter_bought = False
cactus_bought = False
fon_bought = False
pack_bought = False
orig_dino = False
orig_cactus = False
orig_pter = False
orig_fon = False
gameover = False
running = True
fps = 60
pygame.mixer.music.load('data/mainmenu.mp3')
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()
manager = pygame_gui.UIManager((width, height))
con = sqlite3.connect('records_db.db')
cur = con.cursor()
player = None
paused = False
last_save = False
scene = MainScene()
while running:
    timedelta = clock.tick(fps) / 1000.0
    if pygame.event.get(pygame.QUIT):
        running = False
    scene.handle_events(pygame.event.get())
    scene.update()
    if gameover and not isinstance(scene, EndScene):
        pygame.time.wait(500)
        cur.execute(f"INSERT INTO records(name, score) VALUES('{player}', {int(scene.time_score // 1)})")
        money = money + scene.time_score // 1
        con.commit()
        pygame.mixer.music.load('data/gameover.mp3')
        pygame.mixer.music.play()
        scene = EndScene(scene.dino.rect.right, scene.dino.rect.bottom)
        fps = 60
        last_save = None
    pygame.display.flip()