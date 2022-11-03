#Goal: try to kill the squares w bullets

#sources: https://github.com/nealholt/python_programming_curricula/tree/master/CS1/0550_galaga
import pygame, math, random

pygame.init()

#Initialize variables:
clock = pygame.time.Clock() #defins FPS
screen_width = 1920
screen_height = 1080
surface = pygame.display.set_mode((screen_width,screen_height))
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#making square

class Square:
    def __init__(self, color, x, y, width, height, speed): #getting the dimensions of the squares and their speed at which they go down at
        self.rect = pygame.Rect(x,y,width,height)
        self.color = color
        self.direction = 'E'
        self.speed = 5 #changes both speed of the enemies and self

    def move(self): 
        if self.direction == 'E': 
            self.rect.x = self.rect.x+self.speed
        if self.direction == 'W':
            self.rect.x = self.rect.x-self.speed
        if self.direction == 'N':
            self.rect.y = self.rect.y-self.speed
        if self.direction == 'S':
            self.rect.y = self.rect.y+self.speed

    def moveDirection(self, direction): #East, West, North, South -> tells which one is up donw... later on the EWNS is coded into the keys(ex. E -> go to the right -> press D key)
        if direction == 'E':
            self.rect.x = self.rect.x+self.speed
        if direction == 'W':
            self.rect.x = self.rect.x-self.speed
        if direction == 'N':
            self.rect.y = self.rect.y-self.speed
        if direction == 'S':
            self.rect.y = self.rect.y+self.speed

#COLLISION TIME BAYBE

    def collided(self, other_rect): 
        #Return True if self collided with other_rect
        return self.rect.colliderect(other_rect)

    def draw(self, surface): #draws the square
        pygame.draw.rect(surface, self.color, self.rect)

#bullet class
class Bullet(Square):
    def __init__(self, color, x, y, width, height, speed, targetx,targety): #sets the bullet dimensions, color 
        super().__init__(color, x, y, width, height, speed)
        angle = math.atan2(targety-y, targetx-x) 
        print('Angle in degrees:', int(angle*180/math.pi)) #math...prints out angles... radians
        self.dx = math.cos(angle)*speed  #applies speed to certain angle where curson is @
        self.dy = math.sin(angle)*speed #same thing but in y up and down
        self.x = x
        self.y = y
#^^^ short term, it turns the window as a x and y graph... 
    def move(self):
        #self.x and self.y deciamls for accuracy
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)


#Build a square
sq = Square(GREEN,200,200,100,100, 10)

bullets = [] # turns bull and ene to lists
enemies = []

#Main program loop
done = False
while not done:
    #Get user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            print(event.key) #Print value of key pressd ex... 119 = W = upwards 
            """if event.key==119: #w
                sq.direction = 'N'
            if event.key==97: #a
                sq.direction = 'W'
            if event.key==115: #s
                sq.direction = 'S'
            if event.key==100: #d
                sq.direction = 'E'"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos() # info of position of mouse is extracted
            b = Bullet(RED, sq.rect.centerx, sq.rect.centery, 20,20, 20, x,y)
            bullets.append(b) #shoots the bullet from the center of the square

    #Keys pressed 
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        sq.moveDirection('N')
    if pressed[pygame.K_a]:
        sq.moveDirection('W')
    if pressed[pygame.K_s]:
        sq.moveDirection('S')
    if pressed[pygame.K_d]:
        sq.moveDirection('E')
        
    #UPDATE BULL AND ENE
    for b in bullets:
        b.move()
    for e in enemies:
        e.move()
    #spawn enemies top to bottom 
    if random.randint(1,30) == 15: 
        x = random.randint(0,screen_width-40)
        e = Square(BLUE, x,-40, 40,40, 10)
        e.direction = 'S'
        enemies.append(e)
    #Checks for collisions
    '''for b in bullets:
        for e in enemies:
            if b.collided(e.rect):
                #e.color = white #TESTING
                enemies.remove(e)
                bullets.remove(b)'''
    for i in reversed(range(len(bullets))):
        for j in reversed(range(len(enemies))):
            if bullets[i].collided(enemies[j].rect):
                # delete the bullets and enemies when off the screen so it doesnt lag
                del enemies[j]
                del bullets[i]
                break

    #All the drawing/ display / quit
    surface.fill(BLACK) # fills background with black color
    for b in bullets:
        b.draw(surface) # makes sure everything is shown in the display
    for e in enemies:
        e.draw(surface)
    sq.draw(surface)
    pygame.display.flip()
    clock.tick(60) #60 FPS
pygame.quit()
exit()
