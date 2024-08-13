import pygame  # Импорт библиотеки Pygame для работы с графикой и вводом
import sys     # Импорт модуля sys для работы с системными функциями
import random  # Импорт модуля random для генерации случайных чисел
import os      # Импорт модуля os для работы с файловой системой

# Инициализация Pygame
pygame.init()

# Параметры окна
width, height = 800, 500  # Ширина и высота окна
screen = pygame.display.set_mode((width, height))  # Создание окна с указанными параметрами
pygame.display.set_caption("Dino Game")  # Установка заголовка окна

# Загрузка статичного фона
static_background_image = pygame.image.load('background.jpg')  # Загрузка изображения статичного фона
static_background_image = pygame.transform.scale(static_background_image, (width, height))  # Масштабирование изображения под размер окна

# Загрузка движущегося фона
moving_background_image = pygame.image.load('earth.png')  # Загрузка изображения движущегося фона
moving_background_image = pygame.transform.scale(moving_background_image, (width, height // 16))  # Масштабирование изображения под размер окна

background_x1 = 0  # Начальная позиция первого фрагмента движущегося фона
background_x2 = width  # Начальная позиция второго фрагмента движущегося фона
background_speed = 7  # Скорость движения фона

# Загрузка изображений динозаврика для анимации
dino_images = [
    pygame.image.load('monstr-1.png'),  # Загрузка первого изображения динозаврика
    pygame.image.load('monstr.png')      # Загрузка второго изображения динозаврика
]
dino_images = [pygame.transform.scale(img, (80, 110)) for img in dino_images]  # Масштабирование изображений динозаврика

dino_width, dino_height = dino_images[0].get_size()  # Получение размеров изображения динозаврика
dino_x = 50  # Начальная позиция динозаврика по X
dino_y = height - dino_height - 10  # Начальная позиция динозаврика по Y
dino_y_velocity = 0  # Начальная вертикальная скорость динозаврика
is_jumping = False  # Флаг, указывающий, находится ли динозаврик в прыжке

# Переменные для анимации
animation_index = 0  # Индекс текущего изображения для анимации
animation_speed = 0.1  # Скорость анимации
animation_timer = 0  # Таймер для управления анимацией

# Загрузка всех изображений кактусов
cactus_images = []  # Список для хранения изображений кактусов
cactus_dir = 'ship'  # Папка с изображениями кактусов
for filename in os.listdir(cactus_dir):  # Проходим по всем файлам в папке
    if filename.endswith('.png'):  # Проверяем, что файл имеет расширение .png
        image = pygame.image.load(os.path.join(cactus_dir, filename))  # Загрузка изображения кактуса
        image = pygame.transform.scale(image, (70, 100))  # Масштабирование изображения
        cactus_images.append(image)  # Добавляем изображение кактуса в список

# Параметры кактусов
cactus_speed = 5  # Начальная скорость движения кактусов
cactus_spawn_time = pygame.time.get_ticks()  # Время последнего появления кактуса
cactus_interval = random.randint(1000, 3000)  # Интервал между появлением кактусов (1-3 секунды)
cactus_list = []  # Список для хранения кактусов

# Счетчик
score = 0  # Начальный счет

# Функция для отображения текста на экране
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)  # Создание текстового объекта
    textrect = textobj.get_rect()  # Получение прямоугольника для текста
    textrect.center = (x, y)  # Установка центра прямоугольника в заданные координаты
    surface.blit(textobj, textrect)  # Отображение текста на экране

# Функция для рисования обводки вокруг изображения
def draw_border(image, x, y, color=(255, 0, 0), thickness=2):
    rect = image.get_rect()  # Получение прямоугольника для изображения
    rect.topleft = (x, y)  # Установка верхнего левого угла прямоугольника в заданные координаты
    pygame.draw.rect(screen, color, rect, thickness)  # Рисование обводки вокруг изображения

# Основной игровой цикл
def game_loop():
    global background_x1, background_x2
    global cactus_speed, score, is_jumping, dino_y_velocity, dino_y, dino_x
    global cactus_spawn_time, cactus_interval, cactus_list, animation_index, animation_timer

    clock = pygame.time.Clock()  # Создание объекта Clock для управления FPS
    running = True  # Флаг для управления циклом

    # Инициализация переменных
    cactus_list = []  # Сброс списка кактусов
    cactus_speed = 7  # Начальная скорость кактусов
    score = 0  # Сброс счета

    while running:
        # Обновление позиции движущегося фона
        background_x1 -= background_speed  # Двигаем первый фрагмент фона
        background_x2 -= background_speed  # Двигаем второй фрагмент фона

        # Перемещение фрагментов фона, когда они выходят за экран
        if background_x1 <= -width:
            background_x1 = width
        if background_x2 <= -width:
            background_x2 = width

        # Отображение фонов
        screen.blit(static_background_image, (0, 0))  # Отображение статичного фона
        screen.blit(moving_background_image, (background_x1, height - moving_background_image.get_height()))  # Отображение первого фрагмента движущегося фона
        screen.blit(moving_background_image, (background_x2, height - moving_background_image.get_height()))  # Отображение второго фрагмента движущегося фона

        for event in pygame.event.get():  # Обработка всех событий
            if event.type == pygame.QUIT:  # Если закрыть окно
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # Если нажата клавиша
                if event.key == pygame.K_SPACE and not is_jumping:  # Если пробел и не прыгаем
                    is_jumping = True  # Устанавливаем флаг прыжка
                    dino_y_velocity = -20  # Устанавливаем начальную скорость прыжка
        
        # Физика прыжка
        if is_jumping:
            dino_y += dino_y_velocity  # Обновляем позицию динозаврика
            dino_y_velocity += 1  # Увеличиваем скорость по мере прыжка
            if dino_y >= height - dino_height - 10:  # Если динозаврик приземляется
                dino_y = height - dino_height - 10  # Устанавливаем позицию на земле
                is_jumping = False  # Сбрасываем флаг прыжка
        
        # Анимация динозаврика
        animation_timer += animation_speed  # Обновляем таймер анимации
        if animation_timer >= 1:  # Если таймер достиг нужного значения
            animation_timer = 0  # Сбрасываем таймер
            animation_index = (animation_index + 1) % len(dino_images)  # Переключаем изображение для анимации
        
        # Обновление времени и проверка появления новых кактусов
        current_time = pygame.time.get_ticks()  # Получение текущего времени
        if current_time - cactus_spawn_time > cactus_interval:  # Если время прошло
            cactus_x = width  # Начальная позиция кактуса по X
            cactus_y = height - cactus_images[0].get_height() - 10  # Начальная позиция кактуса по Y
            cactus_image = random.choice(cactus_images)  # Выбор случайного изображения кактуса
            cactus_list.append([cactus_x, cactus_y, cactus_image])  # Добавляем новый кактус в список
            cactus_interval = random.randint(1000, 3000)  # Рандомное время до следующего кактуса
            cactus_spawn_time = current_time  # Обновляем время последнего появления кактуса
        
        # Обновление и рисование кактусов
        for cactus in cactus_list:
            cactus[0] -= cactus_speed  # Двигаем кактус влево
            if cactus[0] < -cactus[2].get_width():  # Если кактус ушел за левый край экрана
                cactus_list.remove(cactus)  # Удаляем кактус из списка
                score += 1  # Увеличиваем счет за удаленный кактус
        
        # Проверка на столкновение динозаврика с каждым кактусом
        for cactus in cactus_list:
            cactus_x, cactus_y, cactus_image = cactus
            if dino_x + dino_width > cactus_x and dino_x < cactus_x + cactus_image.get_width():  # Проверка по горизонтали
                if dino_y + dino_height >= cactus_y:  # Проверка по вертикали (нижняя часть динозаврика)
                    game_over_screen(score)  # Переход на экран "Game Over" при столкновении
                    return
        
        # Рисуем динозаврика и кактусы
        screen.blit(dino_images[animation_index], (dino_x, dino_y))  # Отображение динозаврика с текущим изображением
        for cactus in cactus_list:
            screen.blit(cactus[2], (cactus[0], cactus[1]))  # Отображение каждого кактуса
        
        # Отображение счета
        draw_text(f'Score: {score}', pygame.font.Font(None, 36), (0, 0, 0), screen, width // 2, 20)  # Отображение текста счета
        
        # Обновляем экран
        pygame.display.flip()  # Обновление экрана
        
        # Ограничение FPS
        clock.tick(60)  # Установка частоты обновления экрана в 60 кадров в секунду

# Экран Game Over
def game_over_screen(final_score):
    global cactus_speed, dino_y, dino_y_velocity, is_jumping, animation_index, animation_timer
    
    while True:
        # Отображение фонов
        screen.blit(static_background_image, (0, 0))  # Отображение статичного фона
        draw_text('Game Over', pygame.font.Font(None, 72), (255, 0, 0), screen, width // 2, height // 3)  # Отображение текста "Game Over"
        draw_text(f'Final Score: {final_score}', pygame.font.Font(None, 36), (0, 0, 0), screen, width // 2, height // 2)  # Отображение финального счета
        draw_text('Press Space to Restart', pygame.font.Font(None, 36), (0, 0, 0), screen, width // 2, height // 1.5)  # Инструкция для перезапуска игры
        
        pygame.display.flip()  # Обновление экрана
        
        for event in pygame.event.get():  # Обработка всех событий
            if event.type == pygame.QUIT:  # Если закрыть окно
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # Если нажата клавиша
                if event.key == pygame.K_SPACE:  # Если нажата клавиша пробел
                    # Сброс параметров игры
                    cactus_speed = 5  # Сброс скорости кактусов
                    dino_y = height - dino_height - 10  # Сброс позиции динозаврика
                    dino_y_velocity = 0  # Сброс вертикальной скорости динозаврика
                    is_jumping = False  # Сброс флага прыжка
                    animation_index = 0  # Сброс индекса анимации
                    animation_timer = 0  # Сброс таймера анимации
                    global cactus_spawn_time, cactus_interval, cactus_list
                    cactus_spawn_time = pygame.time.get_ticks()  # Обновление времени последнего появления кактуса
                    cactus_interval = random.randint(1000, 3000)  # Рандомный интервал до следующего кактуса
                    cactus_list = []  # Сброс списка кактусов
                    game_loop()  # Перезапуск игрового цикла
                    return

# Запуск игры
game_loop()  # Запуск основного игрового цикла
