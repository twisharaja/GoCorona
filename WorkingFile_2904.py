#################################################

# Name: Twisha Raja
# Andrew id: traja

#################################################

from cmu_112_graphics import *
from tkinter import *
import random

#CITATION- (used for reference): https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

#################################################

# Display Screen when application loads
class SplashScreenMode(Mode):
    def appStarted(mode):
        
        mode.image2 = mode.loadImage('v1.png')
        mode.image2 = mode.scaleImage(mode.image2, 1/2 )

    def redrawAll(mode, canvas):
        f = open("highscore.txt", "r")
        for i in f: score = i
        f.close()
        canvas.create_rectangle(0,0,mode.width, mode.height, fill='black')
        canvas.create_text(mode.width/2, 150, text='Go Corona!', font='fixedsys 60 bold', fill='white')
        canvas.create_text(mode.width/2, 670, text ='Press any key to start playing', font = 'fixedsys 15 bold', fill='white')
        canvas.create_text(mode.width/2, 770, font='fixedsys 30 bold', text = f'Highscore = {score}', fill ='white') 
        canvas.create_text(mode.width/2, 200, font='fixedsys 30 bold', text = 'Make the Virus Survive!', fill ='white')
        canvas.create_image(mode.width/2, 450, image =ImageTk.PhotoImage(mode.image2))

    # Start Game Mode when any key is pressed
    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)

