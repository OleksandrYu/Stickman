from tkinter import *
import random
import time

class Game :
    def __init__ (self):
        self.tk = Tk()
        self.tk.title("Stickman")
        self.tk.resizable(0,0)
        self.tk.wm_attributes("-topmost",1) # Make window over others
        self.canvas = Canvas(self.tk , width =500 ,height =500,highlightthickness = 0)
        self.canvas.pack()
        self.tk.update()
        self.canvas_height = 500
        self.canvas_width = 500
        self.bg = PhotoImage(file = "background.gif")
        self.bg2 = PhotoImage(file = "background2.gif")
        self.bg3 = PhotoImage(file = "background3.gif")
        self.bg4 = PhotoImage(file = "background4.gif")
        self.bg5 = PhotoImage(file = "background5.gif")
        self.bg6 = PhotoImage(file = "background6.gif")

        current_bg = [[self.bg,self.bg2],[self.bg3,self.bg4],[self.bg5,self.bg6]]
        random.shuffle(current_bg)
        
        w= self.bg.width()
        h= self.bg.height()
        for x in range (0,5,2):       # Cycle that fill background by columns
            for y in range (0,5,2):
                self.canvas.create_image(x*w,y*h,image = current_bg[1][0] , anchor = "nw")#1,3,5 column var1
        for x in range (1,6,2):
            for y in range (1,6,2):
               self.canvas.create_image(x*w,y*h,image = current_bg[1][0] , anchor = "nw") #2,4 column var1
        for x in range (0,5,2):       
            for y in range (1,6,2):
                self.canvas.create_image(x*w,y*h,image = current_bg[1][1] , anchor = "nw")#1,3,5    var2
        for x in range (1,6,2):
            for y in range (0,5,2):
               self.canvas.create_image(x*w,y*h,image = current_bg[1][1] , anchor = "nw") #2,4    var2
        self.sprites = []
        self.running = True
    def mainloop (self):
        while 1 :
            if self.running == True :
                for sprite in self.sprites :
                    sprite.move()
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)
class Sprite :
    def __init__ (self,game):
        self.game = game
        self.endgame = False
        self.coordinates = None
    def move(self):
        pass
    def coords (self):
        return self.coordinates
class PlatformSprite(Sprite):
    def __init__ (self,game,photo_image, x, y ,width , height ):
        Sprite.__init__(self,game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x,y,image = self.photo_image,anchor = "nw")
        self.coordinates = Coords(x,y,x + width , y + height)
class StickFigureSprite (Sprite):
    def __init__(self,game):
        Sprite.__init__(self,game)
        self.images_left = [
            PhotoImage(file = "figure-L1.gif"),
            PhotoImage(file = "figure-L2.gif"),
            PhotoImage(file = "figure-L3.gif")
            ]
        self.images_right = [
            PhotoImage(file = "figure-R1.gif"),
            PhotoImage(file = "figure-R2.gif"),
            PhotoImage(file = "figure-R3.gif")
            ]
        self.image= game.canvas.create_image(200,470,image=self.images_left[0],anchor = "nw")
        self.x = -2
        self.y = 0
        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates= Coords()
        game.canvas.bind_all("<KeyPress-Left>",self.turn_left)
        game.canvas.bind_all("<KeyPress-Right>",self.turn_right)
        game.canvas.bind_all("<space>",self.jump)
    def turn_left (self,evt):
        if self.y == 0 :
            self.x = -2
            print(self.x)#!!!!!!!!!!!!!!!!!!!!!!!
    def turn_right (self,evt):
        if self.y == 0:
            self.x = 2
            print(self.x)#!!!!!!!!!!!!!!!!!!!!!!!
    def jump (self,evt):
        if self.y == 0 :
            self.y = -4
            print(self.y)#!!!!!!!!!!!!!!!!!!!!!!!
            self.jump_count = 0
    def change_of_pictures (self):
        if self.x < 0 :
            self.images_to_use = self.images_left
        elif self.x > 0 :
            self.images_to_use = self.images_right

        if self.y != 0 :
            self.game.canvas.itemconfig(self.image ,
                   image = self.images_to_use[2])
        else:    
            self.game.canvas.itemconfig(self.image ,
                  image = self.images_to_use[self.current_image]) # Version 2
    def animate (self) :
        if self.x != 0 and self.y == 0 :
            if time.time() - self.last_time > 0.1 :
                self.last_time = time.time()
                self.current_image += self.current_image_add
                if self.current_image >=2:
                    self.current_image_add = -1
                if self.current_image <=0:
                    self.current_image_add = 1
        self.change_of_pictures()
    
    def coords (self):
        xy = self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy [0]
        self.coordinates.y2 = xy [1]
        self.coordinates.x2 = xy [0] + 27
        self.coordinates.y2 = xy [1] + 30
        return self.coordinates
    def move (self):
        self.animate()
        if self.y < 0 :
            self.jump_count += 1
            if self.jump_count > 20 :
                self.y = 4
        if self.y > 0 :
            self.jump_count -=1
        co = self.coords()
        left = True
        right = True
        top = True
        bottom = True
        falling = True
        if self.y > 0 and co.y2 >= self.game.canvas_heigth:
            self.y = 0
            bottom = False
        elif self.y < 0 and co.y1 <= 0:
            self.y = 0
            top = False
        if self.x > 0  and co.x2 >= self.game.canvas_width:
            self.x = 0
            right = False
        elif self.x < 0 and co.x1 <= 0:
            self.x = 0
            left = False
        for sprite in self.game.sprites : # This cycle check every sprite in list (in turn) 
            if sprite == self : # if sprite is stickman
                continue # skip all next code and turn next obj in list
            sprite_co = sprite.coords()
            # Next code check colission with edges 
            if top and self.y < 0 and collided_top(co,sprite_co) : # if 1) stickman hasn`t hited top yet 2)he is jumping 3)his top has hitted with other sprite - return true
                self.y = -self.y
                top =  False
            if bottom and self.y > 0 and collided_bottom(self.y,co,sprite_co) :
                self.y = sprite_co.y1 - co.y2 # check if there is a distance between player and sprite 
                if self.y < 0 :
                    self.y = 0
                bottom = False
                top = False
            if bottom and falling and self.y == 0 and co.y2 < self.game.canvas_height and collided_bottom (1,co,sprite_co):
                falling = False
            if left and self.x < 0 and collided_left(co , sprite_co) :
                self.x = 0
                left = False
            if right and self.x > 0 and collided_right(co , sprite_co) :
                self.x = 0
                right= False
        if falling and bottom and self.y == 0 and co.y2 <self.game.canvas_height :
            self.y = 4
            self.game.canvas.move(self.image,self.x,self.y)
        
