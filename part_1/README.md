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
