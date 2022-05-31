import pygame
import random
import numpy as np

sqr_len:    int = 20
max_tiles:  int = 625

def main():
    def generatePos() -> int:
        min:        int = 1
        max:        int = 499
        rd:         int = random.randint(min, max)
        while rd % sqr_len != 0:
            rd = random.randint(min, max)
        return rd

    pygame.init()
    window_title:   str = 'Snake'
    window_width:   int = 500
    window_height:  int = 500
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption(window_title)

    def messageToScreen(size: int, msg: str, color: tuple, x: int, y: int, removeBorder: bool, ft: str | None = None) -> None:
        font = pygame.font.SysFont(ft, size)
        txt = font.render(msg, True, color)
        if removeBorder:
            window.blit(txt, (x - txt.get_rect().width / 2, y - txt.get_rect().height))
        else:
            window.blit(txt, (x, y))
        pygame.display.update()

    def messagePop(size: int, msg: str, color1: tuple, color2: tuple, x: int, y: int, removeBorder: bool, ft: str | None = None) -> None:
        font = pygame.font.SysFont(ft, size)
        render_iterations: int = 6
        delay: int = 250
        for i in range(render_iterations):
            if i % 2 == 0:
                txt = font.render(msg, True, color1)
            else:
                txt = font.render(msg, True, color2)
            if removeBorder:
                window.blit(txt, (x - txt.get_rect().width / 2, y - txt.get_rect().height))
            else:
                window.blit(txt, (x, y))
            pygame.display.update()
            pygame.time.delay(delay)
        
    class Snake:
        def __init__(self, x: int, y: int, height: int, width: int):
            self.x = x
            self.y = y
            self.height = height
            self.width = width

    snake = Snake(window_width/2+10, window_height/2+10, 20, 20)
    run, go_up, go_down, go_left, go_right, init, gameover = True, True, False, False, False, True, False
    i, snake_size, frame_size = 0, 0, 20
    backtrack = np.array([snake.x, snake.y])
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        lastPosX = snake.x
        lastPosY = snake.y
        oldPos = np.array([lastPosX,lastPosY])
        if go_up:
            if snake.y - frame_size < 0:
                snake.y = window_height - (snake.y + frame_size)
            else:
                snake.y = lastPosY - frame_size
        elif go_down:
            if snake.y + frame_size >= window_height:
                snake.y = snake.y - window_height + frame_size
            else:
                snake.y = lastPosY + frame_size
        elif go_right:
            if snake.x + frame_size >= window_width:
                snake.x = snake.x - window_width + frame_size
            else:
                snake.x = lastPosX + frame_size
        elif go_left:
            if snake.x - frame_size < 0:
                snake.x = window_width - (snake.x + frame_size)
            else:
                snake.x = lastPosX - frame_size
        keys = pygame.key.get_pressed()      
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if not go_left:
                go_right, go_down, go_left, go_up = True, False, False, False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if not go_right:
                go_right, go_down, go_left, go_up = False, False, True, False
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if not go_down:
                go_right, go_down, go_left, go_up = False, False, False, True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if not go_up:
                go_right, go_down, go_left, go_up = False, True, False, False
        backtrack = np.vstack((backtrack, oldPos))
        i += 1
        black:      tuple = (0, 0, 0)
        gray:       tuple = (210, 210, 210)
        reddish:    tuple = (250, 128, 114)
        greenish:   tuple = (0, 255, 0)
        white:      tuple = (255, 255, 255)
        yellow:     tuple = (255, 255, 0)
        blueish:    tuple = (30, 144, 255)
        window.fill(gray)
        score = "Score: " + str(snake_size + 1)
        message_size:           int     = 50
        width_to_screen_factor: float   = 2 / 3
        messageToScreen(message_size, score, black, window_width * width_to_screen_factor, 0, False)
        if init:
            msg = 0
            appleX = generatePos()
            appleY = generatePos()
            while appleX == snake.x and appleY == snake.y:
                appleX = generatePos()
                appleY = generatePos()
            pygame.draw.rect(window, reddish, (appleX, appleY, sqr_len, sqr_len))
            pygame.draw.rect(window, greenish, (snake.x, snake.y, snake.width, snake.height))
            init = False
        else:
            pygame.draw.rect(window, yellow, (snake.x, snake.y, snake.width, snake.height))
            lvl_1_ceil: int = 5
            lvl_1_inc:  int = 1
            lvl_2_ceil: int = 20
            lvl_2_inc:  int = 2
            lvl_3_ceil: int = 50
            lvl_3_inc:  int = 3
            lvl_4_ceil: int = 100
            lvl_4_inc:  int = 4
            lvl_5_ceil: int = 200
            lvl_5_inc:  int = 5
            lvl_6_ceil: int = 400
            lvl_6_inc:  int = 6
            lvl_7_inc:  int = 7
            if appleX == snake.x and appleY == snake.y:
                if snake_size >= 0 and snake_size < lvl_1_ceil:
                    snake_size = snake_size + lvl_1_inc
                elif snake_size >= lvl_1_ceil and snake_size < lvl_2_ceil:
                    snake_size = snake_size + lvl_2_inc
                    if msg == 0:
                        msg += 1
                        print("Leveled up! Snake is now hungrier.")
                        messagePop(message_size, "Level 2 - Hungry", blueish, white, window_width / 2, window_height / 2, True)
                elif snake_size >= lvl_2_ceil and snake_size < lvl_3_ceil:
                    snake_size = snake_size + lvl_3_inc
                    if msg == 1:
                        msg += 1
                        print("Leveled up! Snake is now chubby.")
                        messagePop(message_size, "Level 3 - Chubby", blueish, white, window_width / 2, window_height / 2, True)
                elif snake_size >= lvl_3_ceil and snake_size < lvl_4_ceil:
                    snake_size = snake_size + lvl_4_inc
                    if msg == 2:
                        msg += 1
                        print("Leveled up! Snake is now fattier.")
                        messagePop(message_size, "Level 4 - Fat", blueish, white, window_width / 2, window_height / 2, True)
                                        
                elif snake_size >= lvl_4_ceil and snake_size < lvl_5_ceil:
                    snake_size = snake_size + lvl_5_inc
                    if msg == 3:
                        msg += 1
                        print("Leveled up! Snake is now overweight.")
                        messagePop(message_size, "Level 5 - Overweight", blueish, white, window_width / 2, window_height / 2, True)
                        
                elif snake_size > lvl_5_ceil and snake_size <= lvl_6_ceil:
                    snake_size = snake_size + lvl_6_inc
                    if msg == 4:
                        msg += 1
                        print("Leveled up! Snake is now obese.")
                        messagePop(message_size, "Level 6 - Obese", blueish, white, window_width / 2, window_height / 2, True)
                        
                elif snake_size >= lvl_6_ceil:
                    snake_size = snake_size + lvl_7_inc
                    if msg == 5:
                        msg += 1
                        print("Leveled up! Snake is now a real chonker. If he eats more, he dies.")
                        messagePop(message_size, "Level MAX - Chonker", blueish, white, window_width / 2, window_height / 2, True)
                appleX = generatePos()
                appleY = generatePos()
                allSnakeXPos = np.array([snake.x])
                allSnakeYPos = np.array([snake.y])
                for z in range(snake_size):
                    allSnakeXPos = np.append(allSnakeXPos, backtrack[i - z][0])
                    allSnakeYPos = np.append(allSnakeYPos, backtrack[i - z][1])
                verifyApplePos: bool    = False
                countError:     int     = 0
                appleX = generatePos()
                appleY = generatePos()
                while verifyApplePos == False:
                    for l in range(len(allSnakeXPos)):
                        if appleX == allSnakeXPos[l] and appleY == allSnakeYPos[l]:
                            countError = countError + 1
                    if countError == 0:
                        percent_factor: int = 100
                        precision:      int = 1
                        print("Apple eaten! Current score: ", snake_size + 1," / 625 (", round((snake_size + 1) / max_tiles * percent_factor, precision)," %)")
                        verifyApplePos = True
                        break
                    else:
                        countError = 0
                        print("The apple was rotten!")
                        appleX = generatePos()
                        appleY = generatePos()
            pygame.draw.rect(window, reddish, (appleX, appleY, sqr_len, sqr_len))
            if snake_size >= 1:
                for z in range(snake_size):
                    oldX = backtrack[i-z][0]
                    oldY = backtrack[i-z][1]
                    backtrack_color: tuple = (50, 205, 50)
                    pygame.draw.rect(window, backtrack_color, (oldX, oldY, snake.width, snake.height))
            allSnakeXPos = np.array([snake.x])
            allSnakeYPos = np.array([snake.y])
            for z in range(snake_size):
                allSnakeXPos = np.append(allSnakeXPos, backtrack[i - z][0])
                allSnakeYPos = np.append(allSnakeYPos, backtrack[i - z][1])
            count = 0
            for k in range(len(allSnakeXPos)):
                if snake.x == allSnakeXPos[k] and snake.y == allSnakeYPos[k]:
                    count += 1
            if (count > 1):
                print("Game over, your score is: ", snake_size + 1," / 625 (", round((snake_size + 1) / max_tiles * percent_factor, precision)," %)")
                gameover = True
                run = False
        if snake_size >= max_tiles:
            print("You won!")
            won = True
            if won:
                winning_color:          tuple   = (0, 128, 0)
                winning_screen_size:    int     = 50
                window_offset:          int     = 30
                messageToScreen(winning_screen_size, "Congratulations, you've won!", winning_color, window_width / 2, window_height / 2, True)
                messageToScreen(30, "Press ESC to play again", black, 0, window_height - window_offset, False)
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_ESCAPE]:
                        main()
            else: 
                pygame.quit()
                quit()
        pygame.display.update()
        initDelay: int = 400
        first_level_delay_factor:   float = 4
        second_level_delay_factor:  float = 4.75
        third_level_delay_factor:   float = 5.25
        fourth_level_delay_factor:  float = 6
        fifth_level_delay_factor:   float = 6.75
        sixth_level_delay_factor:   float = 7.5
        seventh_level_delay_factor: float = 8.25
        if msg == 0:
            delay = round(initDelay / first_level_delay_factor, 0)
        elif msg == 1:
            delay = round(initDelay / second_level_delay_factor, 0)
        elif msg == 2:
            delay = round(initDelay / third_level_delay_factor, 0)
        elif msg == 3:
            delay = round(initDelay / fourth_level_delay_factor, 0)
        elif msg == 4:
            delay = round(initDelay / fifth_level_delay_factor, 0)
        elif msg == 5:
            delay = round(initDelay / sixth_level_delay_factor, 0)
        else:
            delay = round(initDelay / seventh_level_delay_factor, 0)
        pygame.time.delay(int(delay))
    if gameover:
        game_over_color: tuple = (178, 34, 34)
        messageToScreen(window_offset, "Game over :(", game_over_color, window_width / 2, window_height / 2, True)
        messageToScreen(30, "Press ESC to Restart", black, 0, window_height - window_offset, False)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                main()
    else: 
        pygame.quit()
        quit()
main()
