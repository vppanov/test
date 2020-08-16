# # #        TO DO LIST
# 1. Update reset function when we have a player selection screen
# 2. Add player IDs + names and add match information to table
# 3. Use time to record match duration and append it to table
# 4. Prepare a page with statistics and best players for the moment
# 5. Prepare game with 11 points. Change serving and overtime
# 6. Reduce the code - move functions in another file


from time import sleep
from turtle import Screen, Turtle
from math import fabs, ceil
import sqlite3
from datetime import date
from timeit import default_timer

exec(open('system/database.py').read())  # executing database creation file

# variable for the game
count = 0
leftScore = 0
rightScore = 0
serve = None
totalLeft = 0
totalRight = 0
player1 = False
player2 = False
playerNames = ["Веско", "Сашо", "Гери", "Георги", "Ивайло", "Друг"]
player1_id = None
player2_id = None
posCount = 0
positionY = 100
positionX = -350
positionX2 = 100
positionY2 = 100
match_duration = None
DATABASE_NAME = 'system/stats.db'

# window screen set up
window = Screen()
window.title("Table tennis scoreboard")
window.bgcolor("white")
window.setup(width=1024, height=600)
window.tracer(0)

# turtle set up
pen = Turtle()
pen.speed(0)
pen.color("black")
pen.hideturtle()
pen.penup()

#  welcome messages
pen.goto(0, 150)
pen.write("Welcome to scoreboard!", align="center", font=("Arial", 60, "bold"))
pen.goto(0, -100)
pen.write("Please choose players.", align="center", font=("Arial", 60, "bold"))
sleep(5)
pen.clear()




def database_update_():
    global player2_id, player1_id, playerNames, match_duration, leftScore, rightScore
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute(
        'INSERT INTO Table_tennis_statistics (Player_1_Name, Player_2_Name, Player_1_Score, Player_2_Score, '
        'Match_duration, Date) VALUES (?, ?, ?, ?, ?, ?)', [playerNames[player1_id], playerNames[player2_id], leftScore,
                                                            rightScore, match_duration, date.today()])
    conn.commit()
    conn.close()
    return c.lastrowid


# definitions of game functions

def resetscore():
    global serve, totalLeft, totalRight, leftScore, rightScore, count
    serve = None
    totalLeft = totalRight = leftScore = rightScore = count = 0
    pen.clear()
    pen.goto(0, 220)
    pen.write("New game!", align="center", font=("Arial", 60, "bold"))
    pen.goto(0, -100)
    pen.write("Who is serving ?", align="center", font=("Arial", 60, "bold"))


def serveistrue():
    global leftScore, rightScore, totalLeft, totalRight
    pen.clear()
    pen.color("green")
    pen.write("> {} : {} ".format(leftScore, rightScore), align="center", font=("Arial", 200, "bold"))
    pen.goto(0, 220)
    pen.color("white")
    pen.write("Total score {} : {}".format(totalLeft, totalRight), align="center",
              font=("Arial", 60, "bold"))
    pen.goto(0, -100)


def serveisfalse():
    global leftScore, rightScore, totalLeft, totalRight
    pen.clear()
    pen.color("green")
    pen.write(" {} : {} <".format(leftScore, rightScore), align="center", font=("Arial", 200, "bold"))
    pen.goto(0, 220)
    pen.color("white")
    pen.write("Total score {} : {}".format(totalLeft, totalRight), align="center",
              font=("Arial", 60, "bold"))
    pen.goto(0, -100)


def servicecheck():
    global serve, count
    if count == 4:
        serve = not serve
        count = -1  # resetting the counter to negative number to handle service turn


def rightwins():
    global totalLeft, totalRight, rightScore, leftScore, count, start_game, match_duration
    totalRight += 1
    end_game = default_timer()
    match_duration_raw = end_game - start_game
    match_duration = ceil(match_duration_raw / 60)
    database_update_()
    rightScore = leftScore = count = 0
    start_game = default_timer()
    pen.goto(0, -200)
    pen.write('Right  WINS !', align="center", font=("Arial", 100, "bold"))
    pen.goto(0, -100)
    sleep(5)
    pen.clear()
    pen.color("green")
    pen.write(" {} : {} <".format(leftScore, rightScore), align="center", font=("Arial", 200, "bold"))
    pen.goto(0, 220)
    pen.color("white")
    pen.write("Total score {} : {}".format(totalLeft, totalRight), align="center", font=("Arial", 60, "bold"))
    pen.goto(0, -100)


