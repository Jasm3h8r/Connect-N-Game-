import pygame
import numpy as np
import random
import math
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
FONT_SIZE = 20
# Enhanced Color Scheme
BLUE = (25, 25, 112)  # Midnight blue
LIGHT_BLUE = (70, 130, 180)  # Steel blue
DARK_BLUE = (0, 0, 50)  # Very dark blue
BLACK = (0, 0, 0)
RED = (220, 20, 60)  # Crimson red
YELLOW = (255, 215, 0)  # Gold yellow
WHITE = (255, 255, 255)
GREEN = (50, 205, 50)  # Lime green
GRAY = (105, 105, 105)  # Dim gray
LIGHT_GRAY = (220, 220, 220)  # Light gray

# Default game settings (will be overridden by menu)
n = 7  # columns
k = 6  # rows
CONNECT_N = 4  # connect 4 to win
def create_board():
    return np.zeros((k, n))
def drop_piece(board, row, col, piece):
    board[row][col] = piece
def is_valid_location(board, col):
    return board[k - 1][col] == 0
def get_next_open_row(board, col):
    for r in range(k):
        if board[r][col] == 0:
            return r
def winning_move(board, piece):
    winning_positions = []
    for c in range(n - CONNECT_N + 1):
        for r in range(k):
            if all(board[r][c + i] == piece for i in range(CONNECT_N)):
                winning_positions = [(r, c + i) for i in range(CONNECT_N)]
                return True, winning_positions
    for c in range(n):
        for r in range(k - CONNECT_N + 1):
            if all(board[r + i][c] == piece for i in range(CONNECT_N)):
                winning_positions = [(r + i, c) for i in range(CONNECT_N)]
                return True, winning_positions
    for c in range(n - CONNECT_N + 1):
        for r in range(k - CONNECT_N + 1):
            if all(board[r + i][c + i] == piece for i in range(CONNECT_N)):
                winning_positions = [(r + i, c + i) for i in range(CONNECT_N)]
                return True, winning_positions
    for c in range(n - CONNECT_N + 1):
        for r in range(CONNECT_N - 1, k):
            if all(board[r - i][c + i] == piece for i in range(CONNECT_N)):
                winning_positions = [(r - i, c + i) for i in range(CONNECT_N)]
                return True, winning_positions
    return False, []
