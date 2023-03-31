import datetime
from pickle import NONE, TRUE
from tabnanny import check
import pygame
import math
import sys
import numpy as np
# Initializing Pygame
pygame.init()

# Colors
CROSS_COLOR = (66, 66, 66)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BG_COLOR = (173, 255, 47)
LINE_COLOR = BLUE
CIRCLE_COLOR = RED


# Screen
print("1. 3x3")
print("2. 5x5")
N = int(input('Enter the type of board: '))    

if N == 1:
    WIDTH = 600
    ROWS = 3
    SQUARE_SIZE = 200
    LINE_WIDTH = 15
    SPACE = 55
    CIRCLE_RADIUS = 60
    CIRCLE_WIDTH = 15
    CROSS_WIDTH = 25
    
elif N == 2:
    WIDTH = 750
    ROWS = 5
    SQUARE_SIZE = 150
    LINE_WIDTH = 15
    SPACE = 40
    CIRCLE_RADIUS = 45
    CIRCLE_WIDTH = 15
    CROSS_WIDTH = 18

screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("TicTacToe")
screen.fill( WHITE )
# Fonts
END_FONT = pygame.font.SysFont('courier', 40)

def draw_lines():
    for i in range (1,ROWS):
        # horizontal
        pygame.draw.line( screen, LINE_COLOR, (0, i*SQUARE_SIZE), (WIDTH, i*SQUARE_SIZE), LINE_WIDTH )
            
        # vertical
        pygame.draw.line( screen, LINE_COLOR, (i*SQUARE_SIZE, 0), (i*SQUARE_SIZE, WIDTH), LINE_WIDTH )

