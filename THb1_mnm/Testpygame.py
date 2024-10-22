import pygame
import time
import random

pygame.init()

# Màu sắc
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
blue = (50, 153, 213)

# Kích thước màn hình
dis_width = 1300
dis_height = 750

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Pảnh Đâyyyyy')

clock = pygame.time.Clock()

# Kích thước và tốc độ rắn
snake_block_size = 27
snake_speed = 15

# Font chữ
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Âm thanh
eating_sound = pygame.mixer.Sound("ối dồi ôi.wav")
game_over_sound = pygame.mixer.Sound("kha-banh-ao-that-day.wav")

# Hình ảnh
snake_block_img = pygame.transform.scale(pygame.image.load("img_1.png").convert(), (snake_block_size, snake_block_size))
food_img = pygame.transform.scale(pygame.image.load("img.png").convert(), (snake_block_size, snake_block_size))


def Your_score(score):
    value = score_font.render("Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])


def our_snake(snake_block_size, snake_list):
    for x, y in snake_list:
        dis.blit(snake_block_img, [x, y])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    # Đảm bảo vị trí mồi được làm tròn ngay từ đầu
    foodx = round(random.randrange(0, dis_width - snake_block_size, snake_block_size))
    foody = round(random.randrange(0, dis_height - snake_block_size, snake_block_size))

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("Bạn đã thua! Chơi lại (C) hay Thoát (Q)?", yellow)
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block_size
                    x1_change = 0

        # Kiểm tra va chạm với biên
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_over_sound.play()
            game_close = True

        # Cập nhật vị trí đầu rắn
        x1 += x1_change
        y1 += y1_change

        # Làm tròn vị trí đầu rắn để đảm bảo khớp với lưới
        x1 = round(x1 / snake_block_size) * snake_block_size
        y1 = round(y1 / snake_block_size) * snake_block_size

        # Vẽ nền
        dis.fill(blue)

        # Vẽ mồi
        dis.blit(food_img, [foodx, foody])

        # Xử lý phần thân rắn
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)

        # Giữ độ dài rắn
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Kiểm tra va chạm với bản thân
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_over_sound.play()
                game_close = True

        # Vẽ rắn
        our_snake(snake_block_size, snake_List)

        # Hiển thị điểm
        Your_score(Length_of_snake - 1)

        # Cập nhật màn hình
        pygame.display.update()

        # Kiểm tra va chạm với mồi
        if x1 == foodx and y1 == foody:
            eating_sound.play()
            foodx = round(random.randrange(0, dis_width - snake_block_size, snake_block_size))
            foody = round(random.randrange(0, dis_height - snake_block_size, snake_block_size))
            Length_of_snake += 1

        # Điều chỉnh tốc độ
        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()