def leftwins():
    global totalLeft, totalRight, rightScore, leftScore, count, start_game, match_duration
    totalLeft += 1
    end_game = default_timer()
    match_duration_raw = end_game - start_game
    match_duration = ceil(match_duration_raw / 60)
    database_update_()
    leftScore = rightScore = count = 0
    start_game = default_timer()
    pen.goto(0, -200)
    pen.write('Left  WINS !', align="center", font=("Arial", 100, "bold"))
    pen.goto(0, -100)
    sleep(5)
    pen.clear()
    pen.color("green")
    pen.write("> {} : {} ".format(leftScore, rightScore), align="center", font=("Arial", 200, "bold"))
    pen.goto(0, 220)
    pen.color("white")
    pen.write("Total score {} : {}".format(totalLeft, totalRight), align="center",
              font=("Arial", 60, "bold"))
    pen.goto(0, -100)


def wronginput():
    global count
    count -= 1
    pen.goto(0, 150)
    pen.write("Wrong input ", align="center", font=("Arial", 60, "bold"))
    pen.goto(0, -100)


def servingturndisplay():
    global serve, leftScore, rightScore, totalLeft, totalLeft
    if serve:
        pen.clear()
        pen.goto(0, -100)
        pen.color("green")
        pen.write("> {} : {} ".format(leftScore, rightScore), align="center", font=("Arial", 200, "bold"))
        pen.goto(0, 220)
        pen.color("white")
        pen.write("Total score {} : {}".format(totalLeft, totalRight), align="center", font=("Arial", 60, "bold"))
        pen.goto(0, -100)
    elif not serve:
        pen.clear()
        pen.goto(0, -100)
        pen.color("green")
        pen.write(" {} : {} <".format(leftScore, rightScore), align="center", font=("Arial", 200, "bold"))
        pen.goto(0, 220)
        pen.color("white")
        pen.write("Total score {} : {}".format(totalLeft, totalRight), align="center", font=("Arial", 60, "bold"))
        pen.goto(0, -100)


def printnames():
    pen.color("black")
    pen.goto(-200, 100)
    pen.write("Веско", align="center", font=("Arial", 60, "bold"))
    pen.goto(-200, 0)
    pen.write("Сашо", align="center", font=("Arial", 60, "bold"))
    pen.goto(-200, -100)
    pen.write("Гери", align="center", font=("Arial", 60, "bold"))
    pen.goto(300, 100)
    pen.write("Георги", align="center", font=("Arial", 60, "bold"))
    pen.goto(300, 0)
    pen.write("Ивайло", align="center", font=("Arial", 60, "bold"))
    pen.goto(300, -100)
    pen.write("Друг", align="center", font=("Arial", 60, "bold"))


def position():
    global positionY, positionX, positionX2, positionY2, posCount
    if posCount <= 3:
        pen.color("yellow")
        pen.begin_fill()
        pen.goto(positionX, positionY)
        pen.down()
        pen.circle(35)
        pen.end_fill()
        pen.up()
        positionY -= 100
    elif 3 < posCount <= 5:
        pen.color("yellow")
        pen.begin_fill()
        pen.goto(positionX2, positionY2)
        pen.down()
        pen.circle(35)
        pen.end_fill()
        pen.up()
        positionY2 -= 100
    elif posCount >= 6:
        pen.color("yellow")
        pen.begin_fill()
        pen.goto(positionX2, positionY2)
        pen.down()
        pen.circle(35)
        pen.end_fill()
        pen.up()
        positionY2 -= 100
        posCount = 0
        positionY = 100
        positionX = -350
        positionX2 = 100
        positionY2 = 100


def playercheck():
    global player1, player2, player1_id, player2_id
    if player1_id == player2_id:
        pen.goto(0, 200)
        pen.write("Same player selected", align="center", font=("Arial", 60, "bold"))
        printnames()
        player1 = False
        player2 = False
        player1_id = None
        player2_id = None
        sleep(3)
        pen.clear()


def setplayer(e):
    global positionY
    if 0 < posCount <= 3:
        red_position = positionY + 100
        pen.color("red")
        pen.begin_fill()
        pen.goto(positionX, red_position)
        pen.down()
        pen.circle(35)
        pen.end_fill()
        pen.up()
        pen.goto(0, 200)
        pen.write("Player selected", align="center", font=("Arial", 60, "bold"))
        e = not e
        return e
    elif 3 < posCount <= 5:
        red_position2 = positionY2 + 100
        pen.color("red")
        pen.begin_fill()
        pen.goto(positionX2, red_position2)
        pen.down()
        pen.circle(35)
        pen.end_fill()
        pen.up()
        pen.goto(0, 200)
        pen.write("Player selected", align="center", font=("Arial", 60, "bold"))
        e = not e
        return e
    elif posCount == 0:
        pen.color("red")
        pen.begin_fill()
        pen.goto(100, -100)
        pen.down()
        pen.circle(35)
        pen.end_fill()
        pen.up()
        pen.goto(0, 200)
        pen.write("Player selected", align="center", font=("Arial", 60, "bold"))
        e = not e
        return e


# game logic


