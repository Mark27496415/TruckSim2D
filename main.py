import pygame
import random
import pygame_menu

# Настройки
WIDTH = 600
HEIGHT = 700

START_SPEED = 5  # Начальная скорость
SPEED_INCREMENT = 0.5  # Приращение скорости при нажатии клавиш

SPAWN_DISTANCE = 340  # Минимальное расстояние между объектами
MAX_STONES = 1  # Максимальное количество камней на экране
MAX_MONEY_BAGS = 1  # Максимальное количество мешков с деньгами на экране

# Инициализация Pygame
pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TruckSim 2D")
clock = pygame.time.Clock()

# Спрайты
class Player(pygame.sprite.Sprite): # МАШИНКА
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("самосвал-removebg-preview.png")
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect(center=(x, y))


    def update(self): #ОБНОВЛЕНИЕ СОСТОЯНИЯ МАШИНКИ
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += 15  # Движение вправо
            if self.rect.right > WIDTH:  # Проверка правой границы
                self.rect.right = WIDTH
        if keys[pygame.K_LEFT]:
            self.rect.x -= 15 # Движение влево
            if self.rect.left < 0:  # Проверка левой границы
                self.rect.left = 0
        if keys[pygame.K_UP]:
            self.rect.y -= 10
            if self.rect.top < 0:  # Проверка верхней границы
                self.rect.top = 0
        if keys[pygame.K_DOWN]:
            self.rect.y += 10
            if self.rect.bottom > HEIGHT :  # Проверка нижней границы
                self.rect.bottom = HEIGHT

class Money(pygame.sprite.Sprite):#МЕШОК С ДЕНЬГАМИ
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("мешок_с_деньгами-removebg-preview.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=(x, y))

class Stone(pygame.sprite.Sprite):#КАМЕНЬ
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("камень-removebg-preview.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=(x, y))



        #  Отрисовка текста
def draw_text(text, pos, color=(0, 0, 0)):
    font = pygame.font.Font(None, 36)
    text_img = font.render(text, True,color)
    display.blit(text_img, pos)


def start_the_game():
    game_loop()

def spawn_objects(money_bags, stones, last_spawn_y):
    #Спавн мешков с деньгами и камней

    # Спавн мешков, если их меньше максимального количества
    if len(money_bags) < MAX_MONEY_BAGS:
        money_bags.add(Money(random.randint(0, WIDTH), random.randint(0, 150) ))
    # Спавн камней, если их меньше максимального количества
    if len(stones) < MAX_STONES:
        stones.add(Stone(random.randint(0, WIDTH), random.randint(0, 150) ))

    last_spawn_y = SPAWN_DISTANCE  # хранит Y-координату последнего спавна объекта

    # объекты спавнятся с отступом друг от друга и не выходят за пределы экрана.
    if last_spawn_y > HEIGHT:
        last_spawn_y = 0  #чтобы следующий спавн объектов начинался с самого верха экрана

    return last_spawn_y

def game_loop():    #  ИГРОВОЙ ПРОЦЕСС
    global player,score
    player = Player(WIDTH // 2, HEIGHT - 150)  # Позиция машинки
    all_sprites = pygame.sprite.Group(player)
    money_bags = pygame.sprite.Group()
    stones = pygame.sprite.Group()

    #  Загрузка фона
    bg = pygame.image.load('дорога_без_черт-removebg-preview (1)вери гуд.png')
    bg = pygame.transform.scale(bg, (600, 700))
    bg_width = bg.get_width()
    bg_height = bg.get_height()
    bg_x = 0
    bg_y = 0

    score = 0
    road_speed = START_SPEED  # Скорость дороги
    last_spawn_y = 0  # Позиция последнего спавна по оси Y

    # Главный цикл игры
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Проверка условия окончания игры
        if score < -3:
            running = False  # Завершаем цикл игры
            game_over_menu()


        # Обновление
        player.update()

        #  Скроллинг фона(Когда фон достигает нижней границы экрана, он перемещается наверх,
        bg_y += road_speed  # Движение дороги вниз( СКРОЛИНГ ) со скоростью road_speed
        if bg_y >= bg_height - HEIGHT:  # Проверка нижней границы(вышла ли нижняя часть экрана за пределы окна)
            bg_y = bg_height - HEIGHT  #если вышла, то значение bg_y сбрасывается так, чтобы верхняя граница фона совпала с верхней границей экрана
        # Обновляем позиции мешков и камней
        for money_bag in money_bags:
            money_bag.rect.y += road_speed
            if money_bag.rect.bottom > HEIGHT or pygame.sprite.collide_rect(player, money_bag):
                money_bag.kill()
        for stone in stones:
            stone.rect.y += road_speed
            if stone.rect.bottom > HEIGHT or pygame.sprite.collide_rect(player, stone):
                stone.kill()

        #  Спавн мешков и камней
        last_spawn_y = spawn_objects(money_bags, stones, last_spawn_y)  # вызов функции spawn_objects()

        # Обновляем позиции мешков и камней
        for money_bag in money_bags:
            money_bag.rect.y += road_speed
            if money_bag.rect.bottom > HEIGHT: # ВЫХОД ЗА НИЖНИЙ КРАЙ
                money_bag.kill()
            if pygame.sprite.collide_rect(player, money_bag): # СТОЛКНОВКНИЕ МЕШКА С МАШИНОЙ
                money_bag.kill()
                score += 1

        for stone in stones:
            stone.rect.y += road_speed
            if stone.rect.bottom > HEIGHT: # ВЫХОД ЗА НИЖНИЙ КРАЙ
                stone.kill()
            if pygame.sprite.collide_rect(player, stone): # СТОЛКНОВКНИЕ КАМНЯ С МАШИНОЙ
                score -= 1


        #  Отрисовка
        display.fill((0, 0, 0))
        display.blit(bg, (bg_x, bg_y))  # Отрисовка фона
        all_sprites.draw(display)
        money_bags.draw(display)
        stones.draw(display)
        draw_text(f"Score: {score}", (10, 10), color = (255, 255, 255) )  # Вывод счета
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def show_menu():
    menu = pygame_menu.Menu('TruckSim 2D', 300, 400, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Играть', start_the_game)
    menu.add.button('Выход', pygame_menu.events.EXIT)
    menu.mainloop(display)

def game_over_menu():
    menu = pygame_menu.Menu('Игра окончена', 300, 400, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Выйти', pygame_menu.events.EXIT)
    menu.add.button('Рестарт', start_the_game)  # Запускаем игру снова
    menu.mainloop(display)

#  Запуск игры
show_menu()