#Six Second Summoning
import pygame
import random
import time
import math
from pygame.locals import (
    RLEACCEL,
    KEYDOWN,
    K_ESCAPE,
    QUIT,
    K_SPACE,
)

# initialize pygame
pygame.init()

#music
music = pygame.mixer.music.load('music/summon_music.mp3')

#screen width and height
SCREEN_WIDTH=1000
SCREEN_HEIGHT=800

#time to draw summoning circles
total_time = 20

hi_score = 0

# splotch
class Splotch(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Splotch, self).__init__()
        self.surf = pygame.image.load("img/splotch.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.x = x
        self.y = y
        self.rect = self.surf.get_rect(center= (self.x, self.y))

# DUCK!
class Duck(pygame.sprite.Sprite):
    def __init__(self, x, y, scale = 3):
        super(Duck, self).__init__()
        self.surf1 = pygame.image.load("img/duckWithHat.png").convert_alpha()
        self.surf1.set_colorkey((255, 255, 255), RLEACCEL)
        self.x = x
        self.y = y
        self.size = self.surf1.get_size()
        self.surf = pygame.transform.scale(self.surf1, (int(self.size[0]*scale), int(self.size[1]*scale)))
        self.rect = self.surf.get_rect(center= (self.x, self.y))

# GOOSE!
class Goose(pygame.sprite.Sprite):
    def __init__(self, x, y, scale = 3):
        super(Goose, self).__init__()
        self.surf1 = pygame.image.load("img/goose.png").convert_alpha()
        self.surf1.set_colorkey((255, 255, 255), RLEACCEL)
        self.x = x
        self.y = y
        self.size = self.surf1.get_size()
        self.surf = pygame.transform.scale(self.surf1, (int(self.size[0]*scale), int(self.size[1]*scale)))
        self.rect = self.surf.get_rect(center= (self.x, self.y))

# Summoning circle
class Summon(pygame.sprite.Sprite):
    def __init__(self):
        super(Summon, self).__init__()
        self.surf = pygame.image.load("img/redSummon.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.x = int(SCREEN_WIDTH//2 + 200)
        self.y = SCREEN_HEIGHT // 2
        self.rect = self.surf.get_rect(center= (self.x, self.y))

# star
class Star(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Star, self).__init__()
        self.surf = pygame.image.load("img/redStar.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.x = x
        self.y = y
        self.rect = self.surf.get_rect(center= (self.x, self.y))

# blueCircle
class BlueCircle(pygame.sprite.Sprite):
    def __init__(self):
        super(BlueCircle, self).__init__()
        self.surf = pygame.image.load("img/blueCircle.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.x = int(SCREEN_WIDTH//2)
        self.y = SCREEN_HEIGHT // 2 + 200
        self.rect = self.surf.get_rect(center= (self.x, self.y))
    
    def rot_center(self):
        return

# blueStar
class BlueStar(pygame.sprite.Sprite):
    def __init__(self):
        super(BlueStar, self).__init__()
        self.surf = pygame.image.load("img/blueStar.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.x = int(SCREEN_WIDTH//2)
        self.y = SCREEN_HEIGHT // 2 + 200
        self.angle = 0
        self.curnum = 0
        self.rect = self.surf.get_rect(center= (self.x, self.y))
    
    def rot_center(self):
        self.angle += 1
        if self.angle % 10 == 0:
            self.curnum += 1
            if self.curnum >= 6:
                self.curnum -= 6
            self.surf = pygame.image.load(bluestars[self.curnum % 6]).convert_alpha()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)

bluestars = ["img/blueStar.png",
             "img/blueCircle1.png",
             "img/blueCircle2.png",
             "img/blueCircle4.png",
             "img/blueCircle5.png",
             "img/blueCircle6.png"]

# splotch group
splotches = pygame.sprite.Group()

# star group
stars = pygame.sprite.Group()

# geese group
geese_group = pygame.sprite.Group()

# duck group
duck_group = pygame.sprite.Group()

# blue group
blue_group = pygame.sprite.Group()

# draw text
def draw_text(surface, text, size, color, x, y):  
    font = pygame.font.SysFont ("Times", size, bold = True)
    label = font.render (text, 1, color)
    
    surface.blit(label,(x,y))

score_table = [[100, 90, 75],
               [90, 80, 60],
               [75, 60, 50]]

# score calculation
def calculate_score():
    global hi_score
    splotches2 = pygame.sprite.Group()
    dot_in_each = [0, 0, 0, 0, 0, 0]
    var_in_each = [0, 0, 0, 0, 0, 0]
    for spl in splotches:
        if pygame.sprite.spritecollideany(spl, splotches2):
            continue
        splotches2.add(spl)
        min_distance = 1000
        
        for star in stars:
            min_distance = min(min_distance, math.dist([spl.x, spl.y], [star.x, star.y]))
        
        if spl.x < SCREEN_WIDTH//3 and spl.y < SCREEN_HEIGHT//2:
            dot_in_each[0] += 1
            var_in_each[0] = max(var_in_each[0], abs(min_distance - 90))
        elif spl.x < SCREEN_WIDTH//3 and spl.y >= SCREEN_HEIGHT//2:
            dot_in_each[1] += 1
            var_in_each[1] = max(var_in_each[1], abs(min_distance - 90))
        elif spl.x < SCREEN_WIDTH//3 * 2 and spl.y < SCREEN_HEIGHT//2:
            dot_in_each[2] += 1
            var_in_each[2] = max(var_in_each[2], abs(min_distance - 90))
        elif spl.x < SCREEN_WIDTH//3 * 2 and spl.y >= SCREEN_HEIGHT//2:
            dot_in_each[3] += 1
            var_in_each[3] = max(var_in_each[3], abs(min_distance - 90))
        elif spl.y < SCREEN_HEIGHT//2:
            dot_in_each[4] += 1
            var_in_each[4] = max(var_in_each[4], abs(min_distance - 90))
        else:
            dot_in_each[5] += 1
            var_in_each[5] = max(var_in_each[5], abs(min_distance - 90))
        #print(min_distance)
    success = True
    score = 0
    ducks = 0
    geese = 0
    for i in range(6):
        if var_in_each[i] > 40 or dot_in_each[i] < 5:
            success = False
        elif var_in_each[i] > 30 or dot_in_each[i] < 10:
            score += 10
            geese += 1
        else:
            ducks += 1
            tx = int(var_in_each[i]) // 10
            ty = 3 - dot_in_each[i] // 10
            if ty < 0:
                ty = 0
            if tx > 2:
                tx = 2
            score += score_table[tx][ty]
    if success:
        hi_score = max(hi_score, score)
        if score == 600:
            hi_score = 666
    return success, score, ducks, geese

#the timer
start_time = time.time()
end_time = time.time()

#play game
def main(screen):
    # display screen
    running = True
    add_splotch = False
    global start_time
    global end_time
    start_time = time.time()
    end_time = time.time()
    
    # summon six stars
    star1 = Star(random.randint(100,int(SCREEN_WIDTH/3)-100), random.randint(150, int(SCREEN_HEIGHT/2) - 150))
    stars.add(star1)
    star2 = Star(random.randint(int(SCREEN_WIDTH/3)+100,int(SCREEN_WIDTH/3)*2-100), random.randint(150, SCREEN_HEIGHT//2 - 150))
    stars.add(star2)
    star3 = Star(random.randint(int(SCREEN_WIDTH/3)*2+100, SCREEN_WIDTH-100), random.randint(150, SCREEN_HEIGHT//2 - 150))
    stars.add(star3)
    star4 = Star(random.randint(100,int(SCREEN_WIDTH/3)-100), random.randint(int(SCREEN_HEIGHT/2) + 100, SCREEN_HEIGHT - 200))
    stars.add(star4)
    star5 = Star(random.randint(int(SCREEN_WIDTH/3)+100,int(SCREEN_WIDTH/3)*2-100), random.randint(SCREEN_HEIGHT//2 + 100, SCREEN_HEIGHT - 200))
    stars.add(star5)
    star6 = Star(random.randint(int(SCREEN_WIDTH/3)*2+100, SCREEN_WIDTH-100), random.randint(SCREEN_HEIGHT//2 + 100, SCREEN_HEIGHT - 200))
    stars.add(star6)
    
    # play game
    while running:
        # mouse
        mouse = pygame.mouse.get_pos()
        # /mouse
        # time
        end_time = time.time()
        
        # events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                add_splotch = True
                if SCREEN_WIDTH-252 < mouse[0] < SCREEN_WIDTH-252 + 220:
                    if SCREEN_HEIGHT-60 < mouse[1] < SCREEN_HEIGHT - 20:
                        add_splotch = False
            if event.type == pygame.MOUSEBUTTONUP:
                add_splotch = False
                if SCREEN_WIDTH-252 < mouse[0] < SCREEN_WIDTH-252 + 220:
                    if SCREEN_HEIGHT-60 < mouse[1] < SCREEN_HEIGHT - 20:
                        running = False
            # debugging code
            #if event.type == KEYDOWN:
            #    if event.key == K_SPACE:
            #        for s in splotches:
            #            s.kill()
            # /debugging code
        
        # add splotches
        if add_splotch:
            new_splotch = Splotch(mouse[0], mouse[1])
            splotches.add(new_splotch)
        
        # background
        screen.fill((72,0,100))
        
        # draw stars
        for s in stars:
            screen.blit(s.surf, s.rect)
        
        # draw splotches
        for s in splotches:
            screen.blit(s.surf, s.rect)
        
        # Finish summon button
        b_surf = pygame.Surface((220,30))
        b_surf.fill((162, 64, 227))
        screen.blit(b_surf,(SCREEN_WIDTH-252, SCREEN_HEIGHT-60))
        draw_text(screen, "FINISH SUMMONS", 24, (0,0,20), SCREEN_WIDTH-250, SCREEN_HEIGHT-60)
        
        # timer text
        cur_time = str(round(total_time-(end_time-start_time), 2))
        draw_text(screen, cur_time, 40, (255, 217, 92), int(SCREEN_WIDTH/2)-50, SCREEN_HEIGHT-60)
        
        if end_time-start_time > total_time:
            running = False
        
        # update screen
        pygame.display.flip()
    
    return end_screen(screen)

def end_screen(screen):
    success, score, ducks, geese = calculate_score()
    if score == 600:
        score = 666
    #print(success, score, ducks, geese)
    for i in range(ducks):
        new_duck = Duck(i*100 + 100, 300)
        duck_group.add(new_duck)
    for i in range(geese):
        new_geese = Goose(i*100 + 100, 500)
        geese_group.add(new_geese)
    
    text1 = ""
    text2 = f"YOU HAVE SUMMONED {ducks} DUCKS AND {geese} GEESE".format(ducks=ducks, geese=geese)
    text3 = ""
    text4 = f"SCORE: {score}".format(score=score)
    if success:
        text1 = "CONGRATULATIONS ON YOUR SIX SUCCESSFUL SUMMONS!"
        if geese == 6:
            text3 = "6 GEESE? REALLY? DO BETTER NEXT TIME"
        elif ducks == 6 and score < 600:
            text3 = "WOW, YOU ACTUALLY SUMMONED 6 DUCKS! THAT'S IMPRESSIVE!"
        elif ducks == 6 and score == 666:
            text3 = "THAT'S A PERFECT SCORE. HOW... JUST HOW?"
        else:
            text3 = "SOME DUCKS, SOME GEESE. TRY AIMING FOR 6 DUCKS!" 
    else:
        text1 = "NOOOOOOOOO! YOU HAVE FAILED TO DRAW SIX SUMMONING CIRCLES!"
        text3 = "INCOMPLETE CIRCLES MAY STILL SUMMON GEESE"
    
    # display screen
    running = True
    while running:
        # mouse
        mouse = pygame.mouse.get_pos()
        # /mouse
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                return "quit"
            #debugging
            #if event.type == KEYDOWN:
            #    if event.key == K_SPACE:
            #        return "neutral"
            if event.type == pygame.MOUSEBUTTONUP:
                if SCREEN_WIDTH-252 < mouse[0] < SCREEN_WIDTH-252 + 220:
                    if SCREEN_HEIGHT-60 < mouse[1] < SCREEN_HEIGHT - 20:
                        running = False
        # background
        screen.fill((72,0,100))
        
        draw_text(screen, text1, 25, (245, 125, 197), 5, 5)
        draw_text(screen, text2, 25, (245, 125, 197), 5, 35)
        draw_text(screen, text3, 25, (245, 125, 197), 5, 70)
        
        # blue summon
        if ducks == 6:
            for b in blue_group:
                screen.blit(b.surf, b.rect)
                b.rot_center()
        
        # home button
        b_surf = pygame.Surface((220,30))
        b_surf.fill((162, 64, 227))
        screen.blit(b_surf,(SCREEN_WIDTH-252, SCREEN_HEIGHT-60))
        draw_text(screen, "BACK TO MENU", 24, (0,0,20), SCREEN_WIDTH-238, SCREEN_HEIGHT-60)
        
        for d in duck_group:
            screen.blit(d.surf, d.rect)
        for g in geese_group:
            screen.blit(g.surf, g.rect)
        
        draw_text(screen, text4, 30, (125, 239, 245), 5, 130)
        pygame.display.flip()
    return "neutral"
            

def main_menu():
    # display screen
    status = "neutral"
    pygame.mixer.music.play(-1)
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
    run = True
    add_splotch = False
    summon = Summon()
    bigDuck = Duck(200, int(SCREEN_HEIGHT/2), 5)
    bigGoose = Goose(400, int(SCREEN_HEIGHT/2), 5)
    bc = BlueCircle()
    bs = BlueStar()
    blue_group.add(bc)
    blue_group.add(bs)
    while run:
        # mouse
        mouse = pygame.mouse.get_pos()
        # /mouse
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                add_splotch = True
            if event.type == pygame.MOUSEBUTTONUP:
                add_splotch = False
                if int(SCREEN_WIDTH/2)-250 < mouse[0] < int(SCREEN_WIDTH/2) + 250:
                    if int(SCREEN_HEIGHT/4) * 3 < mouse[1] < int(SCREEN_HEIGHT/4) * 3 + 70:
                        for s in splotches:
                            s.kill()
                        status = main(screen)
                        for s in splotches:
                            s.kill()
                        for s in stars:
                            s.kill()
                        for d in duck_group:
                            d.kill()
                        for g in geese_group:
                            g.kill()
        if status == "quit":
            run = False
        
        # add splotches
        if add_splotch:
            new_splotch = Splotch(mouse[0], mouse[1])
            splotches.add(new_splotch)
                
        # background
        screen.fill((72,0,100))
            
        # draw button
        b_surf = pygame.Surface((500,70))
        b_surf.fill((162, 64, 227))
        screen.blit(b_surf,(int(SCREEN_WIDTH/2)-250,int(SCREEN_HEIGHT/4) * 3))
        draw_text(screen, "SUMMON!!!", 40, (0,0,20), int(SCREEN_WIDTH/2)-100, int(SCREEN_HEIGHT/4) * 3 + 10)
        
        # instructions
        draw_text(screen, "TWENTY SECONDS TO SUMMON SIX DUCKS!", 30, (245, 125, 197), 5, 5)
        draw_text(screen, "BEAT THE GAME WITH SIX SUCCESSFUL SUMMONS!", 30, (245, 125, 197), 5, 35)
        draw_text(screen, "(Geese count as successful summons)", 20, (245, 125, 197), 5, 70)
        
        draw_text(screen, "High score: " + str(hi_score), 30, (125, 239, 245), 5, 130)
        
        draw_text(screen, "HOLD DOWN MOUSE BUTTON TO DRAW", 30, (245, 125, 197), 5, 200)
        draw_text(screen, "DRAW THE BEST SUMMONING CIRCLES", 30, (245, 125, 197), 5, 230)
        draw_text(screen, "AROUND THE 5 POINTED STARS", 30, (245, 125, 197), 5, 260)
        
        screen.blit(summon.surf,summon.rect)
        screen.blit(bigDuck.surf, bigDuck.rect)
        screen.blit(bigGoose.surf, bigGoose.rect)
        
        # draw splotches
        for s in splotches:
            screen.blit(s.surf, s.rect)
        
        # update screen
        pygame.display.flip()
    # quitting game
    pygame.mixer.music.stop()
    pygame.quit()

pygame.display.set_caption('TWENTY SECOND SUMMONING')
main_menu()