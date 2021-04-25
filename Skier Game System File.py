
# Skier program
import pygame, sys, random
from pathlib import Path
import json

# different images for the skier depending on his direction
skier_images = ["skier_down.png", "skier_right1.png", "skier_right2.png",
                 "skier_left2.png", "skier_left1.png"]


# Dit is een mooi commentaar..

# class for the Skier sprite
class SkierClass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("skier_down.png")
        self.rect = self.image.get_rect()
        self.rect.center = [320, 100]
        self.angle = 0
        
    def turn(self, direction): 
        # load new image and change speed when the skier turns
        self.angle = self.angle + direction
        reduce_speed = 0
        if self.angle < -2: self.angle = -2
        if self.angle >  2: self.angle =  2
        center = self.rect.center
        self.image = pygame.image.load(skier_images[self.angle])
        self.rect = self.image.get_rect()
        self.rect.center = center
        speed = [self.angle, 6 - abs(self.angle)]
        return speed
    
    def move(self, speed):
        # move the skier right and left De *
        self.rect.centerx = self.rect.centerx + (speed[0] * materiaal)
        if self.rect.centerx < 20:  self.rect.centerx = 20
        if self.rect.centerx > 620: self.rect.centerx = 620 


class LevensClass(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("life.png")
        self.rect = self.image.get_rect()
        self.rect.center = location



# class for obstacle sprites (trees and flags)
class ObstacleClass(pygame.sprite.Sprite):
    def __init__(self, image_file, location, type):
        pygame.sprite.Sprite.__init__(self) 
        self.image_file = image_file        
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = type
        self.passed = False
                   
    def update(self):
        global speed
        self.rect.centery -= speed[1]
        if self.rect.centery < -32:
            self.kill()



# create one "screen" of obstacles: 640 x 640
# use "blocks" of 64 x 64 pixels, so objects aren't too close together
def create_map(obstacles):
    locations = []

## def create_bonusses:
    life_draw = False
    skies_draw = False

    for i in range(random.randint(2, 4)): # Hoeveel punten objecten (vlaggen / levens / skies) per scherm
        row = random.randint(0, 9)
        col = random.randint(0, 9)
        # Max 5% kans op een levensvlaggetje, hoe meer levens je al hebt, des te minder kans
        if life_draw is not True and random.randint(0,100) < (max_levens - nrlevens): 
            type = "life"
            img = "skier_flag_bright.png"
            life_draw = True
            if debug_mode == True:
                col = 0
        # Max 5% kans op beter materiaal, totdat de 5 is bereikt
        elif skies_draw is not True and random.randint(0,100) < (max_materiaal - materiaal): 
            type = "skies"
            img = "skies.png"
            skies_draw = True
            if debug_mode == True:
                col = 0
        else:
            type = "flag"
            img = "skier_flag.png"

        location  = [col * 64 + 32, row * 64 + 32 + 640] #center x, y for obstacle
        if not (location in locations):        # prevent 2 obstacles in the same place
            locations.append(location)       
            obstacle = ObstacleClass(img, location, type)
            obstacles.add(obstacle)

# def create_hinders
    level = int(points / 200)
    for i in range(level):                 # 10 obstacles per screen 
        row = random.randint(0, 9)
        col = random.randint(0, 9)
        if debug_mode == True and col == 0:
            col = 1
        location  = [col * 64 + 32, row * 64 + 32 + 640] #center x, y for obstacle
        if not (location in locations):        # prevent 2 obstacles in the same place
            locations.append(location)
            type = "tree"
            img = random.choice(["skier_tree.png","skier_skihut.png"])
            obstacle = ObstacleClass(img, location, type)
            obstacles.add(obstacle)

    return obstacles


def draw_levens(nrlevens):
    row = 0
    for i in range(nrlevens):
        col = 9 - i
        location  = [col *  64 + 32, row * 64 + 32] #Levens staan altijd bovenaan rechts
        leven = LevensClass(location)
        screen.blit(leven.image, leven.rect)
        

# redraw the screen, including all sprites
def animate():
    screen.fill([255, 255, 255])
    obstacles.draw(screen)
    screen.blit(skier.image, skier.rect)
    levens.draw(screen)
    screen.blit(score_text, [10, 10])
    draw_levens(nrlevens)

    if debug_mode == True:
        screen.blit(snelheid_text, [10, 45])
        screen.blit(materiaal_text, [10, 80])

    pygame.display.flip()


def calculate_speed():
    now = pygame.time.get_ticks()
    seconds = (now - lastcrash) / 1000

    if debug_mode == True:
        game_speed = 300
    else:
        # Add that a high angle reduces the speed.
        game_speed = 10 + (5 * int(seconds / 5))
        
    max_speed = 200
    if game_speed > max_speed:
        game_speed = max_speed        

    return game_speed


def keys_pressed(speed, debug_mode, running):        
    if event.type == pygame.QUIT: running = False
        
    if event.type == pygame.KEYDOWN:          # check for key presses
        if event.key == pygame.K_LEFT:        # left arrow turns left
            speed = skier.turn(-1)
        elif event.key == pygame.K_RIGHT:     #right arrow turns right
            speed = skier.turn(1)
        elif event.key == pygame.K_ESCAPE:
            running = False
        elif event.key == pygame.K_d:
            mods = pygame.key.get_mods()
            if mods & pygame.KMOD_CTRL and mods & pygame.KMOD_SHIFT:
                if debug_mode == True:
                    debug_mode = False
                else:
                    debug_mode = True

    return (speed, debug_mode, running)


def crash(nrlevens):
    nrlevens = nrlevens - 1
    lastcrash = pygame.time.get_ticks()
    if nrlevens < 0:
        running = False
        delay = 1000
        skier.image = pygame.image.load("skier_dead.png")  # crash image
    else:
        running = True
        delay = 1000
        skier.image = pygame.image.load("skier_crash.png")  # crash image
        animate()
        pygame.time.delay(delay)
        skier.image = pygame.image.load("skier_recover.png")  # crash image

    animate()
    pygame.time.delay(delay)

    skier.image = pygame.image.load("skier_down.png")  # resume skiing
    skier.angle = 0
    speed = [0, 6]
    hit[0].passed = True

    return (nrlevens, running, lastcrash)


def is_highscore(highscores, score):
    scoresList = [ int(x) for x in sorted(highscores) ]
    print("Lijst van scores:", scoresList)
    minimalScore = min(scoresList)
    scoresAmount = len(scoresList)
    if score > minimalScore or (scoresAmount < MAX_HIGHSCORES and score > 0):
        print('Highscore reached!')
        return True


def get_name():
    new_highscore_text = font.render("Highscore! Name: ", 1, (255, 255, 255))

    name = ""
    input_given = True
    while input_given == True:
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                if evt.unicode.isalpha():
                    name += evt.unicode
                elif evt.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif evt.key == pygame.K_RETURN or evt.key == pygame.QUIT:
                    input_given = False                
        screen.fill([0, 0, 255])
        screen.blit(new_highscore_text, (150, 250))
        block = font.render(name, True, (255, 255, 255))
        rect = block.get_rect()
        rect.center = screen.get_rect().center
        screen.blit(block, rect)
        pygame.display.flip()
   
    return name


def add_to_highscores(highscores, score, name):
    highscores[str(score)] = name

    # beperken van de highscores door de laagste op te vragen
    # en te kijken of het maximum aantal highscores is overschreden    
    scoresList = [ int(x) for x in sorted(highscores) ]
    if len(scoresList) > MAX_HIGHSCORES:
        erase = min(scoresList)
        del highscores[str(erase)]

    return highscores


def read_highscores(filename):
    file = Path(filename)
    if file.exists():
        try:
            f = open(file,"r")
            fileScores = json.load(f)
            return fileScores
        except:
            print("Not able to read highscores from file")
    return { "0": "niemand" }


def write_highscores(file, highscores):
    f = open(file,"w")
    json.dump(highscores, f)


def display_highscores(highscores):
    X_positie = 150
    Y_positie = 50
    highscores_text = lfont.render("Highscores: ", 1, (0, 255, 0))
    screen.fill([0, 0, 255])
    screen.blit(highscores_text, (X_positie, Y_positie))
    pygame.display.flip()
    
    positionOffset = 75
    numberkeys = [ int(x) for x in sorted(highscores) ]
    sortedkeys = sorted(numberkeys, reverse=True)
    for key in sortedkeys:
        if key != 0:
            highscore_text = font.render(str(key)+'     '+str(highscores[str(key)]), 1, (0, 255, 0))
            screen.blit(highscore_text, (X_positie, Y_positie + positionOffset))
            pygame.display.flip()
            positionOffset += 40


def display_game_over():
    game_over_block = lfont.render("Game Over", 1, (255, 0, 0))
    rect = game_over_block.get_rect()
    rect.center = screen.get_rect().center
    screen.blit(game_over_block, rect)
    pygame.display.flip()
    pygame.time.delay(3000)


def wait_for_keypress():
    wait_for_key = True
    while wait_for_key == True:
        pygame.time.delay(100)
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN or evt.type == pygame.MOUSEBUTTONDOWN:
                print("Key pressed, exiting")
                wait_for_key = False
                

def game_over(screen, highscores_file):
    display_game_over()
    highscores = read_highscores(highscores_file)    
    if debug_mode == False and is_highscore(highscores, points):
        name = get_name()
        highscores = add_to_highscores(highscores, points, name)
        write_highscores(highscores_file, highscores)
    display_highscores(highscores)
    wait_for_keypress()


#############
### START ###
#############
#
debug_mode = False

pygame.init()
screen = pygame.display.set_mode([640,640])
clock = pygame.time.Clock()
speed = [0, 6]
obstacles = pygame.sprite.Group()   # group of obstacle objects
levens = pygame.sprite.Group()

skier = SkierClass()
map_position = 0
points = 0
max_levens = 3
max_materiaal = 5
nrlevens = 2
materiaal = 1
obstacles = create_map(obstacles)
draw_levens(nrlevens) 
font = pygame.font.Font(None, 50)
lfont = pygame.font.Font(None, 80)

game_speed = 5
highscores_file = 'highscores.txt'
MAX_HIGHSCORES = 5

# main Pygame event loop
running = True
lastcrash = pygame.time.get_ticks()

while running:        
    game_speed = calculate_speed()
    
    clock.tick(game_speed)
    for event in pygame.event.get():
        (speed, debug_mode, running) = keys_pressed(speed, debug_mode, running)
                    
    skier.move(speed)                         # move the skier (left or right)
    map_position += speed[1]                      # scroll the obstacles
    
    # create a new block of obstacles at the bottom
    if map_position >= 640:
        obstacles = create_map(obstacles)
        map_position = 0
    
    # check for hitting trees or getting flags
    hit =  pygame.sprite.spritecollide(skier, obstacles, False)
    if hit:
        if hit[0].type == "tree" and not hit[0].passed:  #crashed into tree
            (nrlevens, running, lastcrash) = crash(nrlevens)
        elif hit[0].type == "flag" and not hit[0].passed:   # got a flag
            points += 10
            hit[0].kill()                                 # remove the flag
        elif hit[0].type == "life" and not hit[0].passed:
            nrlevens = nrlevens + 1
            hit[0].kill()
        elif hit[0].type == "skies" and not hit[0].passed:
            materiaal = materiaal + 0.25
            hit[0].kill()
    
    obstacles.update()
    score_text = font.render("Score: " +str(points), 1, (0, 0, 0))
    snelheid_text = font.render("Snelheid: " +str(game_speed), 1, (0, 0, 0))
    materiaal_text = font.render("Materiaal: " +str(materiaal), 1, (0, 0, 0))

    if running != False:
        animate()
    else:
        game_over(screen, highscores_file)

        
pygame.quit()
    
