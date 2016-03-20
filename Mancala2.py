'''
Created on 19-okt.-2015

@author: thomas
'''

''' programming plan:

- AI: Monte Carlo Tree Search 

---> change the "lists" of the state into "tuples"

- positioning of seeds: more spread across the bin and kalaha, and not overlapping

'''


import datetime
import math
import pygame
import pygame.gfxdraw
import random
import sys
import time

from pygame.locals import *
#from ai.boardgame import *

WINDOWWIDTH = 1024
WINDOWHEIGHT = 520
FPS = 30
COMPUTERPAUSE = 1.5

FONTSIZE = 21

#         R    G    B
WHITE  = (255, 255, 255)
BLACK  = (  0,   0,   0)
GREY   = ( 64,  64,  64)
#ORANGE = (255, 128,   0)
ORANGE = (192, 96, 0) 
RED    = (192,   0,   0)

PLAYER = 'Player'
COMPUTER = 'Computer'

P = [PLAYER, COMPUTER]
PCOLOR = [BLACK, BLACK]
BGCOLOR = ORANGE
HIGHLIGHT = RED

BIGRADIUS = 60
SMALLRADIUS = 50
INNERMARGIN = 20
SEEDSIZE = 8

BOARDWIDTH = 6 * (SMALLRADIUS * 2) + 2 * (2 * BIGRADIUS) + INNERMARGIN * 7
BOARDHEIGHT = 2 * (2 * SMALLRADIUS) + INNERMARGIN

XMARGIN = (WINDOWWIDTH - BOARDWIDTH) // 2
YMARGIN = (WINDOWHEIGHT - BOARDHEIGHT) // 2 

#AIDEPTH = 6

TOTALSEEDS = 36



''' board representation as an tuple of tuples
    board.state = ((7 elementen), (7 elementen))
    first index is the player
    second index: the first 6 (0-5) are the bins and how many seeds they contain
        the last, index 6 is the kalaha

           (1, 5) (1, 4) (1, 3) (1, 2) (1, 1) (1, 0) 
    (1, 6)                                           (0, 6)
           (0, 0) (0, 1) (0, 2) (0, 3) (0, 4) (0, 5)        
          
'''


