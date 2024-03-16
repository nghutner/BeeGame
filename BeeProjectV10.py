#VERSION 10:


from cmu_112_graphics import *
import random
import math


class Bee:
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.target = None
        self.inventory = []
        self.impaired = False
        self.vx = 10  
        self.vy = 10
        


    def drawBee(self, app, canvas):
        canvas.create_oval(self.x-self.r, self.y-self.r,
                           self.x+self.r, self.y+self.r,
                           fill=self.color, outline = self.color)
        canvas.create_text(self.x, self.y, text = "\U0001F41D")

    def drawPollenInventory(self, app, canvas):
        if len(self.inventory) > 6:
            self.inventory.pop(0)
        count = 1
        r = 6
        cx, cy = 15, 15
        for flower in self.inventory:
            if flower.color == "white":
                canvas.create_text(cx*count, cy,text = "\U0001F924", 
                    font= "Arial 14")
            else:
                canvas.create_oval((cx*count) - r, cy - r, (cx*count) + r, 
                        cy + r, fill = flower.color, outline = flower.color)
            count += 1
 
    def drawPollenCarried(self, app, canvas):
        if len(self.inventory) > 6:
            self.inventory.pop(0)
        count = 0
        r = self.r/2
        cx, cy = self.x - r, self.y + r
        for flower in self.inventory:
            canvas.create_oval((cx+count) - r/2, cy - r/2, (cx+count) + r/2, 
                            cy + r/2, fill = flower.color, 
                            outline = flower.color)
            count += 3


    def chooseTarget(self, app):
        if self.target != None:  
            #check if already gathered, pollinated, off screen, or special:
            if (self.target.gathered or self.target in app.toRemove or 
                self.target.r > 25) or self.target.color == "white":
                self.target = None  #continue on to choose target
            else: return None  #keep the same target

        #loop thru flowers to choose target:
        leastD = app.height*2
        for flower in app.flowers:
            #if not flower.isPollinator or not flower.gathered:
            if not flower.isPollinator or not flower.gathered:
                if flower not in app.targets:
                    dx = flower.x - self.x
                    dy = flower.y - self.y
                    d = (dx**2 + dy**2)**0.5
                    if d < leastD:
                        leastD = d
                        self.target = flower
                        app.targets += [self.target]
                    

    def beeTimerFired(self, app):
        self.chooseTarget(app)
        
        if self.target == None:  #bounce in place
            self.x = self.x
            app.bounceTime = app.bounceTime + app.timerDelay
            if app.up == True:
                if app.bounceTime >= 300:
                    self.y = self.y + 1
                    app.up = False
                    app.bounceTime = 0       
            else:
                if app.bounceTime >= 300:
                    self.y = self.y - 1
                    app.up = True
                    app.bounceTime = 0
                
        else:  #move towards flower
            dx = self.target.x - self.x
            dy = self.target.y - self.y 
            self.x = self.x + (dx/self.vx)
            self.y = self.y + (dy/self.vy) 
            

class Player(Bee):

    def __init__(self, x, y, r, color):
         super().__init__(x, y, r, color)

    def playerTimerFired(self, app):
        if self.impaired == True:
            self.impair(app)
        else:
            self.color = "yellow"
            dx = app.mouseX - self.x
            dy = app.mouseY - self.y 
            self.x = self.x + (dx/self.vx)
            self.y = self.y + (dy/self.vy) 
    
    #helper function changes bee color while impaired
    def colorFlash(self, app):
        colorList = ["orange red", "cyan", "dark violet", "lawn green", "white"]
        nextColor = colorList[random.randint(0,len(colorList)-1)]
        app.colorTime = app.colorTime + app.timerDelay
        if app.colorTime >= 200:
            self.color = nextColor
            app.colorTime = 0
    
    #changes impaired bee movement and calls colorFlash function
    def impair(self, app):
        app.impairedTime = (app.impairedTime + app.timerDelay)
        if app.impairedTime > 6000:
            app.impairedTime = 0 
            self.impaired = False 
        self.color = "cyan"
        self.colorFlash(app)
        dx = app.mouseX - self.x
        dy = app.mouseY - self.y 
        self.x = self.x + (dx/40)   
        self.y = self.y + (dy/20) 
       


        
