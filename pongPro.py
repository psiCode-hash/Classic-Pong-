import pygame as p

p.init()

fps_Game = p.time.Clock()
screen_width = 600
screen_height = 500

screen = p.display.set_mode((screen_width,screen_height))
p.display.set_caption("Pong 3.0")

font = p.font.SysFont("Constantia" , 30)
#define game variables
live_ball = False
margin = 50
cpu_score = 0
player_score = 0
fps = 60
winner = 0
speed_increase = 0

#define colours
bg = (50,25,50)
white = (255,255,255)

def draw_board():
    screen.fill(bg)
    p.draw.line(screen , white , (0,margin) , (screen_width , margin))

def draw_text(text,font,text_color,x,y):
    img = font.render(text , True , text_color)
    screen.blit(img , (x, y))

class paddle():
    def __init__(self , x , y) :
        self.x = x
        self.y = y
        self.rect = p.Rect(self.x , self.y ,  20 , 100)
        self.speed = 5

    def move(self):
        key = p.key.get_pressed()
        if key[p.K_UP] and self.rect.top > margin :
            self.rect.move_ip(0,-1*self.speed)
        if key[p.K_DOWN] and self.rect.bottom < screen_height:
            self.rect.move_ip(0,self.speed)
    
    #ai for moving the cpu paddle automatically 
    def ai(self):
        if self.rect.centery < pong.rect.top and self.rect.bottom < screen_height :
            self.rect.move_ip(0,self.speed)
        if self.rect.centery > pong.rect.bottom and self.rect.top > margin :
            self.rect.move_ip(0,-1*self.speed)

    def draw(self):
        p.draw.rect(screen , white ,  self.rect)

class ball():
    def __init__(self,x,y) :
        self.reset(x,y)

    def draw(self):
        p.draw.circle(screen , white , (self.x + self.ball_rad , self.y + self.ball_rad) , self.ball_rad)

    def move(self):
        #check for collision detection 
        if self.rect.top < margin :
            self.y_speed *= -1
        if self.rect.bottom > screen_height :
            self.y_speed *= -1
        #collision with paddle
        if self.rect.colliderect(player_paddle) or self.rect.colliderect(cpu_paddle) :
            self.x_speed *= -1

        #check for out of bounds 
        if self.rect.left < 0 :
            self.winner = 1
        if self.rect.right > screen_width :
            self.winner = -1

        #update position of the ball
        self.x += self.x_speed
        self.y += self.y_speed
        self.rect.x = self.x
        self.rect.y = self.y
        
        return self.winner
    
    def reset(self,x,y):
        self.x = x
        self.y = y
        self.ball_rad = 10
        self.rect = p.Rect(self.x , self.y , self.ball_rad , self.ball_rad)
        self.x_speed = -3
        self.y_speed = 3
        self.winner = 0 # 1 : player scored , -1 : cpu scored

#create paddle 
cpu_paddle = paddle(20 , screen_height // 2)   
player_paddle = paddle(screen_width - 40 , screen_height // 2)   

#create ball
pong = ball(screen_width - 60 , screen_height // 2)

run = True
while(run):

    fps_Game.tick(fps)

    draw_board()
    draw_text("CPU : " + str(cpu_score) , font , white , 20 , 15)
    draw_text("PLA1 : " + str(player_score) , font , white , screen_width-120 , 15)
    draw_text("Ball Speed : " + str(abs(pong.x_speed)) , font , white , screen_width//2 - 70 , 15)

    #draw paddles
    cpu_paddle.draw()
    player_paddle.draw()
    
    if live_ball == True:
        speed_increase += 1
        #move ball
        winner = pong.move()
        
        if winner == 0 :
            #draw ball
            pong.draw()

            #move paddles
            player_paddle.move()
            cpu_paddle.ai()

        else :
            live_ball = False 
            if winner == 1 :
                player_score += 1
            elif winner == -1 :
                cpu_score += 1

    #print player instructions 
    if live_ball == False :
        if winner == 0 :
            draw_text('CLICK ANYWHERE TO START' , font , white , screen_width//2 - 200 ,screen_height//2 - 100)
        elif winner == 1 :
            draw_text('Player 1 scored !' , font ,white ,screen_width//2 - 100 , screen_height//2 )
            draw_text('CLICK ANYWHERE TO START' , font , white , screen_width//2 - 200 , screen_height//2 + 50)
        elif winner == -1 :
            draw_text('CPU scored !' , font ,white ,screen_width//2 - 100 , screen_height//2 )
            draw_text('CLICK ANYWHERE TO START' , font , white , screen_width//2 - 200 , screen_height//2 + 50)


    for event in p.event.get():
        if event.type == p.QUIT:
            run = False
        if event.type == p.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            pong.reset(screen_width - 60 , screen_height // 2)

    if speed_increase > 500 :
        speed_increase = 0
        if pong.x_speed < 0 : 
            pong.x_speed -= 1
        if pong.x_speed > 0 :
            pong.x_speed += 1
        if pong.y_speed < 0 : 
            pong.y_speed -= 1
        if pong.y_speed > 0 :
            pong.y_speed += 1

    p.display.update()

p.quit()