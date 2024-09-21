import turtle
import random
import pygame
import time
import emoji
import vlc

# Membuat instance VLC
instance = vlc.Instance()
p = instance.media_player_new()
media = instance.media_new('Source/game-music-loop-7-145285.mp3')
p.set_media(media)

# Mulai pemutaran
p.play()
    

pygame.mixer.init()
screen = turtle.Screen()
heart_emoji = emoji.emojize(':red_heart:')
start = 1
# Set the animation speed
turtle.speed(1)
# change the background color
turtle.bgcolor("black")
# Background image
turtle.bgpic("Source/ezgif-7-62814face8.gif")
# window title
turtle.title("PesawatTempur")
# hide the default turtle
turtle.ht()
# this save memory
turtle.setundobuffer(1)
# this speeds of drawing
turtle.tracer(20)

class Sprit(turtle.Turtle):
    def __init__(self, spritshape, color, startx, starty):
       turtle.Turtle.__init__(self, shape=spritshape)
       self.speed(0)
       self.penup()
       self.color(color)
       self.fd(0)
       self.goto(startx, starty)
       self.speed = 1

    def mive(self):
        self.speed = 0
        self.fd(self.speed)

        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)
            
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)
        
        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

    def move(self):
        self.fd(self.speed)

        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)
            
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)
        
        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

    def is_kolisi(self, other):
        if (self.xcor() >= (other.xcor() - 20)) and \
        (self.xcor() <= (other.xcor() + 20)) and \
        (self.ycor() >= (other.ycor() - 20)) and \
        (self.ycor() <= (other.ycor() + 20)):
            return True
        else: return False

class Player(Sprit):
    def __init__(self, spritshape, color, startx, starty):
        Sprit.__init__(self, spritshape, color, startx, starty)
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
        self.speed = 4
        self.is_invincible = False
        self.invincible_timer = 0
        self.original_color = color
        

    def belok_kiri(self):
        self.lt(45)

    def belok_kanan(self):
        self.rt(45)

    def belok_left(self):
        self.lt(45)

    def belok_right(self):
        self.rt(45)

    def akselerasi(self):
        self.speed += 1

    def deklarasi(self):
        self.speed -= 1

    def aksel(self):
        self.speed += 1

    def deklar(self):
        self.speed -= 1

    def toggle_invincibility(self, duration=3):
        self.is_invincible = True
        self.invincible_timer = time.time() + duration
        self.color("yellow")  # Ubah warna saat kebal

    def update_invincibility(self):
        if self.is_invincible and time.time() > self.invincible_timer:
            self.is_invincible = False
            self.color(self.original_color)



class Musuh(Sprit):
    def __init__(self, spritshape, color, startx, starty):
        Sprit.__init__(self, spritshape, color, startx, starty)
        self.speed = 6
        self.setheading(random.randint(0,360))


class Ally(Sprit):
    def __init__(self, spritshape, color, startx, starty):
        Sprit.__init__(self, spritshape, color, startx, starty)
        self.speed = 6
        self.setheading(random.randint(0,360))
    
    def move(self):
        self.fd(self.speed)

        if self.xcor() > 290:
            self.setx(290)
            self.lt(60)
            
        if self.xcor() < -290:
            self.setx(-290)
            self.lt(60)
        
        if self.ycor() > 290:
            self.sety(290)
            self.lt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.lt(60)


class Misil(Sprit):
    def __init__(self, spritshape, color, startx, starty):
        Sprit.__init__(self, spritshape, color, startx, starty)
        self.shapesize(stretch_wid=0.2, stretch_len=0.4, outline=None)
        self.speed = 20
        self.status = "siap"
        self.goto(-1000, 1000)

    def api(self):
        if self.status == "siap":
            pygame.mixer.music.load("Source/retro-laser-1-236669.mp3")
            pygame.mixer.music.play()
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "menembak"

    def move(self):

        if self.status == "siap":
            self.goto(-1000,1000)

        if self.status == "menembak":
            self.fd(self.speed)

        # Border cek
        if self.xcor() < -290 or self.xcor() > 290 or \
            self.ycor() < -290 or self.ycor() > 290:
            self.goto(-1000, 1000)   
            self.status = "siap"  


