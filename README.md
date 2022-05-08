# Chess2D

Classic two-player chess

## Ruleset:

### Synchronic:
 - Play against a live opponent
 - Modified rules of chess
     - Both players' moves happen at the same time
     - The speed of a piece determines the order of the moves
         - King: 5
         - Queen: 4
         - Rook: 3
         - Bishop: 2
         - Knight: 2
         - Pawn: 1
     - Speed ties, when two pieces with the same speed move at once, are broken by a coin flip
     - If a side loses a turn, that color moves first on the next turn
     - If a side is in check, that color moves first on the next turn
     - Castling is considered a King move
 - Pass and play with two separate boards

### Two-Player:
 - Play against a live opponent
 - Normal rules of chess
 - Pass and play with a flipping board

### One-Player:
 - Play against the unique AI
 - Normal rules of chess
 - Choose your own starting color
