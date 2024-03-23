# COMP 3981 Project
## Part 2

## Team Members
- Mangat Toor
- Nicolas Rodriguez
- Tomasz Stojek
- Vitor Guara
___

## Contents

### I &nbsp;&nbsp;&nbsp;&nbsp;Game Board Representation

### II &nbsp;&nbsp;&nbsp;State Space Generation

### III&nbsp;&nbsp;&nbsp;Moving Notation

### IV&nbsp;&nbsp;Team Member Contribution

### V&nbsp;&nbsp;&nbsp;&nbsp;References

### V&nbsp;&nbsp;&nbsp;&nbsp;Additional Documents



### I &nbsp;&nbsp;&nbsp;&nbsp;Game Board Representation

  
<img src="part_2/assets/game_board.png" alt="Belgian Daisy" style="width:40%;">




#### a. State Representation

The state is represented by a dictionary where the key is a tuple of two integers: 
(int letter, int number). 
The first int in the tuple is used to represent the letter, with A will be treated as 1, and B as 2 etc.
The values in each dictionary entry is a string (String color_of_marble) representing a black or white marble. (“w” or “b”)
For the above board :  
board = dictionary
Visual Representation		State Representation
(A,1)				board(1,1).value = “w”
(C,2)				board(3,2).value = None
(G,5) 				board(7,5).value = “b”


```javascript
state = {
        "(1,1)": "white",
        "(3,2)": none,
        "(7,5)": "black",
        ...
}
```

#### b. Initial State

The initial state can be one of three states:

1. Standard  
   <img src="part_2/assets/img_3.png" alt="Standard" style="width:40%;">
2. German Daisy  
   <img src="part_2/assets/img_2.png" alt="German Daisy" style="width:40%;">
3. Belgian Daisy  
   <img src="part_2/assets/img_1.png" alt="Belgian Daisy" style="width:40%;">

#### c. Actions

Types of Movements:
•	Inline Movements:
1.	Single Marble Movement
2.	Movement of 2 or 3 Marbles Together
•	Sidestep Movements:
3. Of 2 or 3 Marbles Together

Sumitos: An action where a group of two or three marbles of one color pushes a group of opposing marbles, only occurring in inline moves.

#### Limits

An inline move of a single marble cannot execute a sumito and must move into an empty spot on the board.

There are three types of sumitos that are allowed:
3 vs 1
3 vs 2
2 vs 1
Sidestep Movements: Are limited to groups of 2 to 3 marbles that are connected along the same axis.(all touching one another in a straight line on the board) 
 Each marble in a sidestep movement must have an empty spot in the direction it will shift into.

If an inline move goes into an opposing player marble then a sumito must occur, sumito must be legal
General Prohibition: Players cannot move any of their own marbles off the board.


#### d. Transition Model

 Description        | Actions      | Resulting State                                    |
 -------------------|--------------|----------------------------------------------------|
move to direction 1 | `[marbles],1` |For each coordinate(x,y) in marbles: (x + 1,y + 1)    |
move to direction 3 | `[marbles],3` | For each coordinate(x,y) in marbles: (x +0,y + 1)  |
move to direction 5 | `[marbles],5` | For each coordinate(x,y) in marbles: (x -1,y + 0)  |
move to direction 7 | `[marbles],7` | For each coordinate(x,y) in marbles: (x - 1,y - 1) |
move to direction 9 | `[marbles],8` | For each coordinate(x,y) in marbles: (x + 0,y - 1) |
move to direction 11| `[marbles],9` | For each coordinate(x,y) in marbles: (x + 1,y + 0)    |
example Sumito to 11| `[marbles],11` | For each coordinate(x,y) in marbles: (x + 1,y + 0) AND For each opponent coordinate(x,y) inline: (x + 1,y + 0) If opponent coordinate is off-board: remove it


####  Move Examples
Move to direction 3 :
Marbles list [(1,1),(1,2)] -> For each coordinate(x,y) in marbles: (x +0,y + 1)
End state = Marbles list [(1,2),(1,3)]

Sumito to 11:
Marbles list [(1,1), (2,1),(3,1)] -> For each coordinate(x,y) in marbles: (x + 1,y + 0)
End state = Marbles list [(2,1),(3,1),(4,1)]
Opponent's Marbles [(4,1),(5,1)] -> For each coordinate(x,y) in marbles: (x + 1,y + 0)
End state = Opponent’s Marbles [(5,1)] -> (6,1) is off-board so it is removed.


The goal test consists of checking if any player has gotten six of the opposite marbles out of the board.
### II &nbsp;&nbsp;&nbsp;State Space Generation
Understanding and determining legal moves in abalone requires analyzing the current board layout and applying the game's rules accurately. To identify all legal moves using a structured approach based on two primary classes: State and State_Space_Generator. To follow the process:

Marble Locations: Begin with identifying the positions of your marbles on the board, stored in an dictionary named our_marbles.