class Flower:
    def __init__(self, x, y, r, isPollinator, color, gathered):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.isPollinator = isPollinator
        self.gathered = gathered
        

    def drawFlower(self, app, canvas):
        if self.color == "white":
            canvas.create_oval(self.x-self.r, self.y-self.r,
                           self.x+self.r, self.y+self.r,
                           fill=self.color, outline = "dark green", width = 8)
            canvas.create_text(self.x, self.y, text = "\U0001F343", 
                            font= "Arial 16")
        else:
            if self.gathered:
                canvas.create_oval(self.x-self.r, self.y-self.r,
                            self.x+self.r, self.y+self.r,
                            fill=self.color, outline = self.color, width = 3) 
            elif self.isPollinator:
                canvas.create_oval(self.x-self.r, self.y-self.r,
                            self.x+self.r, self.y+self.r,
                            fill=self.color, outline = self.color, width = 3)
                canvas.create_text(self.x, self.y, text = "\U0001F33C",
                                    font= "Arial 14") 
               
            else:
                canvas.create_oval(self.x-self.r, self.y-self.r,
                            self.x+self.r, self.y+self.r,
                            fill=self.color, outline = self.color, width = 3)
                canvas.create_oval(self.x-(self.r/2), self.y-(self.r/2),
                            self.x+(self.r/2), self.y+(self.r/2),
                            fill=self.color, outline = "cornflower blue",
                            width = 5)


    def flowerTimerFired(self, app):
        if self.color == "white":
            if self.y + self.r < 0:
                app.toRemove += [self]   
            self.y = self.y - 6
            #wobble:
            self.x = self.x + 50*(math.sin(400 * self.y))
        
        else:
            if self.y + self.r < 0:
                app.toRemove += [self]   
            self.y = self.y - 6
            #wobble:
            self.x = self.x + 2*(math.sin(400 * self.y))
    
def drawInstructions(app, canvas):
    if app.timer > 0:
        canvas.create_text(app.width/2, app.height/2, 
                            text= "Don't worry, Bee Happy \U0001F603",
                            font='Tahoma 30 bold', fill='LightGoldenrod1')
        canvas.create_text(app.width/2, app.height/2 + 50, 
        text= ("Collect pollen from solid flowers,"),
                            font='Tahoma 15 bold', fill='dark green')
        canvas.create_text(app.width/2, app.height/2 + 70, 
        text= ("Pollinate ringed flowers with matching colored pollen,"),
                            font='Tahoma 15 bold', fill='dark green')
        canvas.create_text(app.width/2, app.height/2 + 90, 
        text= ("And help save the environment!"),
                            font='Tahoma 15 bold', fill='dark green')
        canvas.create_text(app.width/2, app.height/2 + 130, 
        text=("Just remember... special flowers will slow you down \U0001F440"),
                font='Tahoma 9 italic', fill='LightGoldenrod1')
    else:
        canvas.create_text(app.width/2, app.height/2, 
                        text= f'You pollinated {app.score} flowers!',
                        font='Tahoma 30 bold', fill='LightGoldenrod1')

def drawScore(app, canvas):
    canvas.create_text(app.width - 100, 10, 
                        text= f'Score: {app.score}',
                        font='Tahoma 10 bold', fill='LightGoldenrod1')

def drawTimer(app, canvas):
    if app.timer > 0: 
        canvas.create_text(app.width - 40, 10, 
                        text= f'Timer: {app.timer}',
                        font='Tahoma 10 bold', fill='red')
   
    
  
