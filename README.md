# Connect-N Interactive Game

A modern, interactive implementation of the classic Connect Four game with enhanced graphics, intelligent AI, and comprehensive game customization options.

## How It Works

Connect-N is a strategic board game where players take turns dropping colored pieces into a vertical grid. The objective is to connect a specified number of pieces in a row (horizontally, vertically, or diagonally) before your opponent does.

## Game Setup and Configuration

### Interactive Setup Menu

The game features a comprehensive setup menu that allows players to customize every aspect of gameplay:

1. **Grid Size Configuration**:
   - Set number of columns (4-12) using left/right arrow keys
   - Set number of rows (4-12) using up/down arrow keys
   - Visual feedback displays current grid dimensions

2. **Winning Condition**:
   - Choose how many consecutive pieces are needed to win (3 or more)
   - Must be compatible with chosen grid size

3. **Game Mode Selection**:
   - **Player vs Player**: Local multiplayer for two human players
   - **Player vs AI**: Single player against computer opponent

4. **Player Setup**:
   - For PvP: Enter names for both players
   - For PvAI: Enter player name (AI automatically named)

5. **AI Difficulty Selection** (PvAI mode only):
   - **Easy**: Basic AI with mostly random moves and occasional strategy
   - **Medium**: Advanced AI using minimax algorithm with 3-ply depth
   - **Hard**: Expert AI with 5-ply depth and strategic evaluation

### Configuration Summary

After setup completion, players see a summary of all chosen settings before starting the game.

## Gameplay Features

### Basic Rules

1. **Turn-Based Play**: Players alternate dropping one piece per turn
2. **Gravity System**: Pieces fall to the lowest available position in selected column
3. **Connection Objective**: Connect N pieces in a row to win
4. **Four Connection Types**:
   - Horizontal (same row)
   - Vertical (same column)
   - Diagonal (top-left to bottom-right)
   - Anti-diagonal (top-right to bottom-left)

### Interactive Features

- **Visual Column Highlighting**: Valid drop columns glow when it's player's turn
- **Piece Preview**: Hover over columns to see where pieces will land
- **Turn Indicators**: Color-coded display showing current player
- **Smooth Animations**: Pieces drop with realistic physics
- **Victory Celebrations**: Particle effects and flashing animations for wins
- **Real-time Instructions**: On-screen text guides player actions

## AI Intelligence System

### Difficulty Levels

1. **Easy AI**:
   - Primarily random move selection
   - ~30% strategic moves for unpredictability
   - Suitable for learning game basics

2. **Medium AI**:
   - Implements minimax algorithm with 3-ply search depth
   - Evaluates immediate threats and opportunities
   - Balanced challenge for intermediate players

3. **Hard AI**:
   - Advanced minimax with 5-ply search depth
   - Sophisticated position evaluation
   - Expert-level strategic play

### AI Strategy Components

The AI evaluates board positions using multiple sophisticated factors:

- **Positional Value**: Center columns preferred for maximum connection potential
- **Threat Assessment**: Detects and prioritizes blocking opponent wins
- **Window Analysis**: Evaluates all possible N-piece combinations
- **Move Ordering**: Uses heuristics to check most promising moves first
- **Iterative Deepening**: Progressive search depth for optimal move selection

## Visual Design

### Graphics and Effects

- **Animated Backgrounds**: Dynamic gradient effects with wave animations
- **Particle System**: Physics-based victory celebration effects
- **Smooth Animations**: 60 FPS piece dropping with realistic motion
- **Visual Feedback**: Hover effects, glowing columns, turn indicators
- **Color Scheme**: Professional blue/red/yellow color palette

### User Interface

- **Responsive Design**: Adapts to different grid sizes
- **Intuitive Controls**: Mouse-based interaction with keyboard shortcuts
- **Visual Instructions**: Clear on-screen guidance
- **Professional Typography**: Clean, readable fonts throughout

## Technical Implementation

### Architecture

