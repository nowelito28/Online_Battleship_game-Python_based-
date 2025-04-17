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

#### 🖥️ Start the Server

You must pass three arguments:
```bash
python servidor.py <port> <max_simultaneous_games> <ranking_file>
```

**Example:**
```bash
python servidor.py 12345 2 ranking.txt
```

- `port`: The TCP port the server will listen on
- `max_simultaneous_games`: Maximum number of active games at once
- `ranking_file`: Path to the file used to store the player rankings

#### 🎮 Start a Client

You must pass two arguments:
```bash
python cliente.py <server_ip> <port>
```

**Example:**
```bash
python cliente.py 127.0.0.1 12345
```

- `server_ip`: The IP address of the machine running the server (use `localhost` if local)
- `port`: Must match the server’s port

> 🧠 You can open multiple terminals and run clients simultaneously to simulate multiplayer locally.

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
