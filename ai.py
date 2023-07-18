import copy



def inversion_count(puzzle):#Checking wheather solution exists or not ,solution does not exist when inversion count is odd 

    inv_count=0 #Variable for storing the number of inversions in count
    
    lst_puzzle=[]    #Converting the 2D matrix into 1D format ans storing it in the form of a list in lst_puzzle
    
    for i in range(3):
        for j in range(3):
          lst_puzzle.append(puzzle[i][j])
    
    lst_goal=[1,2,3,4,5,6,7,8,0]
    
    for i in range(9):         #Counting number of inversions(nu,ber of pairs of i,j such that a[i]>a[j] for i<j)
      curr=lst_puzzle[i]
      if(curr==0):
        continue
        
      for j in range(i+1,9):
      
        if(lst_puzzle[j]>curr and lst_puzzle[j]!=0):
          inv_count+=1
    
    
    return inv_count


def soln_exists(puzzle,goal):                      #Function  to check if Solution exists or not

    inv_puzzle=inversion_count(puzzle)             #Count the number of inversions between 'puzzle' and s'td_goal'
    inv_goal=inversion_count(goal)                  #Count the number of inversions between 'goal' and 'std_goal'

    if(inv_puzzle%2==0 and inv_goal%2==0):           #if both the inversion counts are of same parity there is a path between them(as when we move a tile inversion counts changes only by a multiple of 2)
        return 1
        
    if(inv_puzzle%2==1 and inv_goal%2==1):               #Hence checking wheather they are both odd or even
        return 1
    
    return 0



def find_idx(puzzle,num): #Function for finding the index of  a particular number  in current puzzle 
    idx=[]

    if(num==9):
        num=0
    for i in range(3):                   #Itertating over the puzzle and checking wheather at each position the required number is found or not
        for j in range(3): 
            if(puzzle[i][j]==num):
                
                idx.append(i)
                idx.append(j)
                
    return tuple(idx)


def possible_dir(puzzle): #Function to calculate the possible directions 0(empty tile) can move in the current puzzle
    dir=[]
    
    x,y=find_idx(puzzle,0)
    
    if(x<2):# if x co-ordinate is less than 2 then it can move down
         dir.append("DOWN")
         
    if(x>0):# if x co-ordinate is greater than 0 then it can move up
         dir.append("UP")
         
    if(y>0):# if y co-ordinate is greater than 0 then it can move left
         dir.append("LEFT")
         
    if(y<2):# if y co-ordinate is less than 2 then it can move right
        dir.append("RIGHT")
        
    return dir



def h_score(puzzle,goal): #Function to calculate the h_score (it is defined as the manhattan distance between goal and given state of puzzle)
    score=0
    
    for i in range(3):
        for j in range(3):
            x,y=find_idx(goal,puzzle[i][j]) #find the index of each of number in the goal state in the current_puzzle
            score=score+abs(x-i)+abs(y-j)   #Calculating Manhattan distance    
                
    return score


def gen_state(puzzle): #Function to generate all the next possible states of the puzzle from the given state
    
    i,j=(find_idx(puzzle,0)) #Find the position of empty tile in the current puzzle
    
    possible_directions=possible_dir(puzzle) #First find the possible directions the empty tile can move in the current puzzle
    
    up=0  #Boolean variable to indicate wheather the empty tile can move up
    
    down=0 #Boolean variable to indicate wheather the empty tile can move down
    
    left=0  #Boolean variable to indicate wheather the empty tile can move left
    
    right=0  #Boolean variable to indicate wheather the empty tile can move right
    
    if("UP" in possible_directions): #Updating the values of variables according to the directions the empty tile can move
        up=1
        
    if("DOWN" in possible_directions): 
        down=1
        
    if("LEFT" in possible_directions):
        left=1
        
    if("RIGHT" in possible_directions):
        right=1
        
    new_state=[] #A list for storing the newly generated puzzles from the current one
    
    if(up==1):        #Generating the new possible states from the current one
    
        new_1=copy.deepcopy(puzzle)     #Create a copy of current puzzle,use deepcopy so that when we change values in it it is not affected in current one
        
        new_1[i-1][j],new_1[i][j]=new_1[i][j],new_1[i-1][j] #Swapping the empty tile with the adjacent corresponding direction
        
        new_state.append(new_1)  #Append the newly generated state to the list 'new_state'
        
    if(down==1):                 #Repeating the same process as above for all other directions
    
        new_2=copy.deepcopy(puzzle)
        
        new_2[i+1][j],new_2[i][j]=new_2[i][j],new_2[i+1][j]
        
        new_state.append(new_2)
        
    if(left==1):
    
        new_3=copy.deepcopy(puzzle)
        
        new_3[i][j-1],new_3[i][j]=new_3[i][j],new_3[i][j-1]
        
        new_state.append(new_3)
        
    if(right==1):
    
        new_4=copy.deepcopy(puzzle)
        
        new_4[i][j+1],new_4[i][j]=new_4[i][j],new_4[i][j+1]
        
        new_state.append(new_4)
        
    return new_state