while True:
    window.update()
    while player1 is not True or player2 is not True:
        printnames()
        x = input(str(input))
        if x == "n" and player1 is False:
            posCount += 1
            pen.clear()
            printnames()
            position()
        elif x == "o" and player1 is False:
            if positionY == 0:
                player1 = setplayer(player1)
                player1_id = playerNames.index("Веско")
                sleep(3)
                pen.clear()
                playercheck()
            elif positionY == -100:
                player1 = setplayer(player1)
                player1_id = playerNames.index("Сашо")
                sleep(3)
                pen.clear()
                playercheck()
            elif positionY == -200 and posCount <= 3:
                player1 = setplayer(player1)
                player1_id = playerNames.index("Гери")
                sleep(3)
                pen.clear()
                playercheck()
            elif positionY2 == 0 and posCount > 0:
                player1 = setplayer(player1)
                player1_id = playerNames.index("Георги")
                sleep(3)
                pen.clear()
                playercheck()
            elif positionY2 == -100 and posCount > 0:
                player1 = setplayer(player1)
                player1_id = playerNames.index("Ивайло")
                sleep(3)
                pen.clear()
                playercheck()
            else:
                player1 = setplayer(player1)
                player1_id = playerNames.index("Друг")
                sleep(3)
                pen.clear()
                playercheck()

        elif x == "n" and player2 is False:
            posCount += 1
            pen.clear()
            printnames()
            position()
        elif x == "o" and player2 is False:
            if positionY == 0:
                player2 = setplayer(player2)
                player2_id = playerNames.index("Веско")
                sleep(3)
                pen.clear()
                playercheck()
            elif positionY == -100:
                player2 = setplayer(player2)
                player2_id = playerNames.index("Сашо")
                sleep(3)
                pen.clear()
                playercheck()
            elif positionY == -200 and posCount <= 3:
                player2 = setplayer(player2)
                player2_id = playerNames.index("Гери")
                sleep(3)
                pen.clear()
                playercheck()
            elif positionY2 == 0 and posCount > 0:
                player2 = setplayer(player2)
                player2_id = playerNames.index("Георги")
                sleep(3)
                pen.clear()
                playercheck()
            elif positionY2 == -100 and posCount > 0:
                player2 = setplayer(player2)
                player2_id = playerNames.index("Ивайло")
                sleep(3)
                pen.clear()
                playercheck()
            else:
                player2 = setplayer(player2)
                player2_id = playerNames.index("Друг")
                sleep(3)
                pen.clear()
                playercheck()
    if player1 is True and player2 is True:
        sleep(2)
        break

window.bgcolor("black")
pen.color("white")

pen.goto(0, 0)
pen.write("Please choose serving player.", align="center", font=("Arial", 60, "bold"))
sleep(1)

start_game = default_timer()
# game logic
while leftScore <= 40 and rightScore <= 40:  # maximum points
    window.update()
    if serve is None:
        z = input(str(input))
        if z == "q":  # command to close window
            window.bye()
        elif z == "1":
            serve = True  # serving left player
            servingturndisplay()
        elif z == "2":
            serve = False  # serving right player
            servingturndisplay()
    while leftScore >= 20 and rightScore >= 20:  # handling overtime
        if serve is True:
            serve = not serve  # switching serving player to right player
        elif serve is False:
            serve = not serve  # switching serving player to left player
        count = 0
        x = input(str(input))
        count += 1
        if x == "r":  # reset result
            resetscore()
        elif x == "4":  # point for left player
            leftScore += 1
            if serve is True:
                serveistrue()
                if fabs(rightScore - leftScore) == 2:  # checking for two points difference
                    leftwins()  # game ends
                    serve = True  # assigning serve turn for next game
            elif serve is False:
                serveisfalse()
                if fabs(leftScore - rightScore) == 2:
                    leftwins()
                    serve = True  # assigning serve turn for next game
        elif x == "5":  # point for right  player
            rightScore += 1
            if serve is True:
                serveistrue()
                if fabs(leftScore - rightScore) == 2:  # checking for two points difference
                    rightwins()
                    serve = False
            elif serve is False:
                serveisfalse()
                if fabs(leftScore - rightScore) == 2:  # checking for two points difference
                    rightwins()
                    serve = False
        else:
            wronginput()  # handling wrong keyboard input
    if leftScore == 21:  # left wins
        leftwins()
    elif rightScore == 21:  # right wins
        rightwins()
    else:
        x = input(str(input))
        count += 1
        if x == "r":  # reset result
            resetscore()
        elif x == "4":  # point for left player
            leftScore += 1
            if serve is True:
                serveistrue()
                servicecheck()
            elif serve is False:
                serveisfalse()
                servicecheck()
        elif x == "5":  # point for right  player
            rightScore += 1
            if serve is True:
                serveistrue()
                servicecheck()
            elif serve is False:
                serveisfalse()
                servicecheck()
        elif x == "q":  # close program
            window.bye()
        else:
            wronginput()  # handling wrong keyboard input