class Partikel(Sprit):
    def __init__(self, spritshape, color, startx, starty):
        Sprit.__init__(self, spritshape, color, startx, starty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.goto(-1000,-1000)
        self.frame = 0

    def explode(self, startx, starty):
        self.goto(startx,starty)
        self.setheading(random.randint(0,360))
        self.frame = 1

    def move(self):
        if self.frame > 0:
            self.fd(10)
            self.frame += 1

        if self.frame > 15:
            self.frame = 0
            self.goto(-1000,-1000)
        


class Gim():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.nyowo = 3
        self.statistik = "Bermain"
        self.pen = turtle.Turtle()
        self.pon = turtle.Turtle()
        self.pan = turtle.Turtle()
        self.pin = turtle.Turtle()
        self.nyawa = ''.join([heart_emoji, heart_emoji, heart_emoji])
        

    def gambar_border(self):
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        

    def spill_status(self):
        if self.score < 0: self.score = 0
        self.pin.clear()
        self.pin.color("white")
        pesan = "Score: %s" %(self.score)
        self.pin.penup()
        self.pin.goto(200, 310)
        self.pin.write(pesan, font=("Arial", 16, "normal"))
        self.pin.color("black")
        
    
    def nyawa_player(self):
        self.pon.clear()
        self.pon.color("white")
        pesan = "Nyawa: "
        self.pon.penup()
        self.pon.goto(-300, 310)
        self.pon.write(pesan, font=("Arial", 16, "normal"))
        self.pon.color("red")
        poson = "%s" %(self.nyawa)
        self.pon.goto(-220, 310)
        self.pon.write(poson, font=("Arial", 16, "normal"))
        self.pon.color("black")

        
    
    def game_over(self):
        self.pan.color("white")
        pesan = "GAME OVER"
        self.pan.penup()
        self.pan.goto(-120, 0)
        self.pan.write(pesan, font=("Arial", 30, "bold"))
        pesan = "Press 'Enter' To Quit"
        self.pan.penup()
        self.pan.goto(-60, -15)
        self.pan.write(pesan, font=("Arial", 10, "normal"))
        self.pan.color("black")
    

    def you_win(self):
        pygame.mixer.music.load("Source/you-win-sequence-1-183948.mp3")
        pygame.mixer.music.play()
        self.pan.color("white")
        pesan = "YOU WIN"
        self.pan.penup()
        self.pan.goto(-90, 0)
        self.pan.write(pesan, font=("Arial", 30, "bold"))
        pesan = "Press 'Enter' To Quit"
        self.pan.penup()
        self.pan.goto(-60, -15)
        self.pan.write(pesan, font=("Arial", 10, "normal"))
        self.pan.color("black") 

    def reset_game(self):
        self.score = 0
        self.nyowo = 3
        self.statistik = "Bermain"
        self.nyawa = ''.join([heart_emoji, heart_emoji, heart_emoji])
        self.spill_status()
        self.nyawa_player()
        


# Create game object
game = Gim()

# Draw the game border
game.gambar_border()

# Show game status
game.spill_status()

# Show hearth of player
game.nyawa_player()




# Create my sprit
player = Player("triangle", "white", 0, 0)
misil = Misil("triangle", "yellow", 0, 0)

def respawn_player():
    player.showturtle()   # Menampilkan kembali pesawat
    player.goto(0, 0)     # Mengatur posisi pesawat ke posisi awal
    player.setheading(90) # Set arah pesawat kembali ke atas
    player.speed = 4      # Reset kecepatan pesawat
    player.toggle_invincibility(5)

def close_window():
    screen.bye()

def reset_game():
    game.reset_game()
    respawn_player()
    game.score = 0
    game.nyowo = 3
    game.statistik = "Bermain"
    game.nyawa = ''.join([heart_emoji, heart_emoji, heart_emoji])
    game.spill_status()
    game.nyawa_player()
    for musuh in musuhs:
        x = random.randint(-250, 250)
        y = random.randint(-250, 250)
        musuh.goto(x, y)
    for ally in allies:
        x = random.randint(-250, 250)
        y = random.randint(-250, 250)
        ally.goto(x, y)
    misil.goto(-1000, 1000)
    misil.status = "siap"
    global start
    start = 1

musuhs =[]
for i in range(6):
    musuhs.append(Musuh('circle', "red", -100, 0))

allies =[]
for i in range(6):
    allies.append(Ally("square", "blue", 100, 0))

partikels =[]
for i in range(20):
    partikels.append(Partikel("circle", "orange", 0, 0))


# keyboard bindings
turtle.onkey(player.belok_kiri, "Left")
turtle.onkey(player.belok_kanan, "Right")
turtle.onkey(player.belok_left, "a")
turtle.onkey(player.belok_right, "d")
turtle.onkey(player.akselerasi, "Up")
turtle.onkey(player.deklarasi, "Down")
turtle.onkey(player.aksel, "w")
turtle.onkey(player.deklar, "s")
turtle.onkey(misil.api, "space")
turtle.listen()



# Main game loop
while True:

    state = p.get_state()
    
    if state == vlc.State.Ended:
        p.stop()
        p.play()

    if start == 1:
        game.pan.reset()
        turtle.update()
        time.sleep(0.02)
        player.move()
        player.update_invincibility()
        misil.move()
        

        for musuh in musuhs:
            musuh.move()
            if player.is_kolisi(musuh) and not player.is_invincible:
                pygame.mixer.music.load("Source/medium-explosion-40472.mp3")
                pygame.mixer.music.play()
                player.hideturtle()
                player.speed = 0
                for partikel in partikels:
                    partikel.explode(player.xcor(), player.ycor())
                x = random.randint(-250, 250)
                y = random.randint(-250, 250)
                musuh.goto(x, y)
                game.score -= 100
                game.nyowo -= 1
                game.spill_status()
                if game.nyowo == 2:
                    game.nyawa = ''.join([heart_emoji, heart_emoji])
                    game.nyawa_player()
                    screen.ontimer(respawn_player, 1000)
                elif game.nyowo == 1:
                    game.nyawa = ''.join([heart_emoji])
                    game.nyawa_player()
                    screen.ontimer(respawn_player, 1000)
                if game.nyowo == 0: 
                    pygame.mixer.music.load("Source/game-over-arcade-6435.mp3")
                    pygame.mixer.music.play()
                    start = -1
                    # Menghentikan loop permainan jika nyawa habis


            if misil.is_kolisi(musuh):
                pygame.mixer.music.load("Source/medium-explosion-40472.mp3")
                pygame.mixer.music.play()
                x = random.randint(-250, 250)
                y = random.randint(-250, 250)
                musuh.goto(x, y)
                misil.status = "siap"
                game.score += 100
                game.spill_status()
                for partikel in partikels:
                    partikel.explode(misil.xcor(), misil.ycor())
                    

        for ally in allies:
            ally.move()
            if misil.is_kolisi(ally):
                pygame.mixer.music.load("Source/medium-explosion-40472.mp3")
                pygame.mixer.music.play()
                x = random.randint(-250, 250)
                y = random.randint(-250, 250)
                ally.goto(x, y)
                misil.status = "siap"
                game.score -= 50
                game.spill_status()
                for partikel in partikels:
                    partikel.explode(misil.xcor(), misil.ycor())


        for partikel in partikels:
            partikel.move()

        if game.score == 100:
            start = 0


    elif start == -1:
        turtle.update()
        game.nyawa = ''
        game.nyawa_player()
        game.game_over()
        game.statistik = "Game Over"
        screen.listen()
        screen.onkey(close_window, "Return")
        turtle.done()

    while start == 0:
        turtle.update()
        game.you_win()
        game.statistik = "you Win"
        screen.listen()
        screen.onkey(close_window, "Return")
        turtle.done()

    if not start:
            break
turtle.done()