def draw_gradient_background(screen):
    """Draw an animated gradient background"""
    time_offset = pygame.time.get_ticks() * 0.001

    for y in range(HEIGHT):
        # Create wave effect
        wave = math.sin(y * 0.01 + time_offset) * 0.2 + math.cos(y * 0.005 + time_offset * 0.7) * 0.1
        ratio = (y / HEIGHT + wave * 0.05) % 1.0

        # Gradient from midnight blue to very dark blue
        r = int(BLUE[0] * (1 - ratio) + DARK_BLUE[0] * ratio)
        g = int(BLUE[1] * (1 - ratio) + DARK_BLUE[1] * ratio)
        b = int(BLUE[2] * (1 - ratio) + DARK_BLUE[2] * ratio)

        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def create_particles():
    """Create victory particles"""
    particles = []
    for _ in range(30):
        particles.append({
            'x': random.randint(0, WIDTH),
            'y': random.randint(HEIGHT // 4, HEIGHT // 2),
            'vx': random.uniform(-3, 3),
            'vy': random.uniform(-5, -1),
            'color': random.choice([RED, YELLOW, GREEN, LIGHT_BLUE]),
            'size': random.randint(2, 6),
            'life': random.randint(60, 120)
        })
    return particles

def update_particles(particles):
    """Update particle positions"""
    for particle in particles[:]:
        particle['x'] += particle['vx']
        particle['y'] += particle['vy']
        particle['vy'] += 0.1  # gravity
        particle['life'] -= 1

        if particle['life'] <= 0 or particle['y'] > HEIGHT:
            particles.remove(particle)

def draw_particles(screen, particles):
    """Draw particles"""
    for particle in particles:
        alpha = min(255, particle['life'] * 4)
        pygame.draw.circle(screen, particle['color'], (int(particle['x']), int(particle['y'])), particle['size'])

def draw_board(board, screen, hovering_col, font, player_names, winning_positions=None, particles=None):
    # Draw animated gradient background
    draw_gradient_background(screen)

    # Draw grid with enhanced visuals
    for c in range(n):
        for r in range(k):
            # Grid squares with subtle animation
            time_offset = pygame.time.get_ticks() * 0.001
            pulse = math.sin(time_offset + c * 0.1 + r * 0.1) * 0.05 + 1.0

            grid_color = (
                min(255, int(LIGHT_BLUE[0] * pulse)),
                min(255, int(LIGHT_BLUE[1] * pulse)),
                min(255, int(LIGHT_BLUE[2] * pulse))
            )

            rect = pygame.Rect(c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE)
            pygame.draw.rect(screen, grid_color, rect)

            # Inner holes with gradient
            hole_rect = pygame.Rect(c * SQUARESIZE + 5, r * SQUARESIZE + SQUARESIZE + 5,
                                  SQUARESIZE - 10, SQUARESIZE - 10)
            pygame.draw.ellipse(screen, GRAY, hole_rect)

    if winning_positions is None:
        winning_positions = []

    # Draw pieces with enhanced visuals
    for c in range(n):
        for r in range(k):
            if board[r][c] != 0:
                if board[r][c] == 1:
                    color = RED
                    player_name = player_names[0]
                elif board[r][c] == 2:
                    color = YELLOW
                    player_name = player_names[1]

                # Highlight winning positions with animation
                if (r, c) in winning_positions:
                    time_offset = pygame.time.get_ticks() * 0.005
                    flash_intensity = (math.sin(time_offset) + 1) * 0.5  # 0 to 1
                    color = (
                        int(color[0] * (1 - flash_intensity) + GREEN[0] * flash_intensity),
                        int(color[1] * (1 - flash_intensity) + GREEN[1] * flash_intensity),
                        int(color[2] * (1 - flash_intensity) + GREEN[2] * flash_intensity)
                    )

                center_x = int(c * SQUARESIZE + SQUARESIZE / 2)
                center_y = HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)

                # Draw shadow
                pygame.draw.circle(screen, (0, 0, 0, 128), (center_x + 2, center_y + 2), RADIUS)

                # Draw main piece
                pygame.draw.circle(screen, color, (center_x, center_y), RADIUS)

                # Draw highlight
                highlight_color = (
                    min(255, color[0] + 50),
                    min(255, color[1] + 50),
                    min(255, color[2] + 50)
                )
                pygame.draw.circle(screen, highlight_color, (center_x - RADIUS//3, center_y - RADIUS//3), RADIUS//3)

    # Draw valid drop zones when it's player's turn
    if mode == 1 or (mode == 2 and turn == 0):
        for col in range(n):
            if is_valid_location(board, col):
                center_x = int(col * SQUARESIZE + SQUARESIZE / 2)
                center_y = int(SQUARESIZE / 2)

                # Subtle glow for valid columns
                glow_color = (100, 100, 100, 50)  # Semi-transparent white
                pygame.draw.circle(screen, glow_color, (center_x, center_y), RADIUS + 3)

    # Draw hovering piece with glow effect (only when it's player's turn)
    if hovering_col is not None and (mode == 1 or (mode == 2 and turn == 0)):
        color = RED if turn == 0 else YELLOW
        center_x = int(hovering_col * SQUARESIZE + SQUARESIZE / 2)
        center_y = int(SQUARESIZE / 2)

        # Glow effect
        for radius in range(RADIUS + 5, RADIUS - 1, -2):
            alpha = max(20, 100 - (RADIUS + 5 - radius) * 15)
            glow_color = (
                min(255, color[0] + alpha // 5),
                min(255, color[1] + alpha // 5),
                min(255, color[2] + alpha // 5)
            )
            pygame.draw.circle(screen, glow_color, (center_x, center_y), radius)

        pygame.draw.circle(screen, color, (center_x, center_y), RADIUS)

        # Player name with background
        text = font.render("Click to drop!", True, WHITE)
        text_bg = pygame.Rect(center_x - text.get_width()//2 - 5, center_y - RADIUS - 25,
                            text.get_width() + 10, text.get_height() + 6)
        pygame.draw.rect(screen, BLACK, text_bg, border_radius=5)
        pygame.draw.rect(screen, WHITE, text_bg, 1, border_radius=5)
        screen.blit(text, (center_x - text.get_width()//2, center_y - RADIUS - 22))

    # Draw turn indicator with better visibility
    turn_text = f"{player_names[turn]}'s Turn"
    if mode == 2 and turn == 1:
        turn_text = "AI is thinking..."
    elif mode == 2 and turn == 0:
        turn_text = f"Your Turn ({player_names[0]})"

    turn_surface = font.render(turn_text, True, WHITE)
    turn_bg = pygame.Rect(10, 10, turn_surface.get_width() + 20, turn_surface.get_height() + 10)

    # Color code the background based on whose turn it is
    if turn == 0:
        bg_color = (0, 100, 0, 200)  # Green for player turn
    else:
        bg_color = (100, 100, 0, 200)  # Yellow for AI turn

    pygame.draw.rect(screen, bg_color, turn_bg, border_radius=8)
    pygame.draw.rect(screen, WHITE, turn_bg, 2, border_radius=8)
    screen.blit(turn_surface, (20, 15))

    # Draw particles if provided
    if particles:
        draw_particles(screen, particles)

    # Draw instruction text at bottom (only during active gameplay)
    if not game_over:
        if mode == 1 or (mode == 2 and turn == 0):
            instruction_text = "Click on a glowing column to drop your piece!"
        else:
            instruction_text = "AI is thinking..."

        instr_surface = font.render(instruction_text, True, LIGHT_GRAY)
        instr_x = WIDTH // 2 - instr_surface.get_width() // 2
        instr_y = HEIGHT - 20
        screen.blit(instr_surface, (instr_x, instr_y))

    pygame.display.update()
def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locations = [c for c in range(n) if is_valid_location(board, c)]
    if depth == 0 or len(valid_locations) == 0:
        return evaluate_board(board), None
    best_col = random.choice(valid_locations)
    if maximizing_player:
        value = -math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, 2) 
            new_score, _ = minimax(board_copy, depth - 1, alpha, beta, False)
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, best_col
    else:
        value = math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, 1)
            new_score, _ = minimax(board_copy, depth - 1, alpha, beta, True)
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value, best_col
def evaluate_board(board):
    score = 0
    for r in range(k):
        for c in range(n - CONNECT_N + 1):
            window = board[r][c:c + CONNECT_N]
            score += evaluate_window(window, 1)  
            score -= evaluate_window(window, 2)  
    for c in range(n):
        for r in range(k - CONNECT_N + 1):
            window = board[r:r + CONNECT_N, c]
            score += evaluate_window(window, 1) 
            score -= evaluate_window(window, 2)
    for r in range(k - CONNECT_N + 1):
        for c in range(n - CONNECT_N + 1):
            window = [board[r + i][c + i] for i in range(CONNECT_N)]
            score += evaluate_window(window, 1) 
            score -= evaluate_window(window, 2) 
    for r in range(CONNECT_N - 1, k):
        for c in range(n - CONNECT_N + 1):
            window = [board[r - i][c + i] for i in range(CONNECT_N)]
            score += evaluate_window(window, 1) 
            score -= evaluate_window(window, 2) 
    center_col = n // 2
    for r in range(k):
        if board[r][center_col] == 1:
            score += 3  
        elif board[r][center_col] == 2:
            score -= 3
    return score
def evaluate_window(window, piece):
    score = 0
    opponent = 2 if piece == 1 else 1
    window = np.array(window)
    piece_count = np.count_nonzero(window == piece)
    empty_count = np.count_nonzero(window == 0)
    opponent_count = np.count_nonzero(window == opponent)
    if piece_count == CONNECT_N:
        score += 100
    elif piece_count == CONNECT_N - 1 and empty_count == 1:
        score += 10
    elif piece_count == CONNECT_N - 2 and empty_count == 2:
        score += 5
    if opponent_count == CONNECT_N - 1 and empty_count == 1:
        score -= 50
    if opponent_count == CONNECT_N - 2 and empty_count == 2:
        score -= 10
    return score
def is_board_full(board):
    for r in range(k):
        for c in range(n):
            if board[r][c] == 0:
                return False
    return True
# Game configuration - will be set through interactive menu
mode = None  # Will be set in menu
player_names = []
difficulty = None  # Will be set in menu

pygame.init()

# Initialize font system
pygame.font.init()

# Load fonts for menu
small_font = pygame.font.SysFont("monospace", 16)

# Initial setup menu
def show_setup_menu():
    """Interactive setup menu for game configuration"""
    global n, k, CONNECT_N, mode, player_names, difficulty

    # Menu state variables
    menu_state = "grid_size"  # grid_size, win_condition, game_mode, player_setup, difficulty, ready
    input_text = ""
    input_active = False

    # Button dimensions
    btn_width = 200
    btn_height = 40
    center_x = 400  # We'll use a fixed width for menu

    # Temporary screen for menu
    menu_screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Connect-N Setup')

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                        if menu_state == "player1_name":
                            player_names[0] = input_text if input_text.strip() else "Player 1"
                            menu_state = "player2_name" if mode == 1 else "difficulty"
                            input_text = player_names[1] if len(player_names) > 1 else ""
                        elif menu_state == "player2_name":
                            player_names[1] = input_text if input_text.strip() else "Player 2"
                            menu_state = "ready"
                        elif menu_state == "player_name":
                            player_names[0] = input_text if input_text.strip() else "Player"
                            player_names[1] = "AI"
                            menu_state = "difficulty"
                            input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        input_active = False
                        input_text = ""
                    else:
                        # Only allow alphanumeric characters and spaces
                        if event.unicode.isalnum() or event.unicode.isspace():
                            input_text += event.unicode
                elif event.key == pygame.K_UP:
                    if menu_state == "grid_size":
                        k = min(12, k + 1)
                    elif menu_state == "win_condition":
                        CONNECT_N = min(min(n, k), CONNECT_N + 1)
                elif event.key == pygame.K_DOWN:
                    if menu_state == "grid_size":
                        k = max(4, k - 1)
                    elif menu_state == "win_condition":
                        CONNECT_N = max(3, CONNECT_N - 1)
                elif event.key == pygame.K_LEFT:
                    if menu_state == "grid_size":
                        n = max(4, n - 1)
                    elif menu_state == "game_mode":
                        mode = 1
                    elif menu_state == "difficulty":
                        difficulty = max(1, difficulty - 1)
                elif event.key == pygame.K_RIGHT:
                    if menu_state == "grid_size":
                        n = min(12, n + 1)
                    elif menu_state == "game_mode":
                        mode = 2
                    elif menu_state == "difficulty":
                        difficulty = min(3, difficulty + 1)
                elif event.key == pygame.K_RETURN:
                    if menu_state == "grid_size":
                        menu_state = "win_condition"
                    elif menu_state == "win_condition":
                        menu_state = "game_mode"
                    elif menu_state == "game_mode":
                        if mode == 1:
                            player_names = ["", ""]
                            menu_state = "player1_name"
                            input_active = True
                        else:
                            player_names = ["", "AI"]
                            menu_state = "player_name"
                            input_active = True
                            difficulty = 2  # Default to medium
                    elif menu_state == "difficulty":
                        menu_state = "ready"
                    elif menu_state == "ready":
                        return  # Exit menu and start game
                elif event.key == pygame.K_ESCAPE:
                    if menu_state in ["player1_name", "player2_name", "player_name"]:
                        input_active = False
                        input_text = ""

        # Draw menu
        menu_screen.fill(BLACK)

        # Animated background
        time_offset = pygame.time.get_ticks() * 0.001
        for y in range(600):
            wave = math.sin(y * 0.01 + time_offset) * 0.1
            ratio = (y / 600 + wave * 0.05) % 1.0
            r = int(BLUE[0] * (1 - ratio) + DARK_BLUE[0] * ratio)
            g = int(BLUE[1] * (1 - ratio) + DARK_BLUE[1] * ratio)
            b = int(BLUE[2] * (1 - ratio) + DARK_BLUE[2] * ratio)
            pygame.draw.line(menu_screen, (r, g, b), (0, y), (800, y))

        # Title
        title_text = pygame.font.SysFont("monospace", 48).render("CONNECT-N SETUP", True, WHITE)
        title_x = center_x - title_text.get_width() // 2
        menu_screen.blit(title_text, (title_x, 50))

        y_offset = 120

        if menu_state == "grid_size":
            # Grid Size Configuration
            subtitle = pygame.font.SysFont("monospace", 24).render("Configure Grid Size", True, LIGHT_BLUE)
            menu_screen.blit(subtitle, (center_x - subtitle.get_width() // 2, y_offset))

            y_offset += 60

            # Columns with interactive controls
            col_text = pygame.font.SysFont("monospace", 20).render(f"Columns: {n}", True, WHITE)
            menu_screen.blit(col_text, (center_x - 150, y_offset))

            # Left/Right arrows
            left_arrow = pygame.font.SysFont("monospace", 20).render("←", True, YELLOW if n > 4 else GRAY)
            menu_screen.blit(left_arrow, (center_x + 80, y_offset))
            right_arrow = pygame.font.SysFont("monospace", 20).render("→", True, YELLOW if n < 12 else GRAY)
            menu_screen.blit(right_arrow, (center_x + 120, y_offset))

            y_offset += 40

            # Rows
            row_text = pygame.font.SysFont("monospace", 20).render(f"Rows: {k}", True, WHITE)
            menu_screen.blit(row_text, (center_x - 150, y_offset))

            # Up/Down arrows
            up_arrow = pygame.font.SysFont("monospace", 20).render("↑", True, YELLOW if k < 12 else GRAY)
            menu_screen.blit(up_arrow, (center_x + 100, y_offset))
            down_arrow = pygame.font.SysFont("monospace", 20).render("↓", True, YELLOW if k > 4 else GRAY)
            menu_screen.blit(down_arrow, (center_x + 100, y_offset + 20))

            y_offset += 60
            next_text = small_font.render("Press ENTER to continue", True, GRAY)
            menu_screen.blit(next_text, (center_x - next_text.get_width() // 2, y_offset))

        elif menu_state == "win_condition":
            # Winning Condition
            subtitle = pygame.font.SysFont("monospace", 24).render("Winning Condition", True, LIGHT_BLUE)
            menu_screen.blit(subtitle, (center_x - subtitle.get_width() // 2, y_offset))

            y_offset += 60

            win_text = pygame.font.SysFont("monospace", 20).render(f"Connect {CONNECT_N} pieces to win", True, WHITE)
            menu_screen.blit(win_text, (center_x - win_text.get_width() // 2, y_offset))

            y_offset += 40

            # Up/Down arrows
            up_arrow = pygame.font.SysFont("monospace", 20).render("↑", True, YELLOW if CONNECT_N < min(n, k) else GRAY)
            menu_screen.blit(up_arrow, (center_x - 20, y_offset))
            down_arrow = pygame.font.SysFont("monospace", 20).render("↓", True, YELLOW if CONNECT_N > 3 else GRAY)
            menu_screen.blit(down_arrow, (center_x - 20, y_offset + 20))

            y_offset += 60
            next_text = small_font.render("Press ENTER to continue", True, GRAY)
            menu_screen.blit(next_text, (center_x - next_text.get_width() // 2, y_offset))

        elif menu_state == "game_mode":
            # Game Mode Selection
            subtitle = pygame.font.SysFont("monospace", 24).render("Choose Game Mode", True, LIGHT_BLUE)
            menu_screen.blit(subtitle, (center_x - subtitle.get_width() // 2, y_offset))

            y_offset += 60

            pvp_color = GREEN if mode == 1 else WHITE
            pvp_text = pygame.font.SysFont("monospace", 20).render("1. Player vs Player", True, pvp_color)
            menu_screen.blit(pvp_text, (center_x - pvp_text.get_width() // 2, y_offset))

            y_offset += 40

            pvai_color = GREEN if mode == 2 else WHITE
            pvai_text = pygame.font.SysFont("monospace", 20).render("2. Player vs AI", True, pvai_color)
            menu_screen.blit(pvai_text, (center_x - pvai_text.get_width() // 2, y_offset))

            y_offset += 60

            # Left/Right arrows
            left_arrow = pygame.font.SysFont("monospace", 20).render("←", True, YELLOW)
            menu_screen.blit(left_arrow, (center_x - 40, y_offset))
            right_arrow = pygame.font.SysFont("monospace", 20).render("→", True, YELLOW)
            menu_screen.blit(right_arrow, (center_x + 20, y_offset))

            y_offset += 40
            next_text = small_font.render("Press ENTER to continue", True, GRAY)
            menu_screen.blit(next_text, (center_x - next_text.get_width() // 2, y_offset))

        elif menu_state in ["player1_name", "player2_name", "player_name"]:
            # Player Name Input
            if menu_state == "player1_name":
                prompt = "Enter Player 1 Name:"
                current_name = input_text
            elif menu_state == "player2_name":
                prompt = "Enter Player 2 Name:"
                current_name = input_text
            else:  # player_name
                prompt = "Enter Your Name:"
                current_name = input_text

            subtitle = pygame.font.SysFont("monospace", 24).render(prompt, True, LIGHT_BLUE)
            menu_screen.blit(subtitle, (center_x - subtitle.get_width() // 2, y_offset))

            y_offset += 60

            # Input box with better styling
            input_bg = pygame.Rect(center_x - 150, y_offset, 300, 40)
            pygame.draw.rect(menu_screen, DARK_BLUE, input_bg)
            pygame.draw.rect(menu_screen, LIGHT_BLUE, input_bg, 2)

            if input_active:
                pygame.draw.rect(menu_screen, YELLOW, input_bg, 2)

            name_text = pygame.font.SysFont("monospace", 20).render(current_name, True, WHITE)
            menu_screen.blit(name_text, (center_x - 140, y_offset + 8))

            if input_active:
                # Blinking cursor
                cursor_x = center_x - 140 + name_text.get_width()
                if pygame.time.get_ticks() % 1000 < 500:
                    pygame.draw.line(menu_screen, WHITE, (cursor_x, y_offset + 5), (cursor_x, y_offset + 35), 2)

            y_offset += 60
            enter_text = small_font.render("Press ENTER to confirm, ESC to cancel", True, GRAY)
            menu_screen.blit(enter_text, (center_x - enter_text.get_width() // 2, y_offset))

        elif menu_state == "difficulty":
            # AI Difficulty Selection
            subtitle = pygame.font.SysFont("monospace", 24).render("Choose AI Difficulty", True, LIGHT_BLUE)
            menu_screen.blit(subtitle, (center_x - subtitle.get_width() // 2, y_offset))

            y_offset += 60

            difficulties = ["Easy", "Medium", "Hard"]
            descriptions = [
                "Relaxed gameplay with occasional strategy",
                "Balanced challenge with solid AI",
                "Expert-level play with advanced tactics"
            ]

            for i, (diff_name, desc) in enumerate(zip(difficulties, descriptions)):
                color = GREEN if difficulty == i + 1 else WHITE
                diff_text = pygame.font.SysFont("monospace", 20).render(f"{i+1}. {diff_name}", True, color)
                menu_screen.blit(diff_text, (center_x - 150, y_offset))

                desc_text = small_font.render(desc, True, GRAY)
                menu_screen.blit(desc_text, (center_x - 140, y_offset + 25))

                y_offset += 60

            # Left/Right arrows
            left_arrow = pygame.font.SysFont("monospace", 20).render("←", True, YELLOW if difficulty > 1 else GRAY)
            menu_screen.blit(left_arrow, (center_x + 100, y_offset - 120))
            right_arrow = pygame.font.SysFont("monospace", 20).render("→", True, YELLOW if difficulty < 3 else GRAY)
            menu_screen.blit(right_arrow, (center_x + 140, y_offset - 120))

            y_offset += 20
            next_text = small_font.render("Press ENTER to continue", True, GRAY)
            menu_screen.blit(next_text, (center_x - next_text.get_width() // 2, y_offset))

        elif menu_state == "ready":
            # Ready to start
            subtitle = pygame.font.SysFont("monospace", 24).render("Game Configuration Complete!", True, GREEN)
            menu_screen.blit(subtitle, (center_x - subtitle.get_width() // 2, y_offset))

            y_offset += 60

            # Display final settings with better formatting
            settings = [
                f"Grid Size: {n} x {k}",
                f"Win Condition: Connect {CONNECT_N}",
                f"Game Mode: {'Player vs Player' if mode == 1 else 'Player vs AI'}",
                f"Players: {player_names[0]} vs {player_names[1]}"
            ]

            if mode == 2:
                diff_names = ["Easy", "Medium", "Hard"]
                settings.append(f"AI Difficulty: {diff_names[difficulty-1]}")

            for setting in settings:
                setting_text = pygame.font.SysFont("monospace", 18).render(setting, True, WHITE)
                menu_screen.blit(setting_text, (center_x - setting_text.get_width() // 2, y_offset))
                y_offset += 30

            y_offset += 40
            start_text = pygame.font.SysFont("monospace", 24).render("Press ENTER to Start Game!", True, YELLOW)
            menu_screen.blit(start_text, (center_x - start_text.get_width() // 2, y_offset))

        # Instructions at bottom
        instr_y = 550
        instr_texts = [
            "Use arrow keys to navigate • ENTER to confirm • ESC to cancel input",
            "↑↓: Adjust values • ←→: Switch options"
        ]

        for i, instr in enumerate(instr_texts):
            instr_text = small_font.render(instr, True, LIGHT_GRAY)
            menu_screen.blit(instr_text, (center_x - instr_text.get_width() // 2, instr_y + i * 20))

        pygame.display.update()
        pygame.time.wait(50)  # Prevent excessive CPU usage

# Show setup menu first
show_setup_menu()
WIDTH = n * SQUARESIZE
HEIGHT = (k + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Connect-N Enhanced Edition')

# Load fonts
font = pygame.font.SysFont("monospace", FONT_SIZE)
title_font = pygame.font.SysFont("monospace", 48)
subtitle_font = pygame.font.SysFont("monospace", 24)

# Show intro animation
def show_intro():
    start_time = pygame.time.get_ticks()
    intro_duration = 3000  # 3 seconds

    while pygame.time.get_ticks() - start_time < intro_duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw gradient background
        draw_gradient_background(screen)

        # Animated title
        time_elapsed = pygame.time.get_ticks() - start_time
        alpha = min(255, time_elapsed // 10)  # Fade in effect

        # Title with glow effect
        title_text = title_font.render("CONNECT-N", True, WHITE)
        title_shadow = title_font.render("CONNECT-N", True, (0, 0, 0, alpha//4))

        title_x = WIDTH // 2 - title_text.get_width() // 2
        title_y = HEIGHT // 2 - 100

        # Draw title shadow/glow
        for offset in range(3, 0, -1):
            glow_color = (alpha // (offset + 1), alpha // (offset + 1), alpha // (offset + 1))
            glow_text = title_font.render("CONNECT-N", True, glow_color)
            screen.blit(glow_text, (title_x + offset, title_y + offset))

        screen.blit(title_text, (title_x, title_y))

        # Subtitle
        subtitle_text = subtitle_font.render("Enhanced Edition", True, LIGHT_BLUE)
        subtitle_x = WIDTH // 2 - subtitle_text.get_width() // 2
        subtitle_y = HEIGHT // 2 - 20
        screen.blit(subtitle_text, (subtitle_x, subtitle_y))

        # Animated dots
        dots = "." * ((time_elapsed // 500) % 4)
        loading_text = subtitle_font.render(f"Loading{dots}", True, WHITE)
        loading_x = WIDTH // 2 - loading_text.get_width() // 2
        loading_y = HEIGHT // 2 + 60
        screen.blit(loading_text, (loading_x, loading_y))

        pygame.display.update()
        pygame.time.wait(50)

def show_game_over_screen(winner_text):
    """Show an attractive game over screen"""
    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < 2500:  # 2.5 seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw gradient background
        draw_gradient_background(screen)

        # Game Over text
        game_over_text = title_font.render("GAME OVER", True, WHITE)
        winner_surface = subtitle_font.render(winner_text, True, GREEN if "Wins" in winner_text else YELLOW)

        # Center the text
        go_x = WIDTH // 2 - game_over_text.get_width() // 2
        go_y = HEIGHT // 2 - 80
        winner_x = WIDTH // 2 - winner_surface.get_width() // 2
        winner_y = HEIGHT // 2 - 10

        # Draw with glow effect
        for offset in range(2, 0, -1):
            glow_color = (100 // offset, 100 // offset, 100 // offset)
            glow_go = title_font.render("GAME OVER", True, glow_color)
            screen.blit(glow_go, (go_x + offset, go_y + offset))

        screen.blit(game_over_text, (go_x, go_y))
        screen.blit(winner_surface, (winner_x, winner_y))

        # Animated celebration particles
        time_elapsed = pygame.time.get_ticks() - start_time
        if time_elapsed > 500:  # Start particles after half second
            particle_x = WIDTH // 2 + math.sin(time_elapsed * 0.01) * 100
            particle_y = HEIGHT // 2 + math.cos(time_elapsed * 0.008) * 50
            pygame.draw.circle(screen, random.choice([RED, YELLOW, GREEN, LIGHT_BLUE]),
                             (int(particle_x), int(particle_y)), 5)

        pygame.display.update()
        pygame.time.wait(30)

show_intro()

game_over = False
turn = 0
board = create_board()
hovering_col = None
particles = None  # Will be created on win
clock = pygame.time.Clock()
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.MOUSEMOTION:
            x_pos = event.pos[0]
            # Ensure column detection is within valid range
            if 0 <= x_pos < WIDTH:
                hovering_col = int(x_pos // SQUARESIZE)
                # Clamp to valid column range
                hovering_col = max(0, min(n - 1, hovering_col))
            else:
                hovering_col = None
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            # Only allow player input when it's their turn (turn 0 for PvP, or when it's player's turn in PvAI)
            if mode == 1 or (mode == 2 and turn == 0):
                if hovering_col is not None and is_valid_location(board, hovering_col):
                    row = get_next_open_row(board, hovering_col)
                    drop_piece(board, row, hovering_col, 1 if turn == 0 else 2)
                    win, winning_positions = winning_move(board, 1 if turn == 0 else 2)
                    if win:
                        particles = create_particles()  # Create victory particles
                        game_over = True
                    elif np.all(board != 0):
                        game_over = True
                    turn = (turn + 1) % 2

    if mode == 2 and turn == 1 and not game_over:
        pygame.time.wait(800)  # AI thinking delay
        valid_locations = [c for c in range(n) if is_valid_location(board, c)]
        if difficulty == 1:
            col = random.choice(valid_locations)
        elif difficulty == 2:
            _, col = minimax(board, 3, -math.inf, math.inf, True)
        elif difficulty == 3:
            _, col = minimax(board, 7, -math.inf, math.inf, True)
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, 2)
        win, winning_positions = winning_move(board, 2)
        if win:
            particles = create_particles()  # Create victory particles
            game_over = True
        elif np.all(board != 0):
            game_over = True
        turn = 0

    # Update particles if they exist
    if particles:
        update_particles(particles)

    # Draw everything
    if game_over and particles:
        # Victory animation with particles
        for _ in range(180):  # 3 seconds at 60 FPS
            update_particles(particles)
            draw_board(board, screen, hovering_col, font, player_names, winning_positions, particles)
            clock.tick(60)
    elif game_over:
        # Game over screen
        winner_name = player_names[turn] if 'winning_positions' in locals() and winning_positions else "It's a Draw!"
        show_game_over_screen(winner_name)
    elif not game_over:
        draw_board(board, screen, hovering_col, font, player_names)

    clock.tick(60)  # 60 FPS

pygame.time.wait(1000)
pygame.quit()