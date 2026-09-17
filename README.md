# Asteroids

A classic Asteroids arcade game clone built in Python using Pygame.

## Features

- Smooth 2D ship rotation and movement
- Wrap-around or bounded arena gameplay
- Destructible asteroids with splitting mechanics
- Dynamic audio system (background music, laser fire, and explosions)

## Prerequisites

- Python 3.10 to 3.12
- [Pygame](https://www.pygame.org/)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vinetailgames/pygames_asteroids.git
   cd pygames_asteroids
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install pygame
   ```

## How to Play

Start the game by running:

```bash
python main.py
```

### Controls

| Action | Key |
| :--- | :--- |
| Rotate Left | `A` or `Left Arrow` |
| Rotate Right | `D` or `Right Arrow` |
| Move Forward | `W` or `Up Arrow` |
| Reverse | `S` or `Down Arrow` |
| Fire Weapon | `Spacebar` |

## Audio Configuration

Audio works automatically on Windows and macOS. If you are running the project on Linux or through WSL (Windows Subsystem for Linux), make sure your system has audio libraries (like PulseAudio) configured, or run the project directly through your native host terminal.

## Built With

- [Python](https://www.python.org/)
- [Pygame](https://www.pygame.org/)
- Built as part of the [Boot.dev](https://www.boot.dev) backend curriculum