class Coords :
    def __init__ (self,x1=0,y1=0,x2=0,y2=0):
        self.x1=x1 # Parametr assighn to variable
        self.y1=y1
        self.x2=x2
        self.y2=y2
        
def within_x (co1,co2) :                     # +
    if co1.x1 > co2.x1 and co1.x1 < co2.x2:
        return True
    elif co1.x2 > co2.x1 and co1.x2 < co2.x2:
        return True
    elif co2.x1 >co1.x1 and co2.x1 < co1.x2 :
        return True
    elif co2.x2 >co1.x1 and co2.x2 < co1.x2 :
        return True
    else :
        return False
def within_y (co1,co2):
    if (co1.y1 > co2.y1 and co1.y1 < co2.y2) \
       or(co1.y2 > co2.y1 and co1.y2 < co2.y2) \
       or(co2.y1 > co1.y1 and co2.y1 < co1.y2) \
       or(co2.y2 > co1.y1 and co2.y2 < co1.y2):
        return True
    else :
        return False
def collided_left (co1,co2):   #+
    if within_y(co1,co2) :
        if co1.x1 <= co2.x2 and co1.x1 >= co2.x1:  
            return True
    return False
def collided_right (co1,co2):   #+
    if within_y(co1,co2) :
        if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
            return True
    return False
def collided_top (co1,co2):   #+
    if within_x(co1,co2) :
        if co1.y1 <= co2.y2 and co1.y1 >= co2.y1:
            return True
    return False
def collided_bottom (y,co1,co2):   #+
    if within_x (co1,co2) :
        y_calc = co1.y2 + y # check if stickman can fall 
        if y_calc >= co2.y1 and y_calc <= co2.y2 :
            return True
    return False                                       


g = Game()
platform1 = PlatformSprite(g,PhotoImage(file = "platform1.gif"),0,480,100,10)
platform2 = PlatformSprite(g,PhotoImage(file = "platform1.gif"),150,440,100,10)
platform3 = PlatformSprite(g,PhotoImage(file = "platform1.gif"),300,400,100,10)
platform4 = PlatformSprite(g,PhotoImage(file = "platform1.gif"),300,160,100,10)
platform5 = PlatformSprite(g,PhotoImage(file = "platform2.gif"),175,350,66,10)
platform6 = PlatformSprite(g,PhotoImage(file = "platform2.gif"),50,300,66,10)
platform7 = PlatformSprite(g,PhotoImage(file = "platform2.gif"),170,120,66,10)
platform8 = PlatformSprite(g,PhotoImage(file = "platform2.gif"),45,60,66,10)
platform9 = PlatformSprite(g,PhotoImage(file = "platform3.gif"),170,250,32,10)
platform10 = PlatformSprite(g,PhotoImage(file = "platform3.gif"),230,200,32,10)
g.sprites.append(platform1)
g.sprites.append(platform2)
g.sprites.append(platform3)
g.sprites.append(platform4)
g.sprites.append(platform5)
g.sprites.append(platform6)
g.sprites.append(platform7)
g.sprites.append(platform8)
g.sprites.append(platform9)
g.sprites.append(platform10)
sf = StickFigureSprite(g)
g.sprites.append(sf)
g.mainloop()