def solve(puzzle,goal): #Main solve funtion

# Logic - We keep a list path to store the differnt routes and at each step we take that route in which the lastly generated puzzle has least manhatten distance and check if it is equal to goal or if it is checked once else we generate all the childs of it and make differnt routes for all the children and add it to path,sort the path and continue this process until path is not empty

    path=[]  #A list for storing the different routes taken by the puzzle (route-sequence of moves from start to current state of the puzzle) 
    
    visited=[] #A visited array to store the puzzles that are already checked once 


    path.append([[puzzle,h_score(puzzle,goal)]]) # Add the initial puzzle to the path with it's h_score
    
    while path:
        
        current_route=path.pop(0) #Current route in which puzzle has least h_score
        
        current_puzzle=current_route[-1][0] #Current puzzle of the route
        
        if current_puzzle == goal: #Checking if current_puzzle is equal to goal or not
            goal_route=current_route
            return goal_route         #If so return the current_route
        
        if(current_puzzle in visited): #Checking if the puzzle is already visited once
            continue

        else:
            visited.append(current_puzzle) #Add the current_puzzle into the visited list

        next_state=gen_state(current_puzzle)  #generate all possible states of the current_puzzle
        
        for state in next_state:
        
            if(state in visited):         #Cheking wheather one of the state generated is already visited or not
                continue
                
            next_route=copy.deepcopy(current_route) #Create a copy of current route to add the children to it
            
            next_route.append([state,h_score(state,goal)]) #Append the newly generated state to current route
            
            path.append(next_route)  #Append the next route to path
          
            
                       
        path=sorted(path,key=lambda x:(x[-1][-1])) #Sort the routes according to the value of manhatten distance of the last puzzle of the route
    
pass

def show_puzzle(route): #Function to show puzzle along with the route

    for i in range(len(route)):  #Route represents the path from start state to goal
    
        puzzle=route[i][0]  # Accesing current puzzle of a prticular route 
            
        #Assigning all the variables their respective values
        steps_taken_until_now=i          
        h_score=route[i][1]         
        total_cost=steps_taken_until_now+h_score
        
        print("Step {}:| Steps taken until now={}, h_score={} ,total_cost={}".format(i,steps_taken_until_now,h_score,total_cost)) #Printing the  respective scores at each step
   
        for i in range(3):        #Printing the matrix
                print(puzzle[i])
        print('\n')





print("Enter the input matrix:")       

puzzle=[]         #Creating a list for storing input puzzle

goal=[]

std_goal=[[1,2,3],[4,5,6],[7,8,9]]
    

for i in range(3):     #Taking input puzzle from the user in row major form
	row=input()                      #Taking a row as input
	puzzle.append(row.split(" "))   #Splitting the numbers in a row  whenever a space encountered 

for i in range(3):
	for j in range (3):
		puzzle[i][j]=int(puzzle[i][j])     #Converting each character in the puzzle to int datatype
print()

print("Enter the goal matrix:")          

for i in range(3):                               #Accepting the goal matrix as input as similar to the puzzle matrix
    row=input()
    goal.append(row.split(" "))

for i in range(3):                       
	for j in range (3):
		goal[i][j]=int(goal[i][j])                    
		
print()

if(soln_exists(puzzle,goal)):                     #Checking wheather solution exists or not
  solution=solve(puzzle,goal)          #Solving and printing the solution if exists
  show_puzzle(solution)
    
else:
 	print("Not Solvable") 