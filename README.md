# Battleship Online – Turn-Based Multiplayer Game

This is a Python-based online turn-based strategy game inspired by Battleship, with RPG-like characters and abilities. Built on a client-server architecture, it supports multiplayer gameplay, character abilities, rankings, and team-based strategy.

## 🎮 Game Features

- Turn-based combat with teams of characters
- Unique character classes with special abilities
- Multiplayer support via client-server architecture
- Ranking and lobby system
- Modular and expandable codebase

## 🗂️ Project Structure

```
battleship-online/
│
├── client/                # Client logic and player interface
│   └── client.py
│
├── server/                # Server logic and match controller
│   ├── server.py
│   ├── lobby.py
│   ├── ranking.py
│
├── game/                  # Core gameplay logic
│   ├── player.py
│   ├── character.py
│   ├── utils.py
│
├── run_server.py          # Entry point to start the game server
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- No external libraries needed (built-in modules only)

### Running the Game

To start the server:
```bash
python run_server.py
```

To connect as a player (in a different terminal or machine):
```bash
python client/client.py
```

### Multiplayer Mode

1. Launch the server
2. Run client scripts on multiple terminals
3. Players are matched and queued automatically

## 🔧 Game Components

- `Player`: Handles team creation, action selection, and turn management
- `Character`: Defines base class and specific roles like Medic, Gunner, etc.
- `Server`: Manages the game flow, player turns, and win conditions
- `Lobby`: Queue system to match players
- `Ranking`: Tracks and displays player scores
- `Utils`: Helper functions for validation, grid control, etc.

## 📄 License

MIT License. Feel free to fork and extend!