- **Pygame Framework**: Handles graphics, input, and audio systems
- **Event-Driven Design**: Responsive to user input and game state changes
- **Modular Code Structure**: Separate systems for AI, rendering, and game logic
- **Efficient Rendering**: Optimized for smooth 60 FPS gameplay

### Performance Optimizations

- **Alpha-Beta Pruning**: Significantly reduces AI search complexity
- **Memory Management**: Efficient particle and animation cleanup
- **Frame Rate Control**: Consistent performance across different hardware
- **Iterative Deepening**: AI finds good moves quickly and improves with time

### Audio System

- **Procedural Sound Generation**: Creates audio effects programmatically
- **Contextual Audio**: Different sounds for game events (drops, wins, UI)
- **Non-blocking Playback**: Audio doesn't interrupt gameplay flow

## Game Statistics

The game tracks comprehensive statistics across sessions:

- Total games played
- Win/loss ratios for players and AI
- Average moves per game
- Best and worst game performances
- Move efficiency metrics

## System Requirements and Installation

### Requirements
- Python 3.x
- Pygame library
- NumPy library

### Installation
```bash
pip install pygame numpy
```

### Launch
```bash
python connect_n_improved.py
```

## Controls and Gameplay

### Menu Navigation
- **Arrow Keys**: Navigate options and adjust values
- **Enter**: Confirm selections and proceed
- **ESC**: Cancel text input

### In-Game Controls
- **Mouse**: Click columns to drop pieces, hover for preview
- **Visual Feedback**: Glowing columns indicate valid moves

## Strategic Gameplay

### Basic Strategy

1. **Center Control**: Middle columns provide most connection opportunities
2. **Threat Creation**: Build multiple winning lines simultaneously
3. **Defensive Priority**: Block opponent threats before creating your own
4. **Position Awareness**: Different board positions have varying strategic value

### AI Counterplay

- **Easy AI**: Focus on simple patterns and immediate blocking
- **Medium AI**: Plan 2-3 moves ahead, create dual threats
- **Hard AI**: Study positional evaluation, force defensive positions

### Board Size Considerations

- **Small Boards** (4x4, 5x5): Faster games, tactical focus
- **Large Boards** (8x8+): Longer games, strategic depth
- **Custom N Values**: Different win conditions change game dynamics

## Advanced Features

### Customization Options

- **Flexible Grid Sizes**: 4x4 to 12x12 boards
- **Variable Win Conditions**: Connect 3+ pieces to win
- **Multiple AI Difficulties**: Easy to expert level opponents
- **Custom Player Names**: Personalized gaming experience

### Technical Features

- **Cross-platform Compatibility**: Works on Windows, macOS, Linux
- **Configurable Settings**: All game parameters adjustable
- **Performance Monitoring**: Frame rate and AI timing statistics
- **Error Handling**: Graceful handling of edge cases and invalid inputs

## Troubleshooting

### Common Issues

1. **Game Won't Start**: Ensure pygame and numpy are installed
2. **No Sound**: Audio is generated programmatically, should work automatically
3. **Performance Issues**: Lower grid sizes for better performance
4. **Display Problems**: Game adapts to screen resolution automatically

### Configuration Tips

- Start with default settings for best experience
- Use medium AI difficulty for balanced challenge
- Experiment with different grid sizes to vary gameplay
- Larger N values require bigger boards for interesting games

## Development and Extension

The codebase is designed for easy modification and extension:

- **Modular Architecture**: Separate AI, UI, and game logic
- **Configurable Constants**: Easy adjustment of game parameters
- **Extensible AI**: Add new difficulty levels or strategies
- **Theme System**: Support for additional visual themes

This enhanced Connect-N implementation provides a modern gaming experience while preserving the strategic depth of the classic game. Whether playing against friends or challenging sophisticated AI opponents, players will enjoy smooth gameplay with beautiful visuals and intelligent computer opponents.#   C o n n e c t - N - G a m e -  
 