def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, 
                        fill='cornflower blue', outline = "cornflower blue")
    drawInstructions(app, canvas)
    if app.timer > 0:
        for flower in app.flowers:
            flower.drawFlower(app, canvas)
        for bee in app.bees:
            bee.drawBee(app, canvas)
            bee.drawPollenCarried(app, canvas)
            if isinstance(bee, Player):   #only draw the player's inventory
                bee.drawPollenInventory(app, canvas) 
        drawScore(app, canvas)
        drawTimer(app, canvas)
   
    
    

def appStarted(app):
    app.helper1 = Bee(app.width/3, app.height/2 - 30, 10, "white")
    app.helper2 = Bee((app.width/3)*2, app.height/2 - 30, 10 , "white")
    app.player = Player(app.width/2, app.height/2, 12 , "yellow")
    app.bees = [app.helper1,app.helper2, app.player]
    app.mouseX = app.width/2
    app.mouseY = app.height/2
    app.flowers = []
    app.flowerSpawnTime = 0
    app.specialSpawnTime = 0
    app.impairedTime = 0
    app.colorTime = 0
    app.bounceTime = 0
    app.instructionsTime = 0
    app.toRemove = []
    app.targets = []
    app.up = True
    app.bounceTime = 0
    app.score = 0
    app.timer = 600
    
    

def mouseMoved(app, event):
    app.mouseX = event.x
    app.mouseY = event.y

def newFlowers(app):
    app.flowerSpawnTime = app.flowerSpawnTime + app.timerDelay
    if app.flowerSpawnTime >= 1500:
        colorList = ["orchid1", "spring green", "medium orchid", 
                        "coral", "medium blue"]
        flowerR = random.randint(10, 25)
        flowerX = random.randint(10, app.width-10)
        flowerY = app.height + (flowerR*2)
        flowerC = colorList[random.randint(0,4)]
        newFlower = Flower(flowerX, flowerY, flowerR, 
                            random.randint(0,1), flowerC, 0)
        app.flowers += [newFlower]
        app.flowerSpawnTime = 0
    app.specialSpawnTime = app.specialSpawnTime + app.timerDelay
    if app.specialSpawnTime >= 6000:
        flowerR = 25
        flowerX = random.randint(0, app.width/2)
        flowerY = app.height + (flowerR*2)
        app.flowers += [Flower(flowerX, flowerY, flowerR, 1, "white", 0)]
        app.specialSpawnTime = 0

def removeFlowers(app):
    for flower in app.toRemove:
        if flower in app.flowers:
            app.flowers.remove(flower)   


def timerFired(app):
    if app.timer > 0:
        app.timer -= 1  
        app.helper1.beeTimerFired(app)
        app.helper2.beeTimerFired(app)
        app.player.playerTimerFired(app)
        newFlowers(app)
        for flower in app.flowers:
                    flower.flowerTimerFired(app)
                    for bee in app.bees:
                        if ((abs(bee.x - flower.x) <= flower.r ) and 
                            (abs(bee.y - flower.y) <= flower.r )):
                            if flower.isPollinator:  #check if pollinator
                                if flower.gathered == False: #Check ungathered
                                    
                                    #helper bees are not affected 
                                    #by special flower:
                                    if (flower.color == "white" and 
                                        not isinstance(bee, Player)):
                                        continue

                                    elif (flower.color == "white" and
                                        isinstance(bee,Player)):
                                        bee.impaired = True
                                        bee.inventory += [flower]
                                        app.toRemove += [flower] 
                                        
                                    else: #normal flowers
                                        bee.inventory += [flower]#collect pollen
                                        flower.gathered = True

                            else: #pollinate the flower
                                for f in bee.inventory: #check for matching 
                                    if f.color == flower.color:
                                        app.score += 1
                                        while flower.r < 40:#grow target flower
                                            flower.r += 20  
                                        while f.r < 40:  #grow original flower
                                            f.r += 20

                                        #remove oldest matching pollen
                                        bee.inventory.remove(f)                     
        removeFlowers(app)  
    else: return None #game over when timer hits 0          
  





    
runApp(width=500, height=500)
