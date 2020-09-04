import pygame
import random
import numpy as np

def main():
    def generatePos():
        rd = random.randint(1,499)
        while rd % 20 != 0:
            rd = random.randint(1,499)
            if (rd % 20) == 0:
                break
        return rd

    pygame.init()

    windowWidth = 500
    windowHeight = 500

    window = pygame.display.set_mode((windowWidth,windowHeight))

    pygame.display.set_caption("Snake")

    def messageToScreen(size, msg, color, x, y, removeBorder, ft = None):
        font = pygame.font.SysFont(ft, size)
        txt = font.render(msg, True, color)
        if removeBorder:
            window.blit(txt, (x-txt.get_rect().width/2,y-txt.get_rect().height))
        else:
            window.blit(txt, (x,y))
        pygame.display.update()

    def messagePop(size, msg, color1, color2, x, y, removeBorder, ft = None):
        font = pygame.font.SysFont(ft, size)
        for i in range(6):
            if i % 2 == 0:
                txt = font.render(msg, True, color1)
            else:
                txt = font.render(msg, True, color2)
            if removeBorder:
                window.blit(txt, (x-txt.get_rect().width/2,y-txt.get_rect().height))
            else:
                window.blit(txt, (x,y))
            pygame.display.update()
            pygame.time.delay(250)
        
    class Object:
        def __init__(self, x, y, height, width):
            self.x = x
            self.y = y
            self.height = height
            self.width = width

    # init snake
    snake = Object(windowWidth/2+10, windowHeight/2+10, 20, 20)

    run = True
    initialize = True
    goUP = True #Snake goes up initially
    goDOWN = False
    goLEFT = False
    goRIGHT = False

    backtrack = np.array([snake.x, snake.y])
    i = 0
    init = True
    gameover = False
    snakeSize = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        lastPosX = snake.x
        lastPosY = snake.y
        
        oldPos = np.array([lastPosX,lastPosY])
        
        if goUP:
            if snake.y - 20 < 0:
                snake.y = windowHeight - (snake.y + 20)
            else:
                snake.y = lastPosY - 20
                
        elif goDOWN:
            if snake.y + 20 >= windowHeight:
                snake.y = snake.y - windowHeight + 20
            else:
                snake.y = lastPosY + 20
        
        elif goRIGHT:
            if snake.x + 20 >= windowWidth:
                snake.x = snake.x - windowWidth + 20
            else:
                snake.x = lastPosX + 20
        
        elif goLEFT:
            if snake.x - 20 < 0:
                snake.x = windowWidth - (snake.x + 20)
            else:
                snake.x = lastPosX - 20
        
        keys = pygame.key.get_pressed()
                            
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if goLEFT == False:
                goRIGHT = True
                goDOWN = False
                goLEFT = False
                goUP = False
            
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if goRIGHT == False:
                goRIGHT = False
                goDOWN = False
                goLEFT = True
                goUP = False
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if goDOWN == False:
                goRIGHT = False
                goDOWN = False
                goLEFT = False
                goUP = True
        
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if goUP == False:
                goRIGHT = False
                goDOWN = True
                goLEFT = False
                goUP = False
                
        #backtrack old position to enlargen the snake and gray rect unused space
            
        backtrack = np.vstack((backtrack, oldPos))
       
        i = i + 1
        
        #debug: print(i, backtrack)
        
        window.fill((210,210,210))
        
        score = "Score: " + str(snakeSize+1)
        #print(score)
        messageToScreen(50, score, (0,0,0), windowWidth*2/3, 0, False)
        
        #generate apple
        
        if init:
            msg = 0
            appleX = generatePos()
            appleY = generatePos()
            
            while appleX == snake.x and appleY == snake.y: #snake and apples dont collide
                appleX = generatePos()
                appleY = generatePos()
            
            pygame.draw.rect(window, (250,128,114), (appleX, appleY, 20, 20))
            pygame.draw.rect(window, (0,255,0), (snake.x, snake.y, snake.width, snake.height))
            
            init = False
        
        else:
            pygame.draw.rect(window, (255,255,0), (snake.x, snake.y, snake.width, snake.height))
                        
            if appleX == snake.x and appleY == snake.y: #snake eats apple
                
                if snakeSize >= 0 and snakeSize < 5:
                    snakeSize = snakeSize + 1
                    
                elif snakeSize >= 5 and snakeSize < 20:
                    snakeSize = snakeSize + 2

                    if msg == 0:
                        msg = msg + 1
                        print("Leveled up! Snake is now hungrier.")
                        messagePop(50, "Level 2 - Hungry", (30,144,255), (255,255,255), windowWidth/2, windowHeight/2, True)
                        
                elif snakeSize >= 20 and snakeSize < 50:
                    snakeSize = snakeSize + 3
                    if msg == 1:
                        msg = msg + 1
                        print("Leveled up! Snake is now chubby.")
                        messagePop(50, "Level 3 - Chubby", (30,144,255), (255,255,255), windowWidth/2, windowHeight/2, True)
                        
                elif snakeSize >= 50 and snakeSize < 100:
                    snakeSize = snakeSize + 4
                    if msg == 2:
                        msg = msg + 1
                        print("Leveled up! Snake is now fattier.")
                        messagePop(50, "Level 4 - Fat", (30,144,255), (255,255,255), windowWidth/2, windowHeight/2, True)
                                        
                elif snakeSize >= 100 and snakeSize < 200:
                    snakeSize = snakeSize + 5
                    if msg == 3:
                        msg = msg + 1
                        print("Leveled up! Snake is now overweight.")
                        messagePop(50, "Level 5 - Overweight", (30,144,255), (255,255,255), windowWidth/2, windowHeight/2, True)
                        
                elif snakeSize > 200 and snakeSize <= 400:
                    snakeSize = snakeSize + 6
                    if msg == 4:
                        msg = msg + 1
                        print("Leveled up! Snake is now obese.")
                        messagePop(50, "Level 6 - Obese", (30,144,255), (255,255,255), windowWidth/2, windowHeight/2, True)
                        
                elif snakeSize >= 400:
                    snakeSize = snakeSize + 7
                    if msg == 5:
                        msg = msg + 1
                        print("Leveled up! Snake is now a real chonker. If he eats more, he dies.")
                        messagePop(50, "Level MAX - Chonker", (30,144,255), (255,255,255), windowWidth/2, windowHeight/2, True)
                        
                
                appleX = generatePos()
                appleY = generatePos()
                
                allSnakeXPos = np.array([snake.x])
                allSnakeYPos = np.array([snake.y])
                
                for z in range(snakeSize):
                    allSnakeXPos = np.append(allSnakeXPos, backtrack[i-z][0])
                    allSnakeYPos = np.append(allSnakeYPos, backtrack[i-z][1])
                
                verifyApplePos = False
                countError = 0
                
                appleX = generatePos()
                appleY = generatePos()
                
                while verifyApplePos == False:
                    for l in range(len(allSnakeXPos)):
                        if appleX == allSnakeXPos[l] and appleY == allSnakeYPos[l]:
                            countError = countError + 1
                    #print(i)
                    if countError == 0:
                        print("Apple eaten! Current score: ",snakeSize+1," / 625 (",round((snakeSize+1)/625*100,1)," %)")
                        verifyApplePos = True
                        break
                    else:
                        countError = 0
                        print("The apple was rotten!")
                        appleX = generatePos()
                        appleY = generatePos()
                #while appleX in allSnakeXPos and appleY in allSnakeYPos: #snake and apples dont collide
                    
                #print(appleX,appleY)
                #print(len(allSnakeXPos))
            pygame.draw.rect(window, (250,128,114), (appleX, appleY, 20, 20))
               
            if snakeSize >= 1:
                for z in range(snakeSize):
                    oldX = backtrack[i-z][0]
                    oldY = backtrack[i-z][1]
                    #print(oldX,oldY), older position
                    pygame.draw.rect(window, (50,205,50), (oldX, oldY, snake.width, snake.height))
                    
                
            #check if snake collapses with himself
            allSnakeXPos = np.array([snake.x])
            allSnakeYPos = np.array([snake.y])
                
            for z in range(snakeSize):
                allSnakeXPos = np.append(allSnakeXPos, backtrack[i-z][0])
                allSnakeYPos = np.append(allSnakeYPos, backtrack[i-z][1])
            
            count = 0
            
            for k in range(len(allSnakeXPos)):
                if snake.x == allSnakeXPos[k] and snake.y == allSnakeYPos[k]:
                    count = count + 1
                    
            if (count > 1):
                print("Game over, your score is: ",snakeSize+1," / 625 (",round((snakeSize+1)/625*100,1)," %)")
                gameover = True
                run = False
        
        if snakeSize >= 625:
            print("You won!")
            won = True
            if won:
                messageToScreen(50, "Congratulations, you've won!", (0,128,0), windowWidth/2, windowHeight/2, True)
                messageToScreen(30, "Press ESC to play again", (0,0,0), 0, windowHeight-30, False)
                
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
        
        initDelay = 400
        
        if msg == 0:
            delay = round(initDelay/4,0)
        elif msg == 1:
            delay = round(initDelay/4.75,0)
        elif msg == 2:
            delay = round(initDelay/5.25,0)
        elif msg == 3:
            delay = round(initDelay/6,0)
        elif msg == 4:
            delay = round(initDelay/6.75,0)
        elif msg == 5:
            delay = round(initDelay/7.5,0)
        else:
            delay = round(initDelay/8.25,0)
            
        pygame.time.delay(int(delay))

    if gameover:
        messageToScreen(50, "Game over :(", (178,34,34), windowWidth/2, windowHeight/2, True)
        messageToScreen(30, "Press ESC to Restart", (0,0,0), 0, windowHeight-30, False)
        
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