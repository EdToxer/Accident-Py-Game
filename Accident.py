from re import I
import pygame
import time
import random
import pygame.locals
import sys

pygame.init()

#Values of the screen
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Accident")
#Colors
black = (0,0,0)
green = (0, 200, 0)
red = (200, 0, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

pause = False
#Game Icon
gameIcon = pygame.image.load('Assests\\Icon.png')
pygame.display.set_icon(gameIcon)
#Music
pygame.mixer.music.load("Assests\\Sound\\Smashing_Windshields_v2.ogg", "ogg")
pygame.mixer.music.set_volume(0.1)
#Sounds
death_sound = pygame.mixer.Sound("Assests\\Sound\\death.wav")
super_sound = pygame.mixer.Sound("Assests\\Sound\\super.mp3")
sandvich_sound = pygame.mixer.Sound("Assests\\Sound\\sandvich.wav")
#Player value
player_width = 70
#Loading a lot of sprites
BuilderHealthyL = [0 for i in range(4)]
BuilderHealthyR = [0 for i in range(4)]
BuilderDamagedL = [0 for i in range(4)]
BuilderDamagedR = [0 for i in range(4)]
BuilderDangerL = [0 for i in range(4)]
BuilderDangerR = [0 for i in range(4)]

for i in range(1,4):
    BuilderHealthyL[i] = pygame.image.load(f"Assests\\Builder\\healthy_anim\\healthyL0{i}.png")
    BuilderDamagedL[i] = pygame.image.load(f"Assests\\Builder\\damaged_anim\\damagedL0{i}.png")
    BuilderDangerL[i] = pygame.image.load(f"Assests\\Builder\\danger_anim\\dangerL0{i}.png")

    BuilderHealthyR[i] = pygame.image.load(f"Assests\\Builder\\healthy_anim\\healthyR0{i}.png")
    BuilderDamagedR[i] = pygame.image.load(f"Assests\\Builder\\damaged_anim\\damagedR0{i}.png")
    BuilderDangerR[i] = pygame.image.load(f"Assests\\Builder\\danger_anim\\dangerR0{i}.png")

#Other Sprites
brickWall = pygame.image.load("Assests\\Obstacles\\Brickwall.png")
constructionSite = pygame.image.load("Assests\\Background\\ConstructionSite.png")
sandvich = pygame.image.load("Assests\\Obstacles\\Sandvich.png")
metal = pygame.image.load("Assests\\Obstacles\\Metal.png")
super = pygame.image.load("Assests\\power_up.png")
#Tracks time in game, usually needed for FPS
clock = pygame.time.Clock()

#Functions to draw obstacles
def things(x, y):
    gameDisplay.blit(brickWall, (x,y))

def things1(x, y):
    gameDisplay.blit(metal, (x,y))

def things2(x, y):
    gameDisplay.blit(sandvich, (x,y))
#Draws builder in different sprites depending on a health state
def builder(x,y,lives,timer, cur_direction):
    timer -= 1
    if timer > 40: builder_draw(1,lives, x,y, cur_direction)
    elif timer < 41 and timer > 20: builder_draw(2,lives, x,y,cur_direction)
    elif timer < 21: builder_draw(3,lives, x,y,cur_direction)
    if timer == 0: return 60
    return timer
def builder_draw(i,lives, x,y, cur_direction):
    set_lives = ["Dead","Danger","Damaged","Healthy"]
    funct = (f"Builder{set_lives[lives]}{cur_direction}[{i}]")
    gameDisplay.blit(eval(funct), (x,y))
#Food to gain health
def power_up():
    global lives
    if lives < 3:
        lives += 1
        pygame.mixer.Sound.play(sandvich_sound)
#Function to draw text
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(2)
    game_loop()

def game_quit():
    pygame.quit()
    sys.exit()

def unpause():
    pygame.mixer.music.unpause()
    global pause
    pause = False
#Time to dodge after being hit
def invincible_time(x):
    global invincible
    global invincible_timer
    if invincible == True:
        if invincible_timer == 99:
            pygame.mixer.Sound.play(super_sound)
        gameDisplay.blit(super, (x-5,470))
        
        invincible_timer -= 1
        if invincible_timer == 0: 
            invincible = False
            invincible_timer = 100
#Kills
def death():
    global invincible
    global lives
    if invincible != True and lives != 1:
        lives -= 1
        invincible = True
    if invincible == False and lives == 1:
        pygame.mixer.music.stop()
        pygame.mixer.Sound.stop(super_sound)
        pygame.mixer.Sound.stop(sandvich_sound)
        pygame.mixer.Sound.play(death_sound)
        message_display("You Died")
#Detects whether something hit you
def hit_detect(x,y,player_width ,thing_height, thing_width, things_startsx, things_startsy):
    if y < things_startsy+thing_height:
                if x > things_startsx and x < things_startsx + thing_width or x+player_width > things_startsx and x + player_width < things_startsx + thing_width:
                    death()
#Detects if sandvich hits you
def power_detect(x,y,player_width ,thing_height, thing_width, things_startsx, things_startsy):
    if y < things_startsy+thing_height:
                if x > things_startsx and x < things_startsx + thing_width or x+player_width > things_startsx and x + player_width < things_startsx + thing_width:
                    power_up()
                    return int(-600), random.randrange(50, display_width - 50)
    return things_startsy, things_startsx
#Counts how many obstacles you've doged during the game
def counter(count):
    largeText = pygame.font.SysFont("comicsansms",25)
    TextSurf, TextRect = text_objects("Уклонено:"+str(count), largeText)
    TextRect.center = ((100),(100))
    gameDisplay.blit(TextSurf, TextRect)
#Function for buttons
def button(msg, x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x + w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == True and action != None:
            action()

    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))
    
    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = ( (x+(w/2), (y+(h/2))))
    gameDisplay.blit(textSurf, TextRect)
