# K-in-a-Row AI Agent

An intelligent game-playing agent for **K-in-a-Row**, a generalized Tic-Tac-Toe variant with configurable board sizes, win conditions, and forbidden squares. Built as part of a university AI course, this project demonstrates classical adversarial search techniques combined with a conversational dialog system.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## About the Game

K-in-a-Row is a two-player strategy game that generalizes Tic-Tac-Toe:

- **Configurable board** — any `m × n` grid (not just 3×3)
- **Configurable win condition** — get **K** tokens in a row to win (horizontally, vertically, or diagonally)
- **Forbidden squares** — certain cells are blocked and cannot be played
- **Handicaps** — pre-placed tokens can shift the starting advantage

Supported game types include classic Tic-Tac-Toe, Five-in-a-Row, Cassini, and custom configurations.

## Features

### Game-Playing Engine
- **Minimax search** with configurable depth limits
- **Alpha-beta pruning** for efficient tree exploration, significantly reducing the number of states evaluated
- **Custom static evaluation function** that scores board states based on line analysis, threats, and blocking opportunities
- **Zobrist hashing** *(optional)* — transposition table for caching previously evaluated board states
- **Move ordering** — children sorted by static eval to maximize alpha-beta cutoffs

### Conversational Agent
The agent maintains an in-character persona and participates in dialog throughout the game. Utterances are:

- **Persona-driven** — consistent character voice across the match
- **Game-state aware** — comments reflect the current board position, threats, and momentum shifts
- **Opponent-responsive** — reacts to the other player's remarks
- **Search-instrumented** — can report real statistics about its computation (states evaluated, cutoffs, time spent)

### Special Dialog Commands
| Opponent says | Agent responds with |
|---|---|
| *"Tell me how you did that"* | Detailed stats on its last move computation |
| *"What's your take on the game so far?"* | A narrative summary of the game history and a win prediction |

## Project Structure

```
.
├── yourUWNetID_KInARow.py    # Main agent implementation
├── Game_Master_Offline.py     # Run matches between agents locally
├── game_types.py              # State and Game_Type class definitions
├── agent_base.py              # Base agent class (KAgent)
├── RandomPlayer.py            # Sample random-move agent
├── winTesterForKinARow.py     # Win-condition checker
├── gameToHTML.py              # Generates HTML game transcripts
└── transcripts/               # Archived match transcripts (HTML/PDF)
```

## Getting Started

### Prerequisites
- Python 3.10+

### Running a Match

1. Open `Game_Master_Offline.py` and configure the two agents and game type at the bottom of the file.

2. Run the game:
   ```bash
   python Game_Master_Offline.py
   ```

3. An HTML transcript of the match will be generated automatically.

### Modes of Play

| Mode | Description |
|---|---|
| **Demo** | Full dialog enabled, relaxed timing (~3 sec/move). Best for showcasing the agent's personality. |
| **Autograder** | Features toggled on/off for grading. Uses controlled eval functions and move ordering. |
| **Competition** | Dialog off (except introductions). Strict time limits for tournament elimination rounds. |

## Algorithms

### Minimax with Alpha-Beta Pruning

The agent uses depth-limited minimax search. Alpha-beta pruning eliminates branches that cannot influence the final decision, often cutting the effective branching factor roughly in half. X is always the maximizing player; O is always minimizing.

```
minimax(state, depth, α, β)
  if terminal or depth == 0:
    return static_eval(state)
  if maximizing:
    for each child (ordered by eval):
      α = max(α, minimax(child, depth-1, α, β))
      if α ≥ β: break   ← cutoff
    return α
  else:
    ...symmetric for minimizing
```

### Static Evaluation

The evaluation function analyzes every possible K-length line on the board and scores based on:
- Number of friendly tokens in each line vs. opponent tokens
- Open-ended threats (lines that can still be completed)
- Near-win detection (K-1 in a row with an open slot)
- Blocking value (preventing opponent completions)

### Zobrist Hashing *(Extra Credit)*

A transposition table using Zobrist keys allows the agent to recognize previously evaluated board positions and skip redundant computation. Stats tracked: table writes, read attempts, and cache hits.

## Sample Transcript

> **Agent:** "Interesting — you've opened with a center play. Classic, but I've seen this before."
>
> **Opponent:** "Tell me how you did that"
>
> **Agent:** "Sure! I searched 847 states in 0.12 seconds at depth 4. Alpha-beta pruning saved me from evaluating roughly 1,200 additional nodes. I chose column 3 because it sets up a dual threat on rows 2 and 4."

## Acknowledgments

- Course staff for the starter code framework and game type definitions
- Built for CSE courses at the University of Washington