class Board(object):
    def __init__(self):
        self.extraTurn = False
        #self.winner = None
        self.state, self.coord = getStartingBoard()
        self.currentPlayer = random.randint(0, 1)
        
    def __repr__(self):
        s = P[0][0] +': '+ str(self.state[0]) +'; '+ P[1][0] + ': '+ str(self.state[1])
        return s

    
    def changePlayer(self):
        self.currentPlayer = 1 - self.currentPlayer
        
    
    def endScore(self):
        for i in range(2):
            for j in range(6):
                self.state[i][6] += self.state[i][j]
                self.state[i][j] = 0
                self.coord[(i, j)] = []
        
        if self.state[0][6] > self.state[1][6]:
            self.winner = 0
        elif self.state[0][6] < self.state[1][6]:
            self.winner = 1

        
    def getAvailableMoves(self, gameState=None, player=None):
        if gameState is None:
            gs = self.state
        else:
            gs = gameState
        if player is None:
            p = self.currentPlayer
        else:
            p = player
        moves = []
        for j in range(6):
            if gs[p][j] > 0:
                moves.append((p, j))
        return moves
    
        
    def getOtherPlayer(self, player=None):
        if player is not None:
            p = player
        else:
            p = self.currentPlayer
        return 1 - p
    
    
    def getOppositeSide(self, pos):
        return 1 - pos[0], 5 - pos[1]
    
    '''def nextState'''
   
    '''def currentPlayer(self, state)'''
    
    def nextState(self, gameState, pos, isAnimated=False):
        global strMessage
        
        if self.extraTurn:
            self.extraTurn = False
        
        side, bin = pos
        #print('Start: side', side, 'bin', bin)
        n = gameState[side][bin]
        
        gameState[side][bin] = 0        
        
        for i in range(n):
            bin += 1
            if bin > 6:
                side = 1 - side
                bin = 0
            #print('loop:', i, '<=', (n + 1), ': side', side, 'bin', bin)
            gameState[side][bin] += 1
            
            if isAnimated:
                moving = self.coord[(pos[0], pos[1])].pop(0)
                dest = givePosAndShade((side, bin), moving[2])
                animateMove(self, moving, dest)
                self.coord[(side, bin)].append(dest)
            
            
        # checking the last sown seed
        if side == self.currentPlayer:
            if bin == 6:
                self.extraTurn = True
                # print a message saying so --> set a strMessage
            elif gameState[side][bin] == 1:
                # sown in one own's empty bin: capturing the opposite pieces 
                other, otherBin = self.getOppositeSide((side, bin))
                if gameState[other][otherBin] > 0:
                    captured = gameState[other][otherBin]
                    if isAnimated:
                        strMessage = '%s captures %d seed' % (P[self.currentPlayer], captured)
                        if captured != 1: strMessage += 's'
                    
                    gameState[other][otherBin] = 0
                    gameState[side][bin] = 0
                    gameState[side][6] += captured + 1
                    
                    if isAnimated:
                        for i in range(captured):
                            orig = self.coord[(other, otherBin)].pop(0)
                            dest = givePosAndShade((side, 6), orig[2])
                            
                            animateMove(self, orig, dest)
                            self.coord[(side, 6)].append(dest)                
                        
                        orig = self.coord[(side, bin)].pop(0)
                        dest = givePosAndShade((side, 6), orig[2])
                        animateMove(self, orig, dest)
                        self.coord[(side, 6)].append(dest)                

        return gameState
                
                    
    def isGameOver(self, gameState=None):
        if gameState is None:
            gs = self.state
        else:
            gs = gameState
        return sum(gs[0][:6]) == 0 or sum(gs[1][:6]) == 0 
    
    
    def winner(self, gameState=None):
        if gameState is None:
            gs = self.state
        else:
            gs = gameState
        if self.isGameOver(gs):
            sc0 = sum(gs[0])
            sc1 = sum(gs[1])
            if sc0 > sc1:
                return 0
            elif sc0 < sc1:
                return 1
            else:
                return -1
    
