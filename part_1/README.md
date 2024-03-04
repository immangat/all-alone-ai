# Part 1

## Contents

- Game Board Representation
- Moving Notation
- Problem Formulation
- Team Member Contribution
- Source Code

### II Moving Notation

Moves are represented as `[X, Yₛ, Z]`, where:

- X: Number of marbles moved (S for single, D for double, T for triple).
- Y: Type of marble (B for black, W for white).
    - If no subscript, the marbles are in a straight line. Subscript represents the shape of the marbles if they are
      double or triple (T, D).
        - <sub>p</sub>: The marbles are in a diagonal shape with the left side pointing down and the right side pointing
          up.
        - <sub>n</sub>: The marbles are in a diagonal shape with the right side pointing down and the left side pointing
          up.
- Z: Direction of movement (R, L, U, D, UL, DL, UR, DR).
    - R: Right
    - L: Left
    - U: Up
    - D: Down
    - UL: Up Left
    - DL: Down Left
    - UR: Up Right
    - DR: Down Right

#### Example Notation with Pictures

- Single Black Marble Move Right: `[B, S, R]`
  ![img_6.png](pictures/img_6.png)
- Double White Marble (Straight Line) Move Up Left: `[W, D, UL]`
  ![img_7.png](pictures/img_7.png)
- Double White Marble (Diagonal) Move Up Left: `[W, Dₙ, UL]`
  ![img_8.png](pictures/img_8.png)
- Triple Black Marble Move Down Right: `[B, T, DR]`
  ![img_9.png](pictures/img_9.png)
