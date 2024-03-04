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
    - <sub>S</sub> subscript represents the shape of the marbles if they are double or triple `(T,D)`. If no subscript
      then the marbles are in a straight line
        - <sub>p</sub> The marbles are in a diagonal shape with the left side pointing down and the right side pointing
          up
        - <sub>n</sub> The marbles are in a diagonal shape with the right side pointing down and the left side pointing
          up
- Z: Direction of movement (R, L, U, D, UL, DL, UR, DR).

## Example Notation

- Single Black Marble Move Right: `[B, S, R]`
- Double White Marble(Straight Line) Move Up Left: `[W, D, UL]`
- Double White Marble(Diagonal) Move Up Left: `[W, Dₙ, UL]`
- Triple Black Marble Move Down Right: `[B, T, DR]`