'''https://jeffbradberry.com/posts/2015/09/intro-to-monte-carlo-tree-search/'''
class MonteCarlo(object):
    def __init__(self, board, **kwargs):
        self.board = board
        self.states = []
        self.update(board.state)        
        self.wins = {}
        self.plays = {}
        seconds = kwargs.get('time', 5)
        self.calculationTime = datetime.timedelta(seconds=seconds)
        self.maxMoves = kwargs.get('maxMoves', 50)
        self.C = kwargs.get('C', 1.4)
    
    def update(self, state):
        self.states.append(state)
    
    def getPlay(self):
        self.maxDepth = 0
        state = self.states[-1]
        player = self.board.currentPlayer
        available = self.board.getAvailableMoves()
        
        if not available:
            return
        if len(available) == 1:
            return available[0]
        
        games = 0        
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculationTime:
            self.runSimulation()
            games += 1
            
        movesStates = [(p, self.board.nextState(state, p)) for p in available]
        
        print('games:', games, 'time elapsed:', datetime.datetime.utcnow() - begin)
        
        # pick the move with the highest percentage of wins
        percentWins, move = max(
            (self.wins.get((player, S), 0) /
             self.plays.get((player, S), 1), p)
            for p, S in movesStates
        )
        print("best move:", move, "%chance of winning:", percentWins)
        
        # display stats for each possible play
        for x in sorted(((100 * self.wins.get((player, S), 0) /
                         self.plays.get((player, S), 1),
                         self.wins.get((player, S), 0),
                         self.plays.get((player, S), 0), p)
                        for p, S in movesStates), reverse=True):
            print("{3}: {0:.2f}% ({1} / {2})".format(*x))
            
        print("Maximum depth searched: %d" % self.maxDepth)
        
        return move
    
    
    def runSimulation(self):
        plays, wins = self.plays, self.wins
        
        visitedStates = set()
        statesCopy = self.states[:]
        state = statesCopy[-1]
        player = self.board.currentPlayer
        
        expand = True
        for t in range(1, self.maxMoves + 1):
            print("t:",t, "statesCopy", statesCopy)
            available = self.board.getAvailableMoves(statesCopy[-1], player)
            movesStates = [(p, self.board.nextState(state, p)) for p in available]
            
            if all(plays.get((player, tuple(S))) for p, S in movesStates):
                # if we have stats on all of the legal moves here, use them.
                log_total = math.log(sum(plays[(player, S)] for p, S in movesStates))
                value, move, state = max(
                    ((wins[(player, S)] / plays[(player, S)]) +
                     self.C * math.sqrt(log_total / plays[(player, S)]), p, S)
                    for p, S in movesStates
                )
            else:
                move, state = random.choice(movesStates)
            
            statesCopy.append(state)
            
            ''' 'player' refers to player who moved
            into that particular state.'''
            if expand and (player, tuple(state)) not in plays:
                expand = False
                plays[(player, tuple(state))] = 0
                wins[(player, tuple(state))] = 0
                if t > self.maxDepth:
                    self.maxDepth = t
            
            visitedStates.add((player, state))
             
            player = self.board.currentPlayer
            winner = self.board.winner(statesCopy[-1])
            if winner is not None:
                break
            
        for player, state in visitedStates:
            if (player, tuple(state)) not in plays:
                continue
            plays[(player, tuple(state))] += 1
            if player == winner:
                wins[(player, tuple(state))] += 1

    

def main():
    global DISPLAYSURF, FPSCLOCK, BASICFONT, strMessage, strMessage2, mcts
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Mancala2')
    BASICFONT = pygame.font.Font('freesansbold.ttf', FONTSIZE)
    
    board = Board()
    board.state, board.coord = getStartingBoard()
    mcts = MonteCarlo(board)
    strMessage = ''
    strMessage2 = ''
    computerMove = None
    
    computerStartTime = time.time()
    
    drawBoard(board)
    pygame.display.update()    
    
    while True:
        
        currentPosition = None
        hintPosition = None
        mouseClicked = False
        strMessage = ''
        
        checkForQuit()
        for event in pygame.event.get(KEYUP):
            if board.isGameOver():
                board = Board()
                strMessage = ''
                strMessage2 = ''
                drawBoard(board)
                pygame.display.update()
            pygame.event.post(event)
        
        if not board.isGameOver(): 
            
            if P[board.currentPlayer] == PLAYER:
    
                for event in pygame.event.get():
                    if event.type == MOUSEMOTION:
                        mousex, mousey = event.pos
                    elif event.type == MOUSEBUTTONDOWN:
                        mousex, mousey = event.pos
                        mouseClicked = True
                            
    
                currentPosition = getPositionAtPixel(mousex, mousey, board.currentPlayer)
                hintPosition = getPositionAtPixel(mousex, mousey)
    
                if mouseClicked:
                    if currentPosition:
                        print('you chose:', currentPosition)
                        
                        board.nextState(board.state, currentPosition, True)
                        if not board.extraTurn:
                            computerStartTime = time.time()
                            
                    
                    else: # clicked somewhere else. menu?
                        pass
                
            else:
                if computerMove is None:
                    computerMove = getBestMove(board)
                
                # computer's turn
                if time.time() - computerStartTime >= COMPUTERPAUSE and computerMove is not None:
                
                    print('computer chose:', computerMove)
                    board.nextState(board.state, computerMove, True)
                    computerMove = None
                    
                    if board.extraTurn:
                        computerStartTime = time.time()
                else:
                    mcts.runSimulation()
        
                
            if board.extraTurn:
                board.extraTurn = False
            else:
                board.changePlayer()     
        
        
        else: # game over
            board.endScore()
            if board.winner is not None:
                strMessage = '%d vs %d. %s won the game' % (board.state[0][6], board.state[1][6], P[board.winner])
            else:
                strMessage = '%d vs %d. The game is a tie' % (board.state[0][6], board.state[1][6])
            strMessage2 = 'Press key for new game'                
        
        
        drawBoard(board, currentPosition, hintPosition)
        pygame.display.update() # enkel dirty area updaten...
        FPSCLOCK.tick(FPS)

 
