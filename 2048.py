import random
import  copy

boardSize = 4 #Change the number as per the required board matrix. E.g. 5 for 5x5 board

#All the functions used in this game:
def newVal(): 
    if random.randint(1, 8) == 1: #Defining the probability that a '4' is generate to be 1/8
        return 4 
    else: 
        return 2 #Mostly generate '2'
        
def addVal():
    rNum = random.randint(0, boardSize-1)
    cNum = random.randint(0, boardSize-1)
    
    while not board[rNum][cNum] == 0:
        rNum = random.randint(0, boardSize-1)
        cNum = random.randint(0, boardSize-1)
    
    board[rNum][cNum] = newVal()

def findMax(board):
    maxNum = board[0][0]
    for r in board:
        for c in r:
            if c > maxNum:
                maxNum = c
    return maxNum

def display():
    maxSpace = len(str(findMax(board))) #Find the number of digits in the largest number
    
    for r in board:
        currLine = "|"
        for i in r:
            if i == 0:
               currLine += (" " * maxSpace) + "|" #Print empty space acc to the length of the largest number
               
            else: 
                currLine += (" " * (maxSpace-len(str(i)))) + str(i) + "|" #Print empty space for num of digits less than largest num
                                                                          #Then print the number
                
        print(currLine) 
    print()
    

def mergeOneLeft(r):
    for j in range(boardSize - 1): #Check all rows except the last
        for i in range(boardSize - 1, 0, -1): 
            if r[i-1] == 0:
                r[i-1] = r[i] #Move to the leftmost possible position
                r[i] = 0
            
    for i in range(boardSize - 1): 
        if r[i] == r[i+1]:
            r[i] *= 2 #Merge when equal values
            r[i+1] = 0
            
    for i in range(boardSize-1, 0, -1): #Shift again if any empty space
        if r[i-1] == 0:
            r[i-1] = r[i]
            r[i] = 0
            
    return r
    
def mergeLeft(currBoard):
    for i in range(boardSize):
        currBoard[i] = mergeOneLeft(currBoard[i]) #Iterate through each row and shift it left
        
    return currBoard
    
def reverseR(r):
    newList = []
    for i in range(boardSize-1, -1, -1):
        newList.append(r[i]) #Reverse the row and add to the new row
    
    return newList

def mergeRight(currBoard): #Merging right is the same as flipping the board 180 degrees and merging to the left
    for i in range (boardSize):
        currBoard[i] = reverseR(currBoard[i]) #Reverse the row 
        currBoard[i] = mergeOneLeft(currBoard[i]) #Merge it to left side
        currBoard[i] = reverseR(currBoard[i]) #Reverse the row again

    return currBoard  
    
def transpose(currBoard):
    for j in range(boardSize): #For columns in the board
        for i in range(j, boardSize): #For rows in each column
            if not i == j: #Do not swap the elements on diagonal
                temp = currBoard[j][i]
                currBoard[j][i] = currBoard[i][j]
                currBoard[i][j] = temp
            
    return currBoard
    
    
    
def mergeUp(currBoard):
    currBoard = transpose(currBoard)
    currBoard = mergeLeft(currBoard)
    currBoard = transpose(currBoard)
    
    return currBoard
    
def mergeDown(currBoard):
    currBoard = transpose(currBoard)
    currBoard = mergeRight(currBoard)
    currBoard = transpose(currBoard)
    
    return currBoard
    
def won(): #Find if the player has reached '2048'
    for r in board:
        if 2048 in r:
            return True
            
    return False
    
def lost(): 
    temp = copy.deepcopy(board)
    temp2 = copy.deepcopy(board)
    
    #Check if merging is possible in any direction. If not, declare that the player has lost the game
    temp = mergeRight(temp)
    if temp == temp2:
        temp = mergeDown(temp)
        if temp == temp2:
            temp = mergeRight(temp)
            if temp == temp2:
                temp = mergeLeft(temp)
                if temp == temp2:
                    return True
    
    return False

#Game STARTS here:       
board = [] #Generate an empty board
for i in range(boardSize):
    r = [] 
    for j in range(boardSize):
        r.append(0) #Initiate all values to zero
    board.append(r) #Append the new row to the board to create an array of arrays
    

#Generate random row and column number (in range)   
numNeeded = 2
while numNeeded > 0:
    r = random.randint(0, boardSize-1)
    c = random.randint(0, boardSize-1)
    
    if board[r][c] == 0:
        board[r][c] = newVal() #Call function to generate a random number in an empty/'0' place
    numNeeded -= 1

#Print a message to indicate that game has started
print("!!2048!!\nYou goal is to get 2048 by merging the values on the board.")
print("Function keys: 'w' to merge up, 's' to merge down, 'a' to merge left, and 'd' to merge right.")
print("Game Start:")
display() #Start by displaying empty board

gameOver = False

while not gameOver:
    currMove = input("Which way do you want to merge?") #Ask for new move

    validIpt = True
    temp = copy.deepcopy(board)
    
    if currMove == 'w': #Merge up
        board = mergeUp(board)
    elif currMove == 's': #Merge down
        board = mergeDown(board)
    elif currMove == 'a': #Merge left
        board = mergeLeft(board)
    elif currMove == 'd': #Merge right
        board = mergeRight(board)
    else:
        validIpt = False 

    #If the input is not valid    
    if not validIpt:
	    print("Your input was not valid, please try again") #Account for mistyped input
    else:
        if board == temp: #If the move that the player asks for is not possible
            print("Try a different direction!")
        else: #If board is same after a move, check if the game ended
            if won(): 
                display()
                print("You won!!")
                gameOver = True
            else:
                addVal() #Find an empty spot to generate new number
                display()
                
                if lost():
                    print("You've lost!!")
                    gameOver = True
        
        
    
