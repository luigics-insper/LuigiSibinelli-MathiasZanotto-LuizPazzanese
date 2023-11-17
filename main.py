import pygame
import math
pygame.init()
WIDTH , HEIGHT = 800 , 600
win = pygame.display.set_mode((WIDTH,HEIGHT)) #window
pygame.display.set_caption('Brick Breaker')

FPS = 60
platform_width = 100
platform_height = 15
ball_radius = 10
FONTE_VIDAS = pygame.font.SysFont("arial", 25)
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

class Tijolos():
    def __init__(self, x, y, largura, altura, vida, cores):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.vida = 2
        self.vida_maxima = vida
        self.cores = cores
        self.cor = cores[0]

    def draw(self, win):
        pygame.draw.rect(win, self.cor, (self.x, self.y, self.largura, self.altura))

    def colisao(self, ball):
        if not (ball.x <= self.x + self.largura and ball.x >= self.x):
            return False
        if not (ball.y - ball.radius <= self.y + self.altura):
            return False
        self.acerto()
        ball.set_velocity(ball.x_vel, ball.y_vel * -1)
        return True
    
    def acerto(self):
        self.vida -= 1
        self.cor = self.interpolar(*self.cores, self.vida/self.vida_maxima)
    
    @staticmethod
    def interpolar(cor1, cor2, t):
        return tuple(int(a + (b - a) * t) for a, b in zip(cor1, cor2))

def draw(win,platform,ball,tijolos,vidas): #colorir
    win.fill('white')
    platform.draw(win)
    ball.draw(win)

    for tijolo in tijolos:
        tijolo.draw(win)

    vidas_texto = FONTE_VIDAS.render(f"Vidas restantes: {vidas}", 1, "black")
    win.blit(vidas_texto, (10, HEIGHT - vidas_texto.get_height() - 10))

    pygame.display.update()

def ball_collision(ball): # colisoes com paredes
    if ball.x -ball_radius <= 0 or ball.x + ball_radius>= WIDTH:
        ball.set_velocity(ball.x_vel * -1,ball.y_vel)
    if ball.y + ball_radius>= HEIGHT or ball.y - ball_radius <= 0:
        ball.set_velocity(ball.x_vel, ball.y_vel * -1)

def platform_ball_collision(ball, platform): # colisao entre bola e plataforma
    if not (ball.x <= platform.x + platform.width and ball.x >= platform.x):
        return
    if not (ball.y + ball.radius >= platform.y):
        return
    
    platform_center = platform.x + platform.width/2
    distance_to_center = ball.x - platform_center

    percent_width = distance_to_center / platform.width
    ang = percent_width * 90
    ang_rad = math.radians(ang)

    x_vel = math.sin(ang_rad) * ball.VEL
    y_vel = math.cos(ang_rad) * ball.VEL * -1

    ball.set_velocity(x_vel, y_vel)

def gerar_tijolos(linhas, colunas):
    tijolos = []

    altura_tijolo = 20
    largura_tijolo = (WIDTH // colunas) - 2

    for linha in range(linhas):
        for coluna in range(colunas):
            tijolo = Tijolos(largura_tijolo * coluna + 2 * coluna, altura_tijolo * linha + 2 * linha, largura_tijolo, altura_tijolo, 5, [(0, 255, 0), (255, 0, 0)])
            tijolos.append(tijolo)
    
    return tijolos

def main():
    clock = pygame.time.Clock()

    platform_x = WIDTH/2 - platform_width / 2
    platform_y = HEIGHT - platform_height - 5
    platform = Platform(platform_x, platform_y,platform_width ,platform_height, 'black')

    vidas = 3

    ball = Ball(WIDTH/2, platform_y - ball_radius, ball_radius,'black')
    tijolos = gerar_tijolos(3, 10)

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
        ball_collision(ball)
        platform_ball_collision(ball,platform)


        for tijolo in tijolos[:]:
            tijolo.colisao(ball)
            if tijolo.vida <= 0:
                tijolos.remove(tijolo)

        #PERDER VIDAS
        if ball.y + ball.radius >= HEIGHT:
            vidas -= 1
            ball.x = platform.x + platform_width/2 
            ball.y = platform_y - ball_radius
            ball.set_velocity(0, ball.VEL *- 1)

        if vidas <= 0:
            platform = Platform(platform_x, platform_y, platform_width, platform_height, 'black')
            ball = Ball(WIDTH/2, platform_y - ball_radius, ball_radius, 'black')
            tijolos = gerar_tijolos(3,10)
            vidas = 3

            texto_derrota = FONTE_VIDAS.render('Você perdeu!', 1, 'red')
            win.blit(texto_derrota, (WIDTH/2 - texto_derrota.get_width()/2, HEIGHT/2 - texto_derrota.get_height()/2))
            pygame.display.update()
            pygame.time.delay(5000)
            
        draw(win, platform, ball, tijolos, vidas)
            
        

    pygame.quit()
    quit()

if __name__ == '__main__':
    main()

