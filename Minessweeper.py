import random
import tkinter as tk
import easygui

root = tk.Tk()
frame = tk.Frame(root)
frame.grid()

numOfCols = 40
numOfRows = 25
didFirstClick = False
minesToPut = 200
buttonsRemaining=0
gameOver=False

def valueAndPredAndSucc(x):
    return [x - 1, x, x + 1]


def validCoordinates(i, j):
    return 0 <= i < numOfRows and 0 <= j < numOfCols

def endGame(weWon):
    global gameOver
    gameOver=True
    if weWon:
        msg="أحسنت يا بني !"
        ttl="أنت فزت ههههه"
    else:
        msg="للأسف لقد تبهدلت !"
        ttl="أنت خسرت ههههه"
    easygui.msgbox(msg, title=ttl)


def leftClick(i, j):
    if not validCoordinates(i, j):
        return
    global didFirstClick
    if not didFirstClick:
        didFirstClick = True
        totalNumberOfButtons=numOfRows * numOfCols
        global minesToPut
        minesToPut = min(minesToPut, totalNumberOfButtons)
        global buttonsRemaining
        buttonsRemaining = totalNumberOfButtons-minesToPut
        while minesToPut > 0:
            ii = random.randint(0, numOfRows - 1)
            jj = random.randint(0, numOfCols - 1)
            if hasMine[ii][jj] or (ii == i and jj == j):
                continue
            hasMine[ii][jj] = True
            minesToPut -= 1
            for iii in valueAndPredAndSucc(ii):
                for jjj in valueAndPredAndSucc(jj):
                    increaseNumOfSurroundingMines(iii, jjj)
    if not clicked[i][j] and not marked[i][j]:
        buttons[i][j].config(state="disabled")
        clicked[i][j] = True
        global gameOver
        if hasMine[i][j]:
            buttons[i][j].config(fg="yellow", bg="red", text="X")
            if not gameOver:
                endGame(False)
            for ii in range(numOfRows):
                for jj in range(numOfCols):
                    leftClick(ii,jj)
        else:
            buttonsRemaining-=1
            if buttonsRemaining==0 and not gameOver:
                    endGame(True)
            if numberOfSurroundingMines[i][j] > 0:
                buttons[i][j].config(bg="white", text=numberOfSurroundingMines[i][j])
            else:
                buttons[i][j].config(bg="white", text="")
                for ii in valueAndPredAndSucc(i):
                    for jj in valueAndPredAndSucc(j):
                        leftClick(ii, jj)


def doubleClick(i, j):
    numOfMarkedAround = 0
    for ii in valueAndPredAndSucc(i):
        for jj in valueAndPredAndSucc(j):
            if (ii != i or jj != j) and validCoordinates(ii, jj) and marked[ii][jj]:
                #            print(ii, jj)
                numOfMarkedAround += 1
    #            print("numOfMarkedAround= ",numOfMarkedAround)

    # print("----")
    if numOfMarkedAround == numberOfSurroundingMines[i][j]:
        for ii in valueAndPredAndSucc(i):
            for jj in valueAndPredAndSucc(j):
                if validCoordinates(ii, jj) and not hasMine[ii][jj]:
                    leftClick(ii, jj)


def rightClick(i, j):
    if not clicked[i][j]:
        b = buttons[i][j]
        if marked[i][j]:
            buttons[i][j].config(state="normal", bg="grey", text="")
            marked[i][j] = False
        else:
            buttons[i][j].config(state="disabled", bg="yellow", text="H")
            marked[i][j] = True


def increaseNumOfSurroundingMines(i, j):
    if validCoordinates(i, j):
        numberOfSurroundingMines[i][j] += 1


buttons = []
clicked = []
marked = []
hasMine = []
numberOfSurroundingMines = []
for i in range(numOfRows):
    buttons.append([])
    clicked.append([])
    marked.append([])
    hasMine.append([])
    numberOfSurroundingMines.append([])
    for j in range(numOfCols):
        b = tk.Button(frame,
                      fg="black",
                      bg="grey",
                      text="")
        buttons[i].append(b)
        clicked[i].append(False)
        marked[i].append(False)
        hasMine[i].append(False)
        numberOfSurroundingMines[i].append(0)
        b.grid(row=i, column=j)
        b.config(height=1, width=2, command=lambda ii=i, jj=j: leftClick(ii, jj))
        b.bind("<Button-3>", lambda blablabla=0, ii=i, jj=j: rightClick(ii, jj))
        b.bind('<Double-Button-1>', lambda blablabla=0, ii=i, jj=j: doubleClick(ii, jj))

root.mainloop()
