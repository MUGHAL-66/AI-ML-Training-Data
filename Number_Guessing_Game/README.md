# Number Guessing Game

A standalone desktop game built with Python and Tkinter. Try to find the computer's hidden number from 1 to 100 in a polished dark-themed interface.

## Features

- Dark navy interface with purple and blue accents
- Easy, Medium, and Hard difficulty levels
- Attempts counter and progress indicator
- Higher/lower hints, win screen, and game-over result
- Input validation and Enter key support
- Play again or change difficulty to start a fresh round
- Uses Python's standard library; no third-party packages are needed

## Requirements

- Python 3.8 or newer
- Tkinter (included with most standard Python installations; on some Linux distributions, install the `python3-tk` system package)

## Run the application

From this folder, run:

```powershell
python main.py
```

On Windows, `py main.py` can also be used if the Python launcher is installed.

## Game rules

The computer chooses a random whole number from 1 to 100. Enter a guess and the game tells you whether the hidden number is higher or lower. Each valid guess uses one attempt; invalid input does not. Easy gives you 10 attempts, Medium gives you 7, and Hard gives you 5. Find the number before you run out of attempts. Choose **PLAY AGAIN** or a different difficulty to begin a new round.
