# Battleship Online – Turn-Based Multiplayer Game

This is a Python-based online turn-based strategy game inspired by Battleship, with RPG-like characters and abilities. It features multiplayer support, character skills, rankings, and a simple lobby system, all in one modular, expandable codebase.

## 🎮 Game Features

- Turn-based combat with teams of characters
- Unique character classes with special abilities
- Multiplayer support using a client-server architecture
- Ranking and matchmaking system
- All files in a flat structure (no subfolders)

## 🗂️ Project Structure

```
Online_Battleship_game-Python_based-/
│
├── cliente.py           # Game client logic and player interface
├── servidor.py          # Game server logic and match controller
├── jugador.py           # Handles player teams and actions
├── personaje.py         # RPG-style character classes and abilities
├── lobby.py             # Queue/lobby system for matchmaking
├── ranking.py           # Ranking system (linked list based)
├── utils.py             # Utility functions for gameplay and validation
├── run_server.py        # Entry point to start the server
├── requirements.txt     # Python dependencies (optional)
└── README.md            # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- No external libraries needed (uses only built-in modules)

### Running the Game

To start the server:

```bash
python run_server.py
```

To run a player (in another terminal or machine):

```bash
python cliente.py
```

> 🧠 You can run multiple clients locally for testing purposes.

### Multiplayer Mode

1. Launch the server with `run_server.py`
2. Open multiple terminals and run `cliente.py` in each
3. Players are added to the lobby and matched automatically

---

## 🔧 Game Components Overview

- `jugador.py`: Handles player teams, actions, health, turns, and victory conditions.
- `personaje.py`: Defines the RPG-style character classes (Medic, Sniper, Gunner, etc.)
- `cliente.py`: Contains the player interface and game flow from the client's perspective.
- `servidor.py`: Coordinates game flow, manages player turns, and sends results.
- `lobby.py`: Simple queue system for player matching before the game starts.
- `ranking.py`: Manages a persistent ranking system using a custom linked list.
- `utils.py`: Contains helper functions for grid validation, random logic, formatting, etc.

---

## 📄 License

This project is licensed under the **MIT License**.  
You’re free to use, modify, and distribute it — just keep the original credit.

---
