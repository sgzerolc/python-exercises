## game states 
1. boards
   row, column, state of objects
2. objects
   - player: move around if possible
   - wall: not moving
   - target: not moving
   - computer: can be pushed by player
3. rules
   - new representation
   - take one step
   - check if wins
   - restore the board

### operations of data
1. store
2. search
3. transition
4. restore

board settings: the board is completely surrounded by walls
state of location: six states.

naive approach: use canonical form: nested lists
- benefit: no space required to store/restore
- drawbacks: long procedures, hard to understand

approach 1: borrowed from lab1's implementation: {location:state}
- benefit
  - fast find: easy to find locations required
- drawbacks
  - space: need O(n) space to store every state

approach 1.1?: using global variables to represent limited game states. -> redundant
- changes: store player's location aside, {player:location}. Otherwise, we need to find the player's location everytime when needed.
  
approach 2: use frozenset to support deep copy of dict



## pushing behavior


## solver
high-level strategy?

output: a list of moves of the player