#### Key Classes
#### State:

Purpose: Captures a potential state space / board layout resulting from a move.
Parameters: Requires details of the move being considered and the current board setup.
Function: Holds the resultant board state after the move.

### State_Space_Generator:

Role: Central to identifying all legal moves and storing them for evaluation.
Important Arrays:
states: Stores State objects representing valid moves found.
current_marbles: Contains coordinates of the player's marbles as tuples.
current_board = current state of the board

Core Methods for Move Evaluation

### Single Marble Check:

Iterates through the player's marbles.
For each marble, it explores all possible directions for an empty spot.
Valid Moves: Inline movements into empty spaces that don't result in sumito are considered legal.
Outcome: If a valid move is identified, a new State object (comprising the move and the current board) is added to the states array.
Grouping Formation: Encountering a friendly marble forms a new group, passed to multi_marble_check for further analysis.

### Multi Marble Check:

Assesses legality of movements for marble groupings.
Validates inline movements through a helper function, considering:
Empty Space: Direct movement into an empty space is legal, and added to states as State object.
Opponent Marbles: Applies sumito check to determine legality. If legal added to states.
Friendly Marbles: For groups smaller than three, recursively applies multi_marble_check.
Sumito Checks: Evaluates the feasibility of pushing opponent marbles based on the number and arrangement of friendly and opponent marbles.


### Sumito Evaluation
Mechanism: For inline movements, it counts the number of friendly marbles from the back and checks if they can push fewer opponent marbles without affecting any friendly ones.

### III&nbsp;&nbsp;&nbsp;Moving Notation
There are two types of moves: inline (i) and side-step (s)
#### Inline Move Notation:
##### i – An – D
   i: in-line
   An: coordinate of trailing marble
   D : direction of move

#### Side Step Move Notation:
##### s – An – Bm - D
s: side-step
An, Bm: coordinates of extremities 
D : direction of move
To avoid ambiguity,
-	A <= B
-	If A = B then n <= m
-	single marble moves are always represented as inline

•	D: Direction of movement (1, 3, 5, 7, 9, 11).
o	1: Up Right
o	3: Right
o	5: Down Right
o	7: Down Left
o	9: Left
o	11: Up Left

#### Example Notation with Pictures

- Single Black Marble Move Right: `[[F6] ,3]`
  ![img_6.png](part_2/assets/img_6.png)
- Double White Marble (Straight Line) Move Up Left: `[[F5,F6], 11]`
  ![img_7.png](part_2/assets/img_7.png)
- Double White Marble (Diagonal) Move Up Right: `[[F6,E6], 1]`
  ![img_8.png](part_2/assets/img_8.png)
- Triple Black Marble Move Down Right: `[[E6,E7,E8],5]`
  ![img_9.png](part_2/assets/img_9.png)


### IV&nbsp;&nbsp;Team Member Contribution

1. **Mangat Toor**
    - Worked on timer logic for the game.
    - Worked on move notation and problem formulation.
    - Worked on move logic. 
    - Worked on pause functionality.
    - Worked on documentation.
    - Worked on State_Space_Generation

2. **Nicolas Rodriguez**
    - Worked on moving single marbles.
    - Worked on axis checking logic when moving marbles.
    - Worked on creating the initial GUI.
    - Worked on move history.
    - Worked on selection logic.
    - Worked on State_Space_Generation

3. **Tomasz Stojek**
    - Worked on logic for moving multiple marbles.
    - Worked on logic for selecting multiple marbles.
    - Worked on move history.
    - Worked on State_Space_Generation

4. **Vitor Guara**
    - Worked on the skeleton of the classes mapped to the GUI.
    - Worked on initial board positions.
    - Worked on undo and start buttons.
    - Worked on saving the states for the undo button.
    - Worked on displaying the score.
    - Worked on State_Space_Generation

### V&nbsp;&nbsp;&nbsp;&nbsp;References
Huang, C.-E. (n.d.). MoveNotation [PDF file]. BCIT. Retrieved from https://learn.bcit.ca/d2l/le/content/1003821/viewContent/9748751/View

### V&nbsp;&nbsp;&nbsp;&nbsp;Additional Documents
Step 1: Install PyInstaller
First, you need to install PyInstaller. You can do this using pip, Python's package installer. Open your command line (Terminal on macOS/Linux, Command Prompt or PowerShell on Windows) and run the following command:

pip install pyinstaller


Navigate to the folder the has game_control.py
And run the following command:

pyinstaller --name="name_of_exe" --onefile -w --add-data "gui_json/theme.json:gui_json/" game_control.py

this will create a .exe in your dist folder of part 2
 

move it to folder where the test.input files are which in this example are in part_2

 

Find the executable in part_ 2 and run it 
 

This will bring up the game menu where you can select the file you want and then select the 
Search States button, after a few seconds you will find your files in the part_2 folder 
 