def checkForQuit():
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()   
        pygame.event.post(event)
        

def getStartingBoard():
    boardState = []
    boardCoord = {}
    for i in range(len(P)):
        side = [3 for x in range(6)]
        side.append(0)      
        boardState.append(side)
                   
        for j in range(7):
            boardCoord[(i, j)] = []
            for k in range(side[j]):
                boardCoord[(i, j)].append(givePosAndShade((i, j)))
        
         
    return boardState, boardCoord
    

def getXYCoordinate(pos):
    # pos is a tuple, with first item the player: 0 is below, 1 is above
    # the second item: 0-5: 1st to 6th bin, 6 is the kalaha

    i, j = pos
    if j < 6:
        # the bins
        x = XMARGIN + (BIGRADIUS * 2) + INNERMARGIN + (INNERMARGIN + SMALLRADIUS * 2) * j + SMALLRADIUS
        y = YMARGIN + (1 - i) * (INNERMARGIN + SMALLRADIUS * 2) + SMALLRADIUS
    else:
        # the kalaha
        x = WINDOWWIDTH - (XMARGIN + BIGRADIUS)
        y = WINDOWHEIGHT // 2
    if i == 1:
        x = WINDOWWIDTH - x    
    return x, y


def getPositionAtPixel(x, y, player=None):
    # if player=None, then we want to get any of the bins or kalahas that match the location of x, y
    # if looking from the perspective of a player, this method just wants to look at the player's bins WITHOUT the kalaha
    for i in range(2):
        if player is not None:
            rangeNr = 6 # exclude the kalaha
            if player != i:
                continue
        else:
            rangeNr = 7 # include the kalaha
        for j in range(rangeNr): 
            x2, y2 = getXYCoordinate((i, j))
            dist = math.sqrt((x2 - x) ** 2 + (y2 - y) ** 2)
            if dist <= BIGRADIUS:
                return i, j


def givePosAndShade(pos, shade=None):  
    x, y = getXYCoordinate(pos)
    
    if pos[1] == 6:
        radx = BIGRADIUS
    else:
        radx = SMALLRADIUS
        
    limitx = random.randint(-(radx - 4 - SEEDSIZE), radx - 4 - SEEDSIZE)
    limity = int(math.sin(math.acos(limitx / (radx - 4))) * SMALLRADIUS)
    
    seedx = x + limitx
    seedy = random.randint(y - (limity - SEEDSIZE), y + limity - SEEDSIZE)

    if shade is None:
        newShade = (random.randint(0, 30), random.randint(0, 30), random.randint(0, 30))
    else:
        newShade = shade
    
    return seedx, seedy, newShade          


def animateMove(board, origin, destination):
    startx, starty = origin[0], origin[1]
    endx, endy = destination[0], destination[1]
    
    speedRate = FPS // 3
    
    stepx = (endx - startx) // speedRate
    stepy = (endy - starty) // speedRate
    
    for i in range(speedRate):
        checkForQuit()
        drawBoard(board, moving=(startx + i * stepx, starty + i * stepy, origin[2]))    
        pygame.display.update()    
        FPSCLOCK.tick(FPS)   
    
    
    
