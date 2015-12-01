#Shlok Amin saq665 and Brendan Frick bjf062
import struct, string, math, Queue
from sets import Set
from Queue import PriorityQueue

'''
#------------------------------------------------------------------
EECS 348
HW 3
#------------------------------------------------------------------
'''

count = 0


class SudokuBoard:

   
    def __init__(self, size, board):
      self.BoardSize = size 
      self.CurrentGameBoard= board 

    def set_value(self, row, col, value):
        self.CurrentGameBoard[row][col]=value 
        return SudokuBoard(self.BoardSize, self.CurrentGameBoard) 
    def print_board(self):
        """Prints the current game board. Leaves unassigned spots blank."""
        div = int(math.sqrt(self.BoardSize))
        dash = ""
        space = ""
        line = "+"
        sep = "|"
        for i in range(div):
            dash += "----"
            space += "    "
        for i in range(div):
            line += dash + "+"
            sep += space + "|"
        for i in range(-1, self.BoardSize):
            if i != -1:
                print "|",
                for j in range(self.BoardSize):
                    if self.CurrentGameBoard[i][j] > 9:
                        print self.CurrentGameBoard[i][j],
                    elif self.CurrentGameBoard[i][j] > 0:
                        print "", self.CurrentGameBoard[i][j],
                    else:
                        print "  ",
                    if (j+1 != self.BoardSize):
                        if ((j+1)//div != j/div):
                            print "|",
                        else:
                            print "",
                    else:
                        print "|"
            if ((i+1)//div != i/div):
                print line
            else:
                print sep
    


def parse_file(filename):
    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val
    
    return board
    




def iscomplete( BoardArray ):
        size = len(BoardArray)
        subsquare = int(math.sqrt(size))

        for row in range(size):
            for col in range(size):

                if BoardArray[row][col]==0:
                    return False
                for i in range(size):
                    if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                        return False
                    if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                        return False
                #determine which square the cell is in
                SquareRow = row // subsquare
                SquareCol = col // subsquare
                for i in range(subsquare):
                    for j in range(subsquare):
                        if((BoardArray[SquareRow*subsquare + i][SquareCol*subsquare + j] == BoardArray[row][col])
                           and (SquareRow*subsquare + i != row) and (SquareCol*subsquare + j != col)):
                            return False
        return True

def init_board( file_name ):
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)

def possibleVals(BoardArray):
    size = len(BoardArray)
    vals = range(size)
    for i in range(size):
        vals[i] = vals[i] + 1
    return vals

def checkValid( sb ):

    BoardArray = sb.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    #check if the value of the cell
    #is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
            if(BoardArray[row][col] != 0):
                for i in range(size):
                    if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                        return False
                    if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                        return False
                #determine which square the cell is in
                SquareRow = row // subsquare
                SquareCol = col // subsquare
                for i in range(subsquare):
                    for j in range(subsquare):
                        si = SquareRow*subsquare + i 
                        sj = SquareCol*subsquare + j
                        if((BoardArray[si][sj] == BoardArray[row][col]) and (si != row) and (sj != col)):
                            return False
    return True


def createMoveMatrix( sb ):
    BoardArray = sb.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    vals = possibleVals(BoardArray)
    
    
    matrix = [ [ 0 for i in range(size) ] for j in range(size) ] #holds number of legal moves for a cell
    for row in range(size):
            for col in range(size):
                if(BoardArray[row][col] != 0):
                    matrix[row][col] = size*size + 1
                else:
                    s = set()
                    
                    for i in range(size):
                        if(BoardArray[row][i] != 0):
                            s.add(BoardArray[row][i])
                        if(BoardArray[i][col] != 0):
                            s.add(BoardArray[i][col])
                    SquareRow = row // subsquare
                    SquareCol = col // subsquare
                    for i in range(subsquare):
                        for j in range(subsquare):
                            si = SquareRow*subsquare + i
                            sj = SquareCol*subsquare + j
                            if((si != row) and (sj != col) and ((i != row) or (i!= col)) and (BoardArray[si][sj] != 0)):   
                                s.add(BoardArray[si][sj])
                    legal = len(s)
                    matrix[row][col] = size - legal
    return matrix

def checkMatrixValid( matrix ):
    size = len(matrix)
    for row in range(size):
            for col in range(size):
                if(matrix[row][col] == 0):
                    return False
    return True


def findMin(matrix):
    size = len(matrix)
    minVal = size*size + 1
    minR = -1
    minC = -1
    for row in range(size):
            for col in range(size):
                if (matrix[row][col] == 0):
                    minR = -1
                    minC = -1
                    break
                if(matrix[row][col] <= minVal and matrix[row][col] != (size*size + 1) and matrix[row][col] != 0):
                    minR = row
                    minC = col
                    minVal = matrix[row][col]
    return [minR,minC]


def findMax(matrix):
    size = len(matrix)
    maxVal = 0
    minR = -1
    minC = -1
    for row in range(size):
            for col in range(size):
                if (matrix[row][col] == 0):
                    minR = -1
                    minC = -1
                    break
                if(matrix[row][col] >= maxVal and matrix[row][col] != (size*size + 1)and matrix[row][col] != 0):
                    minR = row
                    minC = col
                    maxVal = matrix[row][col]
    return [minR,minC]

def findSameValPos(matrix, pos):
    row = pos[0]
    col = pos[1]
    size = len(matrix)

    val = matrix[row][col]

    positions = []

    for i in range(size):
            for j in range(size):
                if (matrix[i][j] == val):
                    positions.append([i,j])

    return positions


def findConstrained(sb, matrix, pos):
    row = pos[0]
    col = pos[1]

    BoardArray = sb.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    BoardArray = sb.CurrentGameBoard
    count = 0
    
    for i in range(size):
        if(i != row and BoardArray[i][col] == 0):
            count += 1
        if(i != col and BoardArray[row][i] == 0):
            count += 1

    SquareRow = row // subsquare
    SquareCol = col // subsquare
    for i in range(subsquare):
        for j in range(subsquare):
            if((SquareRow*subsquare + i != row) and (SquareCol*subsquare + j != col) and (BoardArray[SquareRow*subsquare + i][SquareCol*subsquare + j] == 0)):                                
                count += 1

    return count
# returns the a priority queue of values from lest to most constrained
def findLeastConstrainedVal(sb, position):
    row = position[0]
    col = position[1]
    BoardArray = list(sb.CurrentGameBoard)
    size = len(BoardArray)
    vals = possibleVals(BoardArray)
    matrix = legalValMatrix(BoardArray)
    minDiff = size*size +1
    outVal = -1
    q = PriorityQueue(size)
    vals = possibleVals(BoardArray)
    
    for val in vals:
        if(checkValid(sb.set_value(row,col,val))):
            BoardArray[row][col] = val
            legalMatrix = legalValMatrix(BoardArray)
            diff = sum(map(sum,subMatrix(matrix,legalMatrix)))
            q.put((diff,val))
            #print "trying val %i and diff is %i" % (val,diff)
            #printBoard(legalMatrix)
    return q

# returns matrix of number of taken values
def legalValMatrix( BoardArray ):
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    vals = possibleVals(BoardArray)
    
    
    matrix = [ [ 0 for i in range(size) ] for j in range(size) ] #holds number of legal moves for a cell
    for row in range(size):
            for col in range(size):
                if(BoardArray[row][col] != 0):
                    matrix[row][col] = 0
                else:
                    s = set()
                    for i in range(size):
                        if(BoardArray[row][i] != 0):
                            s.add(BoardArray[row][i])
                        if(BoardArray[i][col] != 0):
                            s.add(BoardArray[i][col])
                    SquareRow = row // subsquare
                    SquareCol = col // subsquare
                    for i in range(subsquare):
                        for j in range(subsquare):
                            si = SquareRow*subsquare + i
                            sj = SquareCol*subsquare + j
                            if((si != row) and (sj != col) and ((i != row) or (i!= col)) and (BoardArray[si][sj] != 0)):                                
                                s.add(BoardArray[si][sj])

                    legal = len(s)
                    matrix[row][col] = size - legal
    return matrix
    
# subtracts two matracies
def subMatrix(a, b):
    size = len(a)

    matrix = [ [ 0 for i in range(size) ] for j in range(size) ] #holds number of legal moves for a cell

    for row in range(size):
            for col in range(size):
                matrix[row][col] = a[row][col] - b[row][col]

    return matrix

def solveBoard_recursiveBT( sb ):
    if (iscomplete(sb.CurrentGameBoard)):
        return sb
    else:
        BoardArray = sb.CurrentGameBoard
        size = len(BoardArray)
        for row in range(size):
            for col in range(size):
                if (BoardArray[row][col] == 0):
                    for val in possibleVals(BoardArray):
                        global count 
                        count += 1
                        if(checkValid(sb.set_value(row,col,val))):
                            sb = sb.set_value(row,col,val)
                            child = solveBoard_recursiveBT( sb );
                            if(child != False):
                                return child
                    sb = sb.set_value(row,col,0)
                    return False

def solveBoard_recursiveFC( sb ):
    if (iscomplete(sb.CurrentGameBoard)):
        return sb
    else:
        BoardArray = sb.CurrentGameBoard
        size = len(BoardArray)
        for row in range(size):
            for col in range(size):
                if (BoardArray[row][col] == 0):
                    for val in possibleVals(BoardArray):
                        global count 
                        count += 1
                        if(checkValid(sb.set_value(row,col,val)) and checkMatrixValid(createMoveMatrix(sb.set_value(row,col,val)))):
                            sb = sb.set_value(row,col,val)
                            child = solveBoard_recursiveFC( sb );
                            if(child != False):
                                return child
                    sb = sb.set_value(row,col,0)
                    return False

def solveBoard_recursiveHeur( sb,FC,MRV, MCV, LCV ):
    if (iscomplete(sb.CurrentGameBoard)):
        return sb
    else:
        BoardArray = sb.CurrentGameBoard
        size = len(BoardArray)
        while(checkMatrixValid(createMoveMatrix(sb)) and checkValid(sb)):
                matrix = createMoveMatrix(sb)
                if MRV:
                    position = findMin(matrix)
                elif MCV:
                    position = findMax(matrix)
                else:
                    for row in range(size):
                        for col in range(size):
                            if (BoardArray[row][col] == 0):
                                position = row,col
                                
                row = position[0]
                col = position[1]
                if LCV:
                    q = findLeastConstrainedVal(sb,position)
                    while(q.empty() != True):
                        val = q.get()[1]
                        global count 
                        if(checkValid(sb.set_value(row,col,val))):
                            sb = sb.set_value(row,col,val)
                            count += 1
                            child = solveBoard_recursiveHeur( sb, FC,MRV,MCV,LCV );
                            if(child != False):
                                return child
                    sb = sb.set_value(row,col,0)

                if (BoardArray[row][col] == 0):
                    for val in possibleVals(BoardArray):
                        global count 
                        count += 1
                        if(checkValid(sb.set_value(row,col,val))):
                            if False:
                                if checkMatrixValid(createMoveMatrix(sb.set_value(row,col,val))):
                                    sb = sb.set_value(row,col,val)
                                    child = solveBoard_recursiveHeur( sb,FC,MRV,MCV,LCV);
                                    if(child != False):
                                        return child
                            else:
                                sb = sb.set_value(row,col,val)
                                child = solveBoard_recursiveHeur( sb,FC,MRV,MCV,LCV );
                                if(child != False):
                                    return child
                    sb = sb.set_value(row,col,0)
                    return False
        return False

def solve(initial_board, forward_checking = False, MRV = False, MCV = False, LCV = False):
    count 
    if MRV or MCV or LCV:
        board = solveBoard_recursiveHeur(initial_board,forward_checking,MRV,MCV,LCV)
        if board != False:
            board.print_board()
            print "Consistancy Checks = ", count
    else:
        if forward_checking:
            board = solveBoard_recursiveFC(initial_board)
            board.print_board()
            print "Consistancy Checks = ", count
        else:
            board = solveBoard_recursiveBT(initial_board)
            board.print_board()
            print "Consistancy Checks = ", count




