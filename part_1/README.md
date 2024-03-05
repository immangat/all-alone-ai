# Part 1

## Contents

- Game Board Representation
- Moving Notation
- Problem Formulation
- Team Member Contribution
- Source Code

### II Moving Notation

Moves are represented as `[[X], Z]`, where:

- X: Contains coordinates of each marble that will be moved in an array
- Z: Direction of movement (R, L, UL, DL, UR, DR).
    - R: Right
    - L: Left
    - UL: Up Left
    - DL: Down Left
    - UR: Up Right
    - DR: Down Right

#### Example Notation with Pictures

- Single Black Marble Move Right: `[[F6] ,R]`
  ![img_6.png](pictures/img_6.png)
- Double White Marble (Straight Line) Move Up Left: `[[F5,F6], UL]`
  ![img_7.png](pictures/img_7.png)
- Double White Marble (Diagonal) Move Up Right: `[[F6,E6], UL]`
  ![img_8.png](pictures/img_8.png)
- Triple Black Marble Move Down Right: `[[E6,E7,E8],DR]`
  ![img_9.png](pictures/img_9.png)

### III Problem Formulation

#### a. State Representation

The state is resented in by a dictionary(`{circle_name: circle_object}`) of circles that can contain a black or white marble. With each move, the
marble(s) are moved to the intended location. 
```javascript

  state = {
  "I5": {marble: Marble()},
  "H5": {marble: none},
  "G5": {marble: none},
  ...,
}
```
#### b. Initial State

The initial state can be one three states

1. Standard  
![img_3.png](img_3.png)
2. German Daisy  
![img_2.png](img_2.png)
3. Belgian Daisy  
![img_1.png](img_1.png)

#### c. Actions

The action can be defined with the move notation and involves moving marbles(1 to 3) to a one of six direction(as
defined in part II)

#### d. Transition Model

#### e. Goal Test

- After each move as been made, check if a side(Black/White) has collected 6 marbles 