def draw_figures():
    for row in range(ROWS):
        for col in range(ROWS):
            if board[row][col] == 1:
                pygame.draw.circle( screen, CIRCLE_COLOR, (int( col * SQUARE_SIZE + SQUARE_SIZE//2 ), int( row * SQUARE_SIZE + SQUARE_SIZE//2 )), CIRCLE_RADIUS, CIRCLE_WIDTH )
            elif board[row][col] == 2:
                pygame.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH )    
                pygame.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH )


def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    if board[row][col] == 0:
        return True
    return False

def getPossibleMove():
    PossibleMove = []
    for row in range(0, ROWS):
        for col in range(0, ROWS):
            if available_square(row, col):
                PossibleMove.append((row, col))
    return PossibleMove

def is_board_full():
    for row in range(ROWS):
        for col in range(ROWS):
            if board[row][col] == 0:
                return False

    return True

# Checking if someone has won
def check_win():

    for row in range (0,3):
        if ((board [row][0] == board[row][1] == board[row][2]) and(board [row][0] is not None)):
            # this row won
            winner = board[row][0]
            return winner
    # check for winning columns
    for col in range (0, 3):
        if (board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None):
            # this column won
            winner = board[0][col]
            return winner
    # check for diagonal winners
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        # game won diagonally left to right
        winner = board[0][0]
        return winner
        
    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        # game won diagonally right to left
        winner = board[0][2]
        return winner

    if is_board_full() == False:
        return NONE
    
    return 3
        

def min_alpha_beta(alpha, beta):
        minv = 2

        qx = None
        qy = None

        result = check_win()
        #result = is_end()

        if result == 1:
            return (-1, 0, 0)
        elif result == 2:
            return (1, 0, 0)
        elif result == 3:
            return (0, 0, 0)

        for i in range(ROWS):
            for j in range(ROWS):
                if available_square(i, j):
                    mark_square(i, j, 1)
                    (m, max_i, max_j) = max_alpha_beta(alpha, beta)
                    if m < minv:
                        minv = m
                        qx = i
                        qy = j
                    mark_square(i, j, 0)

                    if minv <= alpha:
                        return (minv, qx, qy)

                    if minv < beta:
                        beta = minv

        return (minv, qx, qy)

def max_alpha_beta(alpha, beta):
        maxv = -2
        px = None
        py = None

        result = check_win()
        #result = is_end()

        if result == 1:
            return (-1, 0, 0)
        elif result == 2:
            return (1, 0, 0)
        elif result == 3:
            return (0, 0, 0)

        for i in range(ROWS):
            for j in range(ROWS):
                 if available_square(i, j):
                    mark_square(i, j, 2)
                    (m, min_i, min_j) = min_alpha_beta(alpha, beta)
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j
                    mark_square(i, j, 0)

                    # Next two ifs in Max and Min are the only difference between regular algorithm and minimax
                    if maxv >= beta:
                        return (maxv, px, py)

                    if maxv > alpha:
                        alpha = maxv

        return (maxv, px, py)

def board_Empty():
    for row in range(ROWS):
        for col in range(ROWS):
            if (board[row][col] != 0):
                return False
    return True   

def countSame(listToBeChecked, player):
        return all(x == player for x in listToBeChecked)

def getRow(row):
    list = [board[row][0], board[row][1], board[row][2], board[row][3], board[row][4]]
    return list

def getRowBoard(row):
    List1 = [board[row][0], board[row][1], board[row][2], board[row][3]]
    List2 = [board[row][1], board[row][2], board[row][3], board[row][4]] 
    return List1, List2

def getCol(col):
    list = []
    for i in range(0, 5):
        list.append(board[i][col])
    return list

def getColBoard(col):
    List1 = []
    List2 = []  
    for i in range(0, 4):
        List1.append(board[i][col])
    for i in range(1, 5):
        List2.append(board[i][col])
    return List1, List2

def calculateLine(line):
    oSum = line.count(1)
    xSum = line.count(2)
    return oSum, xSum

def getScoreLine(line):
    score = 0
    oSum, xSum= calculateLine(line)
  
    if (oSum == 0 and xSum != 0):
        if xSum == 4:
            score += 100 ** 3
        elif xSum == 3 and line[0] == 0 and line[4] == 0: 
            score += 50 ** 3
        elif xSum == 3:
            score += 47 ** 3 
        else:
            score += (27+xSum) ** 3    
  
    if (oSum == 1 and xSum != 0):
        if xSum == 4:
            score += 65 ** 3
        elif xSum == 3 and (line[0] == 1 or line[4] == 1):
            score += 45 ** 3  
        elif xSum == 3 and (line[1] == 1 or line[2] == 1 or line[3] == 1) :
            score += 0                 
        else:
            score += (27+xSum) ** 3        
    
    if (oSum == 2 and xSum != 0):
        if xSum == 3 or xSum == 2:
            score += 0
        elif xSum == 1 and (line[1] == 1 or line[2] == 1 or line[3] == 1):
            score += 50 ** 3
        elif xSum == 1 and (line[0] == 1 or line[4] == 1):
            score += 0
        else:
            score += (27+xSum) ** 3      

    if (oSum == 3 and xSum != 0):
        if xSum == 2:
            score += 0
        elif xSum == 1 and (line[1] == 2 or line[2] == 2 or line[3] == 2):
            score += 70 ** 3
        else:
            score += -65 ** 3
        
    if (oSum == 4 and xSum != 0):
        score += -70 ** 3

    return score

def getDiagonals_Board():
    List1 = [board[0][0], board[1][1], board[2][2], board[3][3], board[4][4]]
    List2 = [board[0][4], board[1][3], board[2][2], board[3][1], board[4][0]]
    return List1, List2

def getLRD():
    List1 = [board[0][0], board[1][1], board[2][2], board[3][3]]
    List2 = [board[1][1], board[2][2], board[3][3], board[4][4]]
    return List1, List2 

def getLRTS():
    list = [board[0][1], board[1][2], board[2][3], board[3][4]]
    return list

def getLRBS():
    list = [board[1][0], board[2][1], board[3][2], board[4][3]]
    return list

def getRLD():
    List1 = [board[0][4], board[1][3], board[2][2], board[3][1]]
    List2 = [board[1][3], board[2][2], board[3][1], board[4][0]]
    return List1, List2

def getRLTS():
    list = [board[3][0], board[2][1], board[1][2], board[0][3]]
    return list

def getRLBS():
    list = [board[4][1], board[3][2], board[2][3], board[1][4]]
    return list

def checkLeftRightTopMain(position): 
    if position[0] == position[1]:
        return True
    return False
def checkRightLeftTopMain(position):
    if position[0] == 4 - position[1]:
        return True
    return False

def checkLeftRightTopSec(position):
    if position[0] == position[1] - 1:
        return True
    return False

def checkLeftRightBotSec(position):
    if position[0] - 1 == position[1]:
        return True
    return False

def checkRightLeftTopSec(position):
    List = [(0,3), (1,2) , (2,1), (3,0)]
    for pos in List:
        if pos == position:
            return True
    return False    

def checkRightLeftBotSec(position):
    List =  [(1,4), (2,3) , (3,2), (4,1)]
    for pos in List:
        if pos == position:
            return True
    return False

def getDiagionalScore(line):
    score = 0
    oSum, xSum = calculateLine(line)
    if oSum == 0 and xSum != 0:
        if xSum == 4:
            score += 30 ** 3
        elif xSum == 3:
            score += 15 ** 3
        elif xSum == 2:
            score += 10 ** 3
        else:
            score += 0
    if xSum == 0 and oSum != 0:
        if oSum == 4:
            score += -30 ** 3
        elif oSum == 3:
            score += -15 ** 3
        elif oSum == 2:
            score += -10 ** 3
        else:
            score += 0
    return score

def evaluate():
    score = 0
    for i in range(0, ROWS):
        List1 = getRow(i)
        score += getScoreLine(List1)
        List1 = getCol(i)
        score += getScoreLine(List1)
    # get all diagonals
    Diagonal1, Diagonal2 = getDiagonals_Board()
    score += getScoreLine(Diagonal1)
    score += getScoreLine(Diagonal2)

    a =getLRTS()
    b =getLRBS()
    c =getRLTS()
    d =getRLBS()
    diagonals = [ a, b, c , d]
    for i in range(0, 4):
        score += getDiagionalScore(diagonals[i])
    return score

def checkWinMinimax(player, row, col):
   #get current position + row + col
    List1, List2 = getRowBoard(row)
    if countSame(List1, player) or countSame(List2, player):
        return True
    #check win on row or col
    List1, List2 = getColBoard(col)
    if countSame(List1, player) or countSame(List2, player):
        return True
    #check win on descending main diagonal
    if checkLeftRightTopMain((row, col)):
        List1, List2 = getLRD()
        if countSame(List1, player) or countSame(List2, player):
            return True
    #check win on ascending main diagonal
    if checkRightLeftTopMain((row, col)):
        List1, List2 = getRLD()
        if countSame(List1, player) or countSame(List2, player):
            return True
    #check win on secondary main diagonal
    if checkLeftRightTopSec((row,col)):
        List = getLRTS()
        if countSame(List, player):
            return True
    if checkLeftRightBotSec((row,col)):
        List = getLRBS()
        if countSame(List, player):
            return True
    if checkRightLeftTopSec((row,col)):
        List = getRLTS()
        if countSame(List, player):
            return True
    if checkRightLeftBotSec((row,col)):            
        List = getRLBS()
        if countSame(List, player):
            return True
    return False

def checkDraw():
    if is_board_full():
        return True
    return False

def checkGameState():
    if checkWinMinimax(1, LastMove[0], LastMove[1]):
        return 1
    if checkWinMinimax(2, LastMove[0], LastMove[1]):
        return 2
    if checkDraw():
        return 0

def minimax(depth, isMax, alpha, beta, startTime, timeLimit):
    moves = getPossibleMove()
    score = evaluate()
    position = None
    TimePassed = False 

    if datetime.datetime.now() - startTime >= timeLimit:
        TimePassed = True
        result = 0

    if not moves or depth == 0 or TimePassed:
        gameResult = checkGameState()
        if gameResult == 1:
            return -10**(ROWS+1), position
        elif gameResult == 2:
            return 10**(ROWS+1), position
        elif gameResult == 0:
            return 0, position
        return score, position
    #alpha beta pruning
    if isMax:
        for pos in moves:
                mark_square(pos[0], pos[1], 2)
                score, dummy = minimax(depth-1, not isMax, alpha, beta, startTime, timeLimit)
                if score > alpha:
                    alpha = score
                    position = pos
                    BestMove = pos

                mark_square(pos[0], pos[1], 0)
                if beta <= alpha:
                    break

        return alpha, position
    else:
        for pos in moves:
            mark_square(pos[0], pos[1], 1)
            score, dummy = minimax(depth-1, not isMax, alpha, beta, startTime, timeLimit)
            if score < beta:
                beta = score
                position = pos
                BestMove = pos
            mark_square(pos[0], pos[1], 0)
            if alpha >= beta:
                break

        return beta, position


def iterativeDeepSearch():
    if board_Empty():
        position = (2, 2)
    else:
        startTime = datetime.datetime.now()
        endTime = startTime + datetime.timedelta(0, 7)
        depth = 1
        position = None
        while True:
            currentTime = datetime.datetime.now()
            if currentTime >= endTime:
                break
            best, position = minimax(depth, True, -10000000, 10000000, currentTime, endTime-currentTime)
            depth += 1

        if position is None:
                position = BestMove

    return position

def restart():
    screen.fill( BG_COLOR )
    draw_lines()
    for row in range(ROWS):
        for col in range(ROWS):
            board[row][col] = 0

def display_message(content):
    pygame.time.delay(500)
    screen.fill(WHITE)
    end_text = END_FONT.render(content, 1, BLACK)
    screen.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)