# Display screen for the Gaming mode
class GameMode(Mode):
    def appStarted(mode):
        mode.rows = 12
        mode.cols = 12
        mode.margin = 40
        mode.currScore = 0
        mode.highScore = 0
        mode.level = 1
        mode.timerCounter = 0
        
        # Game Mode widget images
        mode.image2 = mode.loadImage('vaccine.png')
        mode.image2 = mode.scaleImage(mode.image2, 1/6)

        mode.image7 = mode.loadImage('man1.png')
        mode.image7 = mode.scaleImage(mode.image7, 1/3.5)

        mode.image8 = mode.loadImage('man2.png')
        mode.image8 = mode.scaleImage(mode.image8, 1/3.5)

        mode.image9 = mode.loadImage('man3.png')
        mode.image9 = mode.scaleImage(mode.image9, 1/3.5)

        mode.image10 = mode.loadImage('man4.png')
        mode.image10 = mode.scaleImage(mode.image10, 1/3.5)

        mode.image11 = mode.loadImage('man5.png')
        mode.image11 = mode.scaleImage(mode.image11, 1/3.5)

        mode.image12 = mode.loadImage('man6.png')
        mode.image12 = mode.scaleImage(mode.image12, 1/3.5)

        mode.image13 = mode.loadImage('doctor.png')
        mode.image13 = mode.scaleImage(mode.image13, 1/6)

        mode.image14 = mode.loadImage('sanitizer.png')
        mode.image14 = mode.scaleImage(mode.image14, 1/6)

        mode.image15 = mode.loadImage('soap.png')
        mode.image15 = mode.scaleImage(mode.image15, 1/6)

        mode.image16 = mode.loadImage('mask.png')
        mode.image16 = mode.scaleImage(mode.image16, 1/6)

        # To make a list of people images to display randomly
        mode.manImageList = [mode.image7, mode.image8, mode.image9, mode.image10, mode.image11, mode.image12]

        # To make a list of danger images to display randomly
        mode.dangerImageList = [mode.image13, mode.image14, mode.image15, mode.image16]

        #initial coordinates of frog
        mode.frog = (11,6)
        
        #initial coordinates of cars
        mode.car = { 0:{ "coords":[(8,0), (8,1),(8,2)] },   #8
                    1: { "coords":[(10,3),(10,4)] },        #10
                    2: { "coords":[(8,6), (8,7)] },         #8
                    3: { "coords":[(10,7)] },               #10
                    4: { "coords":[(9,9), (9,10), (9,11)]}, #9
                    5: { "coords": [(7,7),(7,8)]},          #7
                    6: { "coords": [(8,2)]},                #8
                    7: { "coords": [(7,3)]} }               #7

        #coordinates of river
        mode.river = { 0:{"coords":[(2,0), (2,1),(2,2),(2,3),(2,4),(2,5),(2,6),
                                 (2,7), (2,8),(2,9),(2,10),(2,11)]},
                      1:{"coords":[(3,0), (3,1),(3,2),(3,3),(3,4),(3,5),(3,6),
                                 (3,7), (3,8),(3,9),(3,10),(3,11)]},
                      2:{"coords":[(4,0), (4,1),(4,2),(4,3),(4,4),(4,5),(4,6),
                                 (4,7), (4,8),(4,9),(4,10),(4,11)]} }

        #coordinates of logs
        mode.log = { 0: {"coords":[(2,0), (2,1), (2,2), (2,3)]}, 
                    1: {"coords":[(3,3), (3,4)]},
                    2: {"coords":[(4,3), (4,4), (4,5)]},
                    3: {"coords":[(3,0), (3,1)]},
                    4: {"coords":[(4,9), (4,10)]} }
        
        #coordinates of vaccine
        mode.vaccine = (11,5)

        #list to store coordinates where frog will die
        mode.hotspots = []
        for i in list(mode.river.values()):
            for j in i['coords']:
                mode.hotspots.append(j)

        #remove log coordinates from hotspots
        for i in list(mode.log.values()):
            for j in i['coords']:
                mode.hotspots.remove(j)

        #add car coordinates to hotspots
        for i in list(mode.car.values()):
            for j in i['coords']:
                mode.hotspots.append(j)

        mode.direction = (0, +1) #drow, dcol
        mode.score = 0
        mode.gameOver = False

        # To make virus GIF
        spritestrip = mode.loadImage('virus sprite.png')
        mode.sprites = [ ]
        for i in range(4):
            sprite = spritestrip.crop((530*i, 0, 530+530*i, 536))
            sprite = mode.scaleImage(sprite, 1/9)
            mode.sprites.append(sprite)
        mode.spriteCounter = 0

    #To calculate actual cooridnates of cell
    def getCellBounds(mode, row, col):
        gridWidth  = mode.width - 2*mode.margin
        gridHeight = mode.height - 2*mode.margin
        x0 = mode.margin + gridWidth * col / mode.cols
        x1 = mode.margin + gridWidth * (col+1) / mode.cols
        y0 = mode.margin + gridHeight * row / mode.rows
        y1 = mode.margin + gridHeight * (row+1) / mode.rows
        return (x0, y0, x1, y1)

    # variables to reset when a new games starts
    def restartGame(mode, levelUp=False):
        mode.frog = (11,6)
        mode.gameOver = False
        mode.vaccine = (11,5)
        mode.timerCounter = 0
        if levelUp==True:
            mode.level += 1
            mode.app.timerDelay -= 200
        else:
            mode.currScore = 0
        GameMode()

    def keyPressed(mode, event):
        if event.key == 'p' or event.key == 'P':
            mode.app.setActiveMode(mode.app.pauseMode)

        if mode.gameOver == True:
            if (event.key == 'y' or event.key == 'Y'):
                if(mode.frog[0]==0):
                    mode.restartGame(True)
                else:
                    mode.restartGame()
            # If you press no, you exit the application
            if (event.key == 'n' or event.key == 'N'):
                exit()
                
        # when frog in not in the finisting row key events will update frog position
        elif (mode.frog[0]!=0):
            if (event.key == 'Up'): 
                mode.direction = (-1, 0)
                mode.currScore += 1
                mode.moveFrog()
            elif (event.key == 'Down'):
                mode.direction = (+1, 0)
                mode.moveFrog()
            elif (event.key == 'Left'): 
                mode.direction = (0, -1)
                mode.moveFrog()
            elif (event.key == 'Right'): 
                mode.direction = (0, +1)
                mode.moveFrog()

    def moveFrog(mode):
        (drow, dcol) = mode.direction
        (frogRow, frogCol) = mode.frog
        (newRow, newCol) = (frogRow + drow, frogCol + dcol)
        if ((newRow >= 0) and (newRow < mode.rows) and
            (newCol >= 0) and (newCol < mode.cols)):
            mode.frog=(newRow, newCol)

        if (mode.frog in mode.hotspots) or mode.frog[0] == 0:
            mode.gameOver = True

    # moves alternate cars in opposite direction
    def moveCar(mode, i):
        if i % 2 == 0:
            (row, col) = mode.car[i]["coords"][0]

            # wrap car coordinates
            if (col-1 < 0):
                col = mode.cols

            # to display moving car, we add next to the car list and remove the last coordinate
            mode.car[i]["coords"].insert(0,(row,col-1))
            mode.hotspots.append((row,col-1))

            remove = mode.car[i]["coords"].pop()
            mode.hotspots.remove(remove)
        else:
            (row, col) = mode.car[i]["coords"][-1]
            
            if (col+1 >= mode.cols):
                col = -1
            mode.car[i]["coords"].append((row,col+1))
            mode.hotspots.append((row,col+1))

            if mode.frog in mode.car[i]["coords"]:
                    mode.gameOver = True

            remove = mode.car[i]["coords"].pop(0)
            mode.hotspots.remove(remove)

    # moves alternate logs in opposite direction
    def moveLog(mode, i):
        if i%2 == 0:
            (row, col) = mode.log[i]["coords"][0]

            if (col-1 < 0):
                col = mode.cols

            mode.log[i]["coords"].insert(0,(row, col-1))
            mode.hotspots.remove((row, col-1))

            # To move frog with log if frog on log 
            if mode.frog in mode.log[i]["coords"]:
                mode.direction = (0, -1)
                mode.moveFrog()

            if (mode.frog in mode.hotspots):
                mode.gameOver = True

            remove = mode.log[i]["coords"].pop()
            mode.hotspots.append(remove)
        else:
            (row, col) = mode.log[i]["coords"][-1]

            if (col+1 >= mode.cols):
                col = -1

            mode.log[i]["coords"].append((row, col+1))
            mode.hotspots.remove((row,col+1))
            if mode.frog in mode.log[i]["coords"]:
                mode.direction = (0, +1)
                mode.moveFrog()
            if (mode.frog in mode.hotspots):
                mode.gameOver = True

            remove = mode.log[i]["coords"].pop(0)
            mode.hotspots.append(remove)
            
    def moveVaccine(mode):
        (drow, dcol) = mode.direction
        (vaccineRow, vaccineCol) = mode.vaccine
        
        (newRow, newCol) = (vaccineRow + drow, mode.frog[1] + dcol)
        
        if ((newRow >= 0) and (newRow < mode.rows) and
            (newCol >= 0) and (newCol < mode.cols)):
            mode.vaccine=(newRow, newCol)

        if (mode.vaccine == mode.frog):
            mode.gameOver = True

    def timerFired(mode):
        mode.timerCounter += 1
        # To start chasing frog when user moves one step forward
        if(mode.frog[0] < 11 and mode.timerCounter % 2 == 0):
            mode.moveVaccine()

        mode.spriteCounter = (1 + mode.spriteCounter) % len(mode.sprites)
        
        if (mode.frog in mode.hotspots):
            mode.gameOver = True
        if mode.gameOver: return

        for i in range(len(mode.car)):
            mode.moveCar(i)

        for i in range(len(mode.log)):
            mode.moveLog(i)

    # To save high scores locally to retain after closing program
    def calcHighScore(mode, currScore):
        f = open("highscore.txt", "r")
        for i in f: score = i
        f.close()
        if(currScore > int(score)):
            with open("highscore.txt", "w") as f1:
                f1.write(str(currScore))
            f1.close()
            canvas.create_text(mode.width/6.5, 780, font='fixedsys 13 bold', text = f'Highscore = {mode.highScore}', fill ='Tomato')
            return currScore
        else:
            return int(score)

    # To draw River widget on game screen
    def drawRiver(mode, canvas):
        for i in mode.river.keys():
            for coords in (mode.river[i]["coords"]):
                (row, col) = coords
                (x0, y0, x1, y1) = mode.getCellBounds(row, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill = '', outline = "dimGray")

    # To draw car widgets on game screen
    def drawCar(mode, canvas):
        for i in mode.car.keys():
            for coords in (mode.car[i]["coords"]):
                (row, col) = coords
                (x0, y0, x1, y1) = mode.getCellBounds(row, col)
                dangerImage = random.sample(mode.dangerImageList, 1)
                canvas.create_rectangle(x0, y0, x1, y1, fill = '', outline = "dimGray")
                canvas.create_image(70 + col*60, 70 + row*60, image = ImageTk.PhotoImage(dangerImage[0]))

    # To draw Log widgets on game screen  
    def drawLog(mode, canvas):
        for i in mode.log.keys():
            for coords in (mode.log[i]["coords"]):
                (row, col) = coords
                (x0, y0, x1, y1) = mode.getCellBounds(row, col)
                manImage = random.sample(mode.manImageList, 1)
                canvas.create_rectangle(x0, y0, x1, y1, fill = 'Gray9', outline = "")
                canvas.create_image(70 + col*60, 70 + row*60, image = ImageTk.PhotoImage(manImage[0]))

    # To draw Background widgets on game screen
    def drawBoard(mode, canvas):
        for row in range(mode.rows):
            for col in range(mode.cols):
                (x0, y0, x1, y1) = mode.getCellBounds(row, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill='black', outline="Gray15")
                
    # To draw chasing vaccine
    def drawVaccine(mode, canvas):
        (row, col) = mode.vaccine
        canvas.create_image(70 + col*60, 70 + row*60, image=ImageTk.PhotoImage(mode.image2))

    # To draw frog widgets on game screen
    def drawFrog(mode, canvas):
        (row, col) = mode.frog

        sprite = mode.sprites[mode.spriteCounter]
        canvas.create_image(70 + col*60, 70 + row*60, image=ImageTk.PhotoImage(sprite))

    # To display game status on game screen
    def drawGameOver(mode, canvas):
        mode.highScore = mode.calcHighScore(mode.currScore)
        if mode.currScore > mode.highScore:
            canvas.create_text(mode.width/6.5, 780, font='fixedsys 13 bold', text = f'Highscore = {mode.highScore}', fill ='Tomato')
        else:
            canvas.create_text(mode.width/6.5, 780, font='fixedsys 13 bold', text = f'Highscore = {mode.highScore}', fill ='black')
        if (mode.gameOver == True):
            # Display screen for Level Up when frog wins
            if (mode.frog[0]==0):
                # randomCountry = random.sample(mode.countryList, 1)
                canvas.create_text(mode.width/2, mode.height/2, text = 'Good Job!', font = 'fixedsys 70 bold',fill ='white')
                # canvas.create_text(mode.width/2, mode.height/1.7, text = f'You infected all people in {randomCountry}!', font = 'fixedsys 30 bold',fill ='white')
                canvas.create_text(mode.width/2, mode.height/1.5, text = 'Go to Next Level (Y/N)', font = 'fixedsys 40 bold', fill ='white')
            # Display screen for Level Up when frog dies
            else:
                canvas.create_text(mode.width/2, mode.height/2, text = 'Game Over!', font = 'fixedsys 70 bold',fill ='white')
                canvas.create_text(mode.width/2, mode.height/1.7 , text = 'Play again? (Y/N)', font = 'fixedsys 40 bold',fill ='white')
        # Display strip for footer on game screen
        canvas.create_text(mode.width/2, 20, font='fixedsys 13 bold', text = f'P = Pause ', fill ='Turquoise4')
        # canvas.create_text(mode.width/6.5, 780, font='fixedsys 13 bold', text = f'Highscore = {mode.highScore} ')
        canvas.create_text(mode.width/1.16, 780, font='fixedsys 13 bold', text = f'Your Score = {mode.currScore} ')

    def redrawAll(mode, canvas):
        mode.drawBoard(canvas)
        mode.drawRiver(canvas)
        mode.drawVaccine(canvas)
        mode.drawCar(canvas)
        mode.drawLog(canvas)
        mode.drawFrog(canvas)
        mode.drawGameOver(canvas)

# Display Screen in Pause Mode       
class PauseMode(Mode):
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0,0,mode.width, mode.height, fill='black')
        canvas.create_text(mode.width/2, mode.height/2, text ='Press any key to start playing!!', font = 'fixedsys 20 bold', fill='white')

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)

class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        app.pauseMode = PauseMode()
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay = 800

app = MyModalApp(width = 800, height = 800)