#Before main loop
def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
        gameDisplay.blit(constructionSite, (0,0))
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("Accident", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        button("Go!", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, game_quit)
        pygame.display.update()
        clock.tick(15)

def paused():
    pygame.mixer.music.pause()
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("Paused", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        button("Resume", 150, 450, 200, 50, green, bright_green, unpause)
        button("Quit", 550, 450, 100, 50, red, bright_red, game_quit)
        pygame.display.update()
        clock.tick(15)

def game_loop():
    global pause
    pygame.mixer.music.play(-1)
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    thing_width = 100
    thing_height = 100
    things_startsx = random.randrange(50, display_width - 50)
    things_startsx1 = random.randrange(50, display_width - 50)
    things_startsx2 = random.randrange(50, display_width - 50)
    things_startsy = -600
    things_startsy1 = -600
    things_startsy2 = -600
    things_speed = 7
    last_direction = 1
    cur_direction = "R"
    global invincible_timer
    invincible_timer = 100
    global invincible
    invincible = False
    count = 0
    timer = 20
    global lives
    lives = 1
    x_changeR = 0
    x_changeL = 0
    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit == True
                game_quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    x_changeR = 0
                    if x_changeL < -5:
                        x_changeL = -5
                if event.key == pygame.K_LEFT:
                    x_changeL = 0
                    if x_changeR > 5:
                        x_changeR = 5
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_changeL = -5
                if event.key == pygame.K_RIGHT:
                    x_changeR = 5
                if event.key == pygame.K_LEFT and x_changeR != 0:
                    x_changeL = -10
                    x_changeR = 5
                if event.key == pygame.K_RIGHT and x_changeL != 0:
                    x_changeL = -5
                    x_changeR = 10
                if event.key == pygame.K_p:
                    pause = True
                    paused()
        movement = x_changeL + x_changeR
        x += movement
        gameDisplay.blit(constructionSite, (0,0))

        counter(count)
        things(things_startsx, things_startsy)
        things_startsy += things_speed

        if things_startsy > display_height:
            things_startsy = 0 - thing_height
            things_startsx = random.randrange(50, display_width - 50)
            count += 1
        if things_startsy1 > display_height:
            things_startsy1 = 0 - thing_height
            things_startsx1 = random.randrange(50, display_width - 50)
            count += 1
        
        if count > 2:
            things_speed = 10
            thing_width = 100
            things1(things_startsx1, things_startsy1)
            things_startsy1 += things_speed

        if lives < 3:
            things2(things_startsx2, things_startsy2)
            things_startsy2,things_startsx2 = power_detect(x,y,player_width ,thing_height, thing_width, things_startsx2, things_startsy2)
            things_startsy2 += things_speed
            if things_startsy2 > display_height:
                things_startsy2 = 0 - thing_height
                things_startsx2 = random.randrange(50, display_width - 50)

        invincible_time(x)
        if movement != 0: last_direction = movement
        if movement < 0: cur_direction = "L"
        elif movement > 0: cur_direction = "R"
        elif last_direction > 0: cur_direction = "R"
        elif last_direction < 0: cur_direction = "L"
        else: cur_direction = "R"
        timer = builder(x,y,lives, timer, cur_direction)
        
        if x > display_width - player_width or x < 0:
            invincible = False
            death()        
        hit_detect(x,y,player_width ,thing_height, thing_width, things_startsx, things_startsy)
        hit_detect(x,y,player_width ,thing_height, thing_width, things_startsx1, things_startsy1)
        
        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
sys.exit()