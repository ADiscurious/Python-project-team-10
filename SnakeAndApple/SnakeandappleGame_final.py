#Snake and apple game by Adil Dhawan, Shiv Joshi, Darshil Chaniyara and Ainesh Dhawan
import pygame
from pygame.locals import *
import time
import random

from tkinter.ttk import *
import tkinter as tk


root = tk.Tk()
root.title('Settings')

v = tk.IntVar()

tk.Label(root, 
        text="""CHOOSE DIFFICULTY""",
        justify = tk.LEFT,
        padx = 20).pack()

tk.Radiobutton(root, 
               text="EASY",
               padx = 20, 
               variable=v, 
               value=1).pack(anchor=tk.W)

tk.Radiobutton(root, 
               text="HARD",
               padx = 20, 
               variable=v, 
               value=2).pack(anchor=tk.W)

a = tk.IntVar()

tk.Label(root, 
        text="""CHOOSE THEME""",
        justify = tk.LEFT,
        padx = 20).pack()

tk.Radiobutton(root, 
               text="GRASSLAND",
               padx = 20, 
               variable=a, 
               value=3).pack(anchor=tk.W)

tk.Radiobutton(root, 
               text="GRAVEYARD",
               padx = 20, 
               variable=a, 
               value=4).pack(anchor=tk.W)


c= tk.IntVar()

tk.Label(root, 
        text="""CHOOSE A GAME MODE""",
        justify = tk.LEFT,
        padx = 20).pack()

tk.Radiobutton(root, 
               text="SNAKE'S SELF-COLLISION ON",
               padx = 20, 
               variable=c, 
               value=5).pack(anchor=tk.W)

tk.Radiobutton(root, 
               text="SNAKE'S SELF_COLLISION OFF",
               padx = 20, 
               variable=c, 
               value=6).pack(anchor=tk.W)

tk.Label(root, 
        text="""Warning: not choosing an option or closing this window will automatically
 select the last option in that case""",
        justify = tk.CENTER,
        padx = 20).pack()
def Close():
        root.destroy()
# Button for closing
exit_button =tk.Button(root, text="START", command=Close)
exit_button.pack(pady=20)

root.mainloop()
if (v.get() ==1):
       #print("you picked option1")
       speed=0.3      
else:
        #print("you picked option2")
        speed=0.09
        

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        if (a.get() ==3):
            #print("you picked option3")
            self.image = pygame.image.load(r"resources/apple.jpg").convert()
        else:
            #print("you picked option4")
            self.image = pygame.image.load(r"resources/apple1.jpg").convert()
        
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,21)*SIZE
        self.y = random.randint(2,16)*SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        #self.head = pygame.image.load("resources/head.jpg").convert()
        if (a.get() ==3):
            #print("you picked option3")
            self.image = pygame.image.load(r"resources/block.jpg").convert()
        else:
            #print("you picked option4")
            self.image = pygame.image.load(r"resources/block1.jpg").convert()
        
        self.direction = 'down'

        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("The Classic Snake")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play_background_music(self):
        if (a.get() ==3):
            #print("you picked option3")
            pygame.mixer.music.load(r'resources/bg_music_1.mp3')
        else:
            #print("you picked option4")
            pygame.mixer.music.load(r'resources/bg_music_2.mp3')    

        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
           if (a.get() ==3):
                sound = pygame.mixer.Sound(r"resources/crash.mp3")
           else:
                sound = pygame.mixer.Sound(r"resources/crash2.mp3")
           
        elif sound_name == 'ding':
            if (a.get() ==3):
                sound = pygame.mixer.Sound(r"resources/ding.mp3")
            else:
                sound = pygame.mixer.Sound(r"resources/score2.mp3")
            

        pygame.mixer.Sound.play(sound)
        #pygame.mixer.music.stop()


    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)


    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        if (a.get() ==3):
            #print("you picked option3")
            bg = pygame.image.load(r"resources/background.jpg")
        else:
            #print("you picked option4")
            bg = pygame.image.load(r"resources/background1.jpg")        
        
        self.surface.blit(bg, (0,0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple scenario

        for i in range(self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
                self.play_sound("ding")
                self.snake.increase_length()
                self.apple.move()
                with open(r'resources/score.txt',"r") as f:
                    global highscore
                    highscore=f.read()
                    #print(highscore)
                    if self.snake.length>int(highscore):
                        highscore=self.snake.length
                        #print(highscore)

        # snake colliding with itself
        if (c.get() ==5):      
            for i in range(3, self.snake.length):
                if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                    self.play_sound('crash')
                    if highscore != 0: #the if else stattemen is to avoid bugs...
                        with open(r'resources/score.txt',"w") as f:
                            f.write(str(highscore))
                    else:
                        with open(r'resources/score.txt',"w") as f:
                            f.write(str(highscore))
                    raise "Collision Occurred"        
        else:
            pass
            


        # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] < 1000 and 0 <= self.snake.y[0] < 800):
            self.play_sound('crash')
            if highscore != 0: #the if else stattemen is to avoid bugs...
                with open(r'resources/score.txt',"w") as f:
                    f.write(str(highscore))
            else:
                with open(r'resources/score.txt',"w") as f:
                    f.write(str(highscore))
            
            raise "Hit the boundry error"

    def display_score(self):
        font = pygame.font.Font(r'resources/arcadeclassic.ttf',42)
        score = font.render(f"SCORE {self.snake.length}",True,(42,111,160))
        self.surface.blit(score,(830,8))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.Font(r'resources/arcadeclassic.ttf', 70)
        line1 = font.render(f"Game is over!", True, (255,255,255))
        self.surface.blit(line1, (300, 300))
        line2 = font.render(f"Your score is {self.snake.length}", True, (255,255,255))
        self.surface.blit(line2, (260, 350))
        if self.snake.length>1:
            line5 = font.render(f"Your  HIGHSCORE  is {highscore}", True, (255,255,255))
            self.surface.blit(line5, (150, 250))
        else:
            pass
        line3 = font.render("To play again press Enter!", True, (255,255,255))
        self.surface.blit(line3, (50, 450))
        line4 = font.render(" To exit press Escape!", True, (255,255,255))
        self.surface.blit(line4, (110, 500))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(speed)

if __name__ == '__main__':
    game = Game()
    game.run()