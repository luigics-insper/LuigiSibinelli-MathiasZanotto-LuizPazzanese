import pygame

WIDTH , HEIGHT = 800 , 600
win = pygame.display.set_mode((WIDTH,HEIGHT)) #window
pygame.display.set_caption('Brick Breaker')

FPS = 60
platform_width = 100
platform_height = 15
ball_radius = 10
class Platform: #plataforma
    VEL = 5

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self,win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

    def movement(self, direction=1):
        self.x = self.x + self.VEL * direction

class Ball: #bola
    VEL = 5

    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.x_vel = 2
        self.y_vel = -self.VEL


    def movement(self): #movimento da bola
        self.x += self.x_vel
        self.y += self.y_vel

    def set_velocity(self,x_vel,y_vel): #vel da bola
        self.x_vel = x_vel
        self.y_vel = y_vel

    def draw(self,win): #desenha a bolinha
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)




def draw(win,platform,ball): #colorir
    win.fill('white')
    platform.draw(win)
    ball.draw(win)
    pygame.display.update()

def ball_colission(ball): #por enquanto so tem as colisoes com paredes, falta com a plataforma
    if ball.x -ball_radius <= 0 or ball.x + ball_radius>= WIDTH:
        ball.set_velocity(ball.x_vel * -1,ball.y_vel)
    if ball.y + ball_radius>= HEIGHT or ball.y - ball_radius <= 0:
        ball.set_velocity(ball.x_vel, ball.y_vel * -1)
    

def main():
    clock = pygame.time.Clock()

    platform_x = WIDTH/2 - platform_width / 2
    platform_y = HEIGHT - platform_height - 5
    platform = Platform(platform_x, platform_y,platform_width ,platform_height, 'black')

    ball = Ball(WIDTH/2, platform_y - ball_radius, ball_radius,'black')

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            keys = pygame.key.get_pressed()

            
        if keys[pygame.K_LEFT] and platform.x - platform.VEL >= 0:
                    platform.movement(-1)
        if keys[pygame.K_RIGHT] and platform.x + platform.width + platform.VEL <= WIDTH:
                    platform.movement(1)
            
        ball.movement()
        ball_colission(ball)
        draw(win, platform, ball)
        

    pygame.quit()
    quit()

if __name__ == '__main__':
    main()