def drawBoard(board, select=None, hint=None, moving=None, debug=False):
    DISPLAYSURF.fill(BGCOLOR)
    
    textSurf = BASICFONT.render('%s\'s Turn' % (P[board.currentPlayer]), True, PCOLOR[board.currentPlayer])
    textRect = textSurf.get_rect()
    if board.currentPlayer == 1:
        textRect.topleft = (XMARGIN, YMARGIN - 50)
    else:
        textRect.bottomleft = (XMARGIN, WINDOWHEIGHT - YMARGIN + 50) 
        
    DISPLAYSURF.blit(textSurf, textRect)
        

    # draw the bins and kalaha
    for i in range(2):
        for j in range(7):
            x, y = getXYCoordinate((i, j))
            if j == 6:
                pygame.gfxdraw.aaellipse(DISPLAYSURF, x, y, BIGRADIUS, SMALLRADIUS, PCOLOR[i])
                pygame.gfxdraw.aaellipse(DISPLAYSURF, x, y, BIGRADIUS - 1, SMALLRADIUS - 1, PCOLOR[i])
                pygame.gfxdraw.aaellipse(DISPLAYSURF, x, y, BIGRADIUS - 2, SMALLRADIUS - 2, PCOLOR[i])
                
                # draw the seeds in kalaha
            else:
                if (i, j) == select and board.state[i][j] > 0 and i == board.currentPlayer:
                    borderColor = HIGHLIGHT
                else:
                    borderColor = PCOLOR[i]                
                pygame.gfxdraw.aacircle(DISPLAYSURF, x, y, SMALLRADIUS, borderColor)
                pygame.gfxdraw.aacircle(DISPLAYSURF, x, y, SMALLRADIUS - 1, borderColor)
                pygame.gfxdraw.aacircle(DISPLAYSURF, x, y, SMALLRADIUS - 2, borderColor)

            if hint == (i, j):
                hintSurf = BASICFONT.render('(%d)' % board.state[i][j], True, PCOLOR[i])
                hintRect = hintSurf.get_rect()               
                if i == 0:
                    hintRect.center = x, y + SMALLRADIUS + 15
                else:
                    hintRect.center = x, y - SMALLRADIUS - 15
                DISPLAYSURF.blit(hintSurf, hintRect)

            # draw the seeds in the bins and kalaha
            for seed in board.coord[(i, j)]:
                pygame.gfxdraw.filled_circle(DISPLAYSURF, seed[0], seed[1], SEEDSIZE, seed[2])
                pygame.gfxdraw.aacircle(DISPLAYSURF, seed[0], seed[1], SEEDSIZE, GREY)
    
            if debug:
                textSurf = BASICFONT.render('(%d, %d)' % (i, j), True, PCOLOR[i])
                textRect = textSurf.get_rect()
                textRect.center = (x, y)
                DISPLAYSURF.blit(textSurf, textRect)
                
            if moving:
                pygame.gfxdraw.filled_circle(DISPLAYSURF, moving[0], moving[1], SEEDSIZE, moving[2])
                pygame.gfxdraw.aacircle(DISPLAYSURF, moving[0], moving[1], SEEDSIZE, GREY)
                
    
    if strMessage:
        textSurf = BASICFONT.render(strMessage, True, PCOLOR[i])
        textRect = textSurf.get_rect()
        textRect.center = (WINDOWWIDTH // 2, 30)
        DISPLAYSURF.blit(textSurf, textRect)
    if strMessage2:
        textSurf = BASICFONT.render(strMessage2, True, PCOLOR[i])
        textRect = textSurf.get_rect()
        textRect.center = (WINDOWWIDTH // 2, WINDOWHEIGHT - 30)
        DISPLAYSURF.blit(textSurf, textRect)
        

def getBestMove(board):
    startTime = time.time()
    move = mcts.getPlay() #random.choice(board.getAvailableMoves())
    endTime = time.time() - startTime
    print('move:', move, 'time:', endTime)
    return move


if __name__ == '__main__':
    main() 