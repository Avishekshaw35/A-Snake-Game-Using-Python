import pygame
import random
import os

pygame.mixer.init()
x = pygame.init()

#colors
white = (230,230,230)
black = (0,0,0)
red = (255,0,0)
br = (200,0,200)
blue = (0,0,255)
new = (230,180,200)
#creating window
s_width = 900
s_height = 500
gamewindow = pygame.display.set_mode((s_width,s_height))
#Back groungd image
backimg = pygame.image.load('background.jpg')
backimg = pygame.transform.scale(backimg, (s_width,s_height)).convert_alpha()
#Welcome image
w_game = pygame.image.load('welcome.jpg')
w_game = pygame.transform.scale(w_game, (s_width,s_height)).convert_alpha()
#Game over image
g_over = pygame.image.load('last.jpg')
g_over = pygame.transform.scale(g_over, (s_width,s_height)).convert_alpha()
#game title
pygame.display.set_caption("SnakeAlim")
pygame.display.update()
clock = pygame.time.Clock()
#screen project
font = pygame.font.SysFont(None,55)
#Score to the screen
def text_screen(text,color=blue,x=5,y=5):
    text = font.render(text,True,color)
    gamewindow.blit(text,(x,y))
# Snake plot
def plot_snake(gamewindow,color,body,size):
    for x,y in body:
        pygame.draw.rect(gamewindow,color,[x,y,size,size])
#welcome screen
def welcome():
    exit_game = False
    while not exit_game:
        gamewindow.blit(w_game,(0,0))
        text_screen("--| Welcome to snakes |--",br,200,100)
        text_screen("Press Space bar to play ...",br,200,140)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # pygame.mixer.music.load("eating.mp3")
                    # pygame.mixer.music.play()
                    gameloop()
        pygame.display.update()
        clock.tick(60)
#game loop
def gameloop():
    #game specific variable
    #checking the file
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt","w") as f:
            f.write("0")
    
    with open("highscore.txt","r") as f:
        highscore = f.read()
    
    # pygame.mixer.music.load("back.mp3")
    # pygame.mixer.music.play()
    exit_game = False
    game_over = False
    game_quit = False
    eat_itself = False
    snake_x = 45
    snake_y = 100
    size = 10
    velocity_x = 0
    velocity_y =0
    food_x = random.randint(15,(s_width-15))
    food_y = random.randint(15,(s_height-15))
    speed = 5
    score = 0
    fps = 30
    snake_length = 1
    snake_body = list()
    #while loop
    while not exit_game:
        if game_over:
            with open("highscore.txt","w") as f:
                f.write(highscore)
            gamewindow.blit(g_over,(0,0))
            text_screen("Your Score: "+str(score), br, 10, 5)
            if eat_itself:
                text_screen("Eaten itself Game Over!",red,(s_width/2)-230,(s_height/2)-80)
            else:
                text_screen("Out of Screen Game Over!",red,(s_width/2)-230,(s_height/2)-80)
            text_screen("Press Enter to Continue ...",red,(s_width/2)-230,(s_height/2)-20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # pygame.mixer.music.load("eating.mp3")
                        # pygame.mixer.music.play()
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:  #if any key is pressed
                    if event.key == pygame.K_RIGHT:  #if the pressed key is right key(+ve)
                        velocity_x = speed
                        velocity_y = 0
                    elif event.key == pygame.K_LEFT:  #if the pressed key is left key(-ve)
                        velocity_x = - speed
                        velocity_y = 0
                    elif event.key == pygame.K_UP:  #if the pressed key is up key(-ve)
                        velocity_y = -speed
                        velocity_x = 0
                    elif event.key == pygame.K_DOWN:  #if the pressed key is right key(+ve)
                        velocity_y = speed
                        velocity_x = 0
                    elif event.key == pygame.K_b:
                        score += 50
            gamewindow.fill(white) #filling the window
            gamewindow.blit(backimg,(0,0))
            snake_x = (snake_x + velocity_x)%s_width #setting velocity_x
            snake_y = (snake_y + velocity_y)%s_height #setting velocity_y 
            if abs(snake_x - food_x)<size and abs(snake_y - food_y)<size: # eating food
                pygame.mixer.music.load('eating.mp3')
                pygame.mixer.music.play()
                score += 10
                food_x = random.randint(15,(s_width-15))
                food_y = random.randint(60,(s_height-15))
                snake_length += 5
            if score>int(highscore):
                    highscore = str(score)
            text_screen("Score: "+str(score)+"  Highscore: "+highscore, br, 10, 5)
            #pygame.draw.rect(gamewindow,black,[snake_x,snake_y,size,size]) # SNAKE
            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snake_body.append(head)
            if len(snake_body) > snake_length:
                del snake_body[0]
            if head in snake_body[:-1]: #game Over
                game_over = True
                eat_itself = True
                pygame.mixer.music.load("lose.wav")
                pygame.mixer.music.play()
            if snake_x<0 or snake_x>s_width or snake_y<0 or snake_y>s_height: #game over
                game_over = True
                pygame.mixer.music.load("lose.wav")
                pygame.mixer.music.play()
            plot_snake(gamewindow,black,snake_body,size) #Snake plotting
            pygame.draw.rect(gamewindow,red,[food_x,food_y,size,size]) # FOOD
        pygame.display.update() #update the game window
        clock.tick(fps)
    pygame.quit()
    quit()

welcome()