board = np.zeros((ROWS, ROWS))
player = 1
game_over = False
draw_lines()

LastMove = None
BestMove = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if player == 1:
            if event.type == pygame.MOUSEBUTTONDOWN and game_over == False:

                mouseX = event.pos[0] # x
                mouseY = event.pos[1] # y

                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_col = int(mouseX // SQUARE_SIZE)

                if available_square( clicked_row, clicked_col ):
                     ##
                    mark_square( clicked_row, clicked_col, player )
                    LastMove = (clicked_row, clicked_col)
                   
                    draw_figures()
                    if ROWS == 5:
                        result = checkGameState()
                    elif ROWS == 3:
                        result = check_win()
                    if result == player and result == 1:
                        game_over = True
                        display_message("O is winner")
                    elif result == 3:
                        game_over = True
                        display_message("It is draw")
                player = player + 1

        else:
            if game_over == False:
                if (ROWS == 5):
                    (px, py) = iterativeDeepSearch()
                    if available_square(px, py):
                        mark_square(px, py, player)

                    draw_figures()

                    result = checkGameState()
                    if checkWinMinimax(player, px, py):
                        game_over = True
                        display_message("X is winner")
                    elif checkDraw():
                        game_over = True
                        display_message("It is draw")
                elif (ROWS == 3):
                    (m,px, py) = max_alpha_beta(-2,2)
                    if available_square(px, py):
                        mark_square(px, py, player)

                    draw_figures()

                    result = check_win()
                    if result == player and result == 2:
                        game_over = True
                        display_message("X is winner")
                    elif checkDraw():
                        game_over = True
                        display_message("It is draw")
                
                player = 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                player = 1
                game_over = False

        pygame.display.update()
        print(board)