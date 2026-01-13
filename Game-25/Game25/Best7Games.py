import random
import time
import pygame
import sys
import os
import threading
import msvcrt  # For Windows keyboard input; on Unix, you'd need `curses`
import math

# Track how many times each game is played
play_counts = {
    "Memory Puzzle": 0,
    "Battleship": 0,
    "Hangman": 0,
    "Flappy Bird": 0,
    "Jigsaw Puzzle": 0,
    "Pac-Man": 0,
    "Space Invaders": 0
}

# --- Clear Screen Function ---
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- Loading/Transition Animation ---
def loading(text="Loading"):
    for i in range(3):
        print(f"{text}{'.' * (i+1)}", end="\r")
        time.sleep(0.3)
    clear_screen()

# --- Placeholder Game ---
def placeholder_game(game_name):
    clear_screen()
    print(f"🚧 {game_name} is under construction.")
    print("🛠️ Stay tuned – it will be available soon!")
    time.sleep(2)

# --- Game Functions ---
# Define each game's function here (e.g., def snake_game():, def tetris_game():, etc.)

# --- Game 1: Memory Puzzle ---
def memory_puzzle():
    clear_screen()
    print("🧠 Welcome to Memory Puzzle!")

    # Create pairs of letters (A-H) for a 4x4 grid (8 pairs)
    pairs = list("AABBCCDDEEFFGGHH")
    random.shuffle(pairs)

    grid_size = 4
    board = [pairs[i*grid_size:(i+1)*grid_size] for i in range(grid_size)]
    revealed = [[False]*grid_size for _ in range(grid_size)]
    
    def display_board():
        print("\n   " + "  ".join(str(i+1) for i in range(grid_size)))
        for idx, row in enumerate(revealed):
            row_display = []
            for jdx, card_revealed in enumerate(row):
                if card_revealed:
                    row_display.append(board[idx][jdx])
                else:
                    row_display.append("*")
            print(chr(65+idx) + "  " + "  ".join(row_display))
    
    def parse_input(pos):
        if len(pos) != 2:
            return None
        row = ord(pos[0].upper()) - 65
        col = int(pos[1]) - 1
        if 0 <= row < grid_size and 0 <= col < grid_size:
            return row, col
        return None
    
    matched_pairs = 0
    attempts = 0
    
    while matched_pairs < (grid_size * grid_size) // 2:
        display_board()
        print(f"\nAttempts: {attempts}")
        first = input("Pick the first card (e.g., A1): ").strip()
        pos1 = parse_input(first)
        if not pos1 or revealed[pos1[0]][pos1[1]]:
            print("❗ Invalid or already revealed position.")
            continue
        
        revealed[pos1[0]][pos1[1]] = True
        clear_screen()
        print("🧠 Welcome to Memory Puzzle!")
        display_board()

        second = input("Pick the second card (e.g., B3): ").strip()
        pos2 = parse_input(second)
        if not pos2 or revealed[pos2[0]][pos2[1]] or pos2 == pos1:
            print("❗ Invalid or already revealed position.")
            revealed[pos1[0]][pos1[1]] = False
            continue
        
        revealed[pos2[0]][pos2[1]] = True
        clear_screen()
        print("🧠 Welcome to Memory Puzzle!")
        display_board()

        attempts += 1
        
        if board[pos1[0]][pos1[1]] == board[pos2[0]][pos2[1]]:
            print("🎉 It's a match!")
            matched_pairs += 1
        else:
            print("❌ Not a match.")
            time.sleep(2)
            revealed[pos1[0]][pos1[1]] = False
            revealed[pos2[0]][pos2[1]] = False
        
        clear_screen()
        print("🧠 Welcome to Memory Puzzle!")

    print(f"🏆 Congratulations! You matched all pairs in {attempts} attempts.")


# --- Game 2: Battleship ---
def battleship():
    clear_screen()
    print("🚢 Welcome to Battleship!")
    print("Try to find and sink the enemy ship hidden on the grid.")

    size = 5
    board = [["~"] * size for _ in range(size)]
    ship_row = random.randint(0, size - 1)
    ship_col = random.randint(0, size - 1)
    attempts = 0
    max_attempts = 10

    def print_board(show_ship=False):
        print("  " + " ".join(str(i+1) for i in range(size)))
        for r in range(size):
            row_display = []
            for c in range(size):
                if show_ship and r == ship_row and c == ship_col:
                    row_display.append("S")
                else:
                    row_display.append(board[r][c])
            print(chr(65 + r) + " " + " ".join(row_display))

    while attempts < max_attempts:
        print_board()
        print(f"\nAttempts left: {max_attempts - attempts}")
        move = input("Enter your guess (e.g., A3) or 'quit' to exit: ").strip().upper()
        if move.lower() == "quit":
            print("👋 Thanks for playing Battleship!")
            break
        if len(move) < 2 or not move[0].isalpha() or not move[1:].isdigit():
            print("❗ Invalid input. Use format like A3.")
            time.sleep(1)
            clear_screen()
            print("🚢 Welcome to Battleship!")
            continue
        row = ord(move[0]) - 65
        col = int(move[1:]) - 1
        if not (0 <= row < size and 0 <= col < size):
            print("❗ Coordinates out of range.")
            time.sleep(1)
            clear_screen()
            print("🚢 Welcome to Battleship!")
            continue
        if board[row][col] != "~":
            print("⚠️ You already guessed that spot!")
            time.sleep(1)
            clear_screen()
            print("🚢 Welcome to Battleship!")
            continue

        attempts += 1
        if row == ship_row and col == ship_col:
            board[row][col] = "X"
            clear_screen()
            print("🚢 Welcome to Battleship!")
            print_board(show_ship=True)
            print("\n🎉 Hit! You sank the enemy ship! You win!")
            break
        else:
            board[row][col] = "O"
            print("\n❌ Miss!")
            time.sleep(1)
            clear_screen()
            print("🚢 Welcome to Battleship!")

    else:
        print_board(show_ship=True)
        print("\n💥 Game Over! You ran out of attempts.")
        print(f"The ship was at {chr(ship_row + 65)}{ship_col + 1}.")


# --- Game 3: Hangman ---
def hangman():
    clear_screen()
    print("💀 Welcome to Hangman!")
    
    words = ["python", "programming", "hangman", "challenge", "developer"]
    word = random.choice(words)
    guessed_letters = set()
    attempts_left = 6
    
    def display_word():
        displayed = " ".join(letter if letter in guessed_letters else "_" for letter in word)
        print("\nWord: " + displayed)
    
    while attempts_left > 0:
        display_word()
        print(f"Attempts left: {attempts_left}")
        guess = input("Guess a letter: ").strip().lower()
        
        if len(guess) != 1 or not guess.isalpha():
            print("❗ Please enter a single letter.")
            continue
        
        if guess in guessed_letters:
            print("⚠️ You already guessed that letter.")
            continue
        
        guessed_letters.add(guess)
        
        if guess in word:
            print("✅ Good guess!")
        else:
            print("❌ Wrong guess.")
            attempts_left -= 1
        
        if all(letter in guessed_letters for letter in word):
            display_word()
            print("\n🎉 Congratulations! You guessed the word!")
            break
        time.sleep(1)
    else:
        print(f"\n😢 Game over! The word was '{word}'.")
    

# --- Game 4: Flappy Bird ---
def flappy_bird():
    pygame.init()

    WIDTH, HEIGHT = 400, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🐦 Flappy Bird")

    clock = pygame.time.Clock()
    FONT = pygame.font.SysFont(None, 40)

    GRAVITY = 0.5
    BIRD_JUMP = -10

    bird_x = 50
    bird_y = HEIGHT // 2
    bird_vel = 0

    PIPE_WIDTH = 70
    PIPE_GAP = 150
    pipe_speed = 3

    # Start with two pipes
    pipes = []
    def add_pipe():
        height = random.randint(100, HEIGHT - 100 - PIPE_GAP)
        pipes.append({"x": WIDTH, "height": height})

    add_pipe()
    add_pipe()
    pipes[1]["x"] += WIDTH // 2 + PIPE_WIDTH

    score = 0
    running = True

    while running:
        screen.fill((135, 206, 235))  # Sky blue background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_vel = BIRD_JUMP

        # Bird physics
        bird_vel += GRAVITY
        bird_y += bird_vel

        # Draw bird
        bird_rect = pygame.Rect(bird_x, bird_y, 30, 30)
        pygame.draw.ellipse(screen, (255, 255, 0), bird_rect)  # Yellow bird

        # Move pipes
        for pipe in pipes:
            pipe["x"] -= pipe_speed
            # Draw top pipe
            top_rect = pygame.Rect(pipe["x"], 0, PIPE_WIDTH, pipe["height"])
            pygame.draw.rect(screen, (34, 139, 34), top_rect)  # Green pipe
            # Draw bottom pipe
            bottom_rect = pygame.Rect(pipe["x"], pipe["height"] + PIPE_GAP, PIPE_WIDTH, HEIGHT - pipe["height"] - PIPE_GAP)
            pygame.draw.rect(screen, (34, 139, 34), bottom_rect)

        # Remove pipes that are off-screen & add new ones
        if pipes and pipes[0]["x"] < -PIPE_WIDTH:
            pipes.pop(0)
            add_pipe()
            score += 1

        # Collision detection
        for pipe in pipes:
            top_rect = pygame.Rect(pipe["x"], 0, PIPE_WIDTH, pipe["height"])
            bottom_rect = pygame.Rect(pipe["x"], pipe["height"] + PIPE_GAP, PIPE_WIDTH, HEIGHT - pipe["height"] - PIPE_GAP)
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                print("💥 You hit a pipe! Game Over.")
                time.sleep(2)
                running = False

        # Check ground and ceiling collision
        if bird_y > HEIGHT - 30 or bird_y < 0:
            print("💥 You hit the ground or ceiling! Game Over.")
            time.sleep(2)
            running = False

        # Display score
        score_surface = FONT.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_surface, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


# --- Game 5: Jigsaw Puzzle ---
def jigsaw_puzzle():
    clear_screen()
    print("🧩 Welcome to Jigsaw Puzzle!")

    # For simplicity, use a small 3x3 puzzle represented by numbers 1-9 shuffled
    puzzle_size = 3
    pieces = list(range(1, puzzle_size * puzzle_size + 1))
    random.shuffle(pieces)

    # We'll simulate the puzzle as a shuffled list, user must reorder pieces to sorted order
    def display_pieces(pieces_list):
        for i in range(puzzle_size):
            row = pieces_list[i*puzzle_size:(i+1)*puzzle_size]
            print(" ".join(str(p).rjust(2) for p in row))

    print("\nThe puzzle pieces are shuffled:")
    display_pieces(pieces)

    print("\nYour goal: Arrange the pieces in ascending order (1 to 9).")
    print("You will swap two pieces by their positions (1-9).")

    while True:
        display_pieces(pieces)
        try:
            swap_input = input("Enter two positions to swap (e.g., '3 7'): ").strip()
            pos1, pos2 = map(int, swap_input.split())
            if not (1 <= pos1 <= 9 and 1 <= pos2 <= 9):
                print("Positions must be between 1 and 9.")
                continue
            # Swap pieces
            pieces[pos1 - 1], pieces[pos2 - 1] = pieces[pos2 - 1], pieces[pos1 - 1]
        except Exception:
            print("Invalid input. Please enter two numbers separated by space.")
            continue

        if pieces == list(range(1, 10)):
            clear_screen()
            display_pieces(pieces)
            print("\n🎉 Congratulations! You solved the puzzle!")
            break


# --- Game 6: Pac-Man ---
def pacman():
    clear_screen()
    print("🟡 Welcome to Pac-Man!")

    WIDTH, HEIGHT = 20, 10
    walls = "#"
    empty = " "
    dot = "."
    pacman_char = "P"
    ghost_char = "G"

    maze_layout = [
        "####################",
        "#........#.........#",
        "#.####.#.#.####.#..#",
        "#..................#",
        "#.####.#.####.#.####",
        "#..................#",
        "#.####.#.####.#.####",
        "#........#.........#",
        "#........#.........#",
        "####################"
    ]

    board = [list(row) for row in maze_layout]
    pacman_pos = [1, 1]
    ghost_pos = [8, 18]
    score = 0
    max_score = sum(row.count(dot) for row in board)

    def draw_board():
        clear_screen()
        print(f"Score: {score}/{max_score}\n")
        for r in range(HEIGHT):
            row = ""
            for c in range(WIDTH):
                if [r, c] == pacman_pos:
                    row += pacman_char
                elif [r, c] == ghost_pos:
                    row += ghost_char
                else:
                    row += board[r][c]
            print(row)

    def move(pos, direction):
        r, c = pos
        if direction == 'up':
            r -= 1
        elif direction == 'down':
            r += 1
        elif direction == 'left':
            c -= 1
        elif direction == 'right':
            c += 1
        if 0 <= r < HEIGHT and 0 <= c < WIDTH and board[r][c] != walls:
            return [r, c]
        return pos

    def ghost_move():
        # Try to move ghost randomly to open adjacent space
        directions = ['up', 'down', 'left', 'right']
        random.shuffle(directions)
        for d in directions:
            new_pos = move(ghost_pos, d)
            if new_pos != ghost_pos:
                return new_pos
        return ghost_pos

    print("Controls: W = up, A = left, S = down, D = right, Q = quit")
    time.sleep(2)

    while True:
        draw_board()
        if pacman_pos == ghost_pos:
            print("💀 Game Over! The ghost caught you.")
            break
        if score == max_score:
            print("🏆 Congratulations! You ate all the dots!")
            break

        key = None
        if os.name == 'nt':
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
        else:
            # For non-Windows, you might want to use a library like 'getch' or 'curses' 
            # This placeholder will just wait for input (blocking)
            print("Enter move (WASD to move, Q to quit): ", end='', flush=True)
            key = sys.stdin.read(1).lower()

        if key:
            if key == 'w':
                pacman_pos = move(pacman_pos, 'up')
            elif key == 'a':
                pacman_pos = move(pacman_pos, 'left')
            elif key == 's':
                pacman_pos = move(pacman_pos, 'down')
            elif key == 'd':
                pacman_pos = move(pacman_pos, 'right')
            elif key == 'q':
                print("👋 Thanks for playing Pac-Man!")
                break

        r, c = pacman_pos
        if board[r][c] == dot:
            board[r][c] = empty
            score += 1

        ghost_pos = ghost_move()

        time.sleep(0.15)
        

# --- Game 7: Space Invaders ---
def space_invaders():
    pygame.init()
    
    # Screen setup
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("👾 Space Invaders")
    
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    
    # Player
    player_img = pygame.Surface((50, 30))
    player_img.fill(GREEN)
    player_x = WIDTH // 2 - 25
    player_y = HEIGHT - 60
    player_speed = 5
    
    # Bullet
    bullet_img = pygame.Surface((5, 15))
    bullet_img.fill(WHITE)
    bullet_x = 0
    bullet_y = player_y
    bullet_speed = 10
    bullet_state = "ready"  # "ready" or "fire"
    
    # Enemy
    enemy_img = pygame.Surface((40, 30))
    enemy_img.fill(RED)
    enemy_speed = 3
    enemy_list = []
    num_enemies = 6
    
    for i in range(num_enemies):
        x = random.randint(0, WIDTH - 40)
        y = random.randint(50, 150)
        enemy_list.append([x, y, enemy_speed])
    
    score = 0
    font = pygame.font.Font(None, 36)
    
    clock = pygame.time.Clock()
    running = True
    
    def show_score():
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
    
    def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
        distance = math.sqrt((enemy_x - bullet_x)**2 + (enemy_y - bullet_y)**2)
        return distance < 27  # collision threshold
    
    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        # Move player left/right
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
            player_x += player_speed
        # Fire bullet
        if keys[pygame.K_SPACE]:
            if bullet_state == "ready":
                bullet_x = player_x + 22
                bullet_y = player_y
                bullet_state = "fire"
        
        # Bullet movement
        if bullet_state == "fire":
            screen.blit(bullet_img, (bullet_x, bullet_y))
            bullet_y -= bullet_speed
            if bullet_y < 0:
                bullet_state = "ready"
        
        # Enemy movement
        for enemy in enemy_list:
            enemy[0] += enemy[2]
            # Change direction at edges
            if enemy[0] <= 0 or enemy[0] >= WIDTH - 40:
                enemy[2] *= -1
                enemy[1] += 40  # move down
            
            # Check collision with bullet
            if is_collision(enemy[0], enemy[1], bullet_x, bullet_y):
                score += 1
                bullet_state = "ready"
                bullet_y = player_y
                enemy[0] = random.randint(0, WIDTH - 40)
                enemy[1] = random.randint(50, 150)
            
            # Check if enemy reached player level
            if enemy[1] > player_y - 30:
                running = False
                break
            
            screen.blit(enemy_img, (enemy[0], enemy[1]))
        
        screen.blit(player_img, (player_x, player_y))
        show_score()
        
        pygame.display.flip()
        clock.tick(60)
    
    # Game over screen
    screen.fill(BLACK)
    game_over_font = pygame.font.Font(None, 64)
    game_over_text = game_over_font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 32))
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    


# --- Game Instructions ---
def show_instructions(game_name):
    clear_screen()
    instructions = {
        "Memory Puzzle": """
        🧠 Memory Puzzle Instructions:
        - Flip two cards at a time to find matching pairs.
        - Remember the positions of cards to match them.
        """,
        "Battleship": """
        🚢 Battleship Instructions:
        - Place your ships on a grid.
        - Take turns to guess the locations of the opponent's ships.
        - Sink all opponent ships to win.
        """,
        "Hangman": """
        💀 Hangman Instructions:
        - Guess letters to reveal the hidden word.
        - Each incorrect guess brings you closer to losing.
        """,
        "Flappy Bird": """
        🐦 Flappy Bird Instructions:
        - Press space to make the bird flap.
        - Avoid pipes to stay alive.
        """,
        "Jigsaw Puzzle": """
        🧩 Jigsaw Puzzle Instructions:
        - Arrange pieces to form the complete image.
        - Complete the puzzle to win.
        """,
        "Pac-Man": """
        🟡 Pac-Man Instructions:
        - Move Pac-Man to eat dots.
        - Avoid ghosts to stay alive.
        """,
        "Space Invaders": """
        👾 Space Invaders Instructions:
        - Move your ship to shoot aliens.
        - Destroy all aliens to win.
        """
    }
    print(f"📘 Instructions for {game_name}:\n")
    print(instructions.get(game_name, "🚧 No instructions available for this game."))
    input("\n🔙 Press Enter to return to the menu...")
    clear_screen()
    
# --- Play Game ---
def play_game(game_func):
    while True:
        loading("Starting Game")
        game_func()
        print("\n🔁 What would you like to do next?")
        print("1. 🔄 Restart Game")
        print("2. 🔙 Return to Main Menu")
        print("3. ❌ Exit")
        choice = input("Your choice: ").strip()
        if choice == '1':
            continue
        elif choice == '2':
            break
        elif choice == '3':
            print("👋 Exiting...")
            time.sleep(1)
            sys.exit()
        else:
            print("❗ Invalid input. Returning to menu.")
            time.sleep(1)
            break

# --- Game Mapping ---
game_functions = {
    "Memory Puzzle": memory_puzzle,
    "Battleship": battleship,
    "Hangman": hangman,
    "Flappy Bird": flappy_bird,
    "Jigsaw Puzzle": jigsaw_puzzle,
    "Pac-Man": pacman,
    "Space Invaders": space_invaders
    #"Memory Match": lambda: placeholder_game("Memory Match")
}

# --- Game Menu ---
def game_menu():
    while True:
        clear_screen()
        print("╔════════════════════════════╗")
        print("🎮  PYTHON MINI GAMES MENU  🎮")
        print("╚════════════════════════════╝")
        for i, game in enumerate(play_counts.keys(), 1):
            print(f"{i:2}. {game} (played {play_counts[game]} times)")
        print(f"{len(play_counts)+1:2}. 📘 View Instructions")
        print(f"{len(play_counts)+2:2}. ❌ Exit")
        print("──────────────────────────────")
        choice = input("🎯 Choose a game (1-{}): ".format(len(play_counts)+2)).strip()

        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(play_counts):
                game_name = list(play_counts.keys())[choice_num - 1]
                play_counts[game_name] += 1
                game_func = game_functions.get(game_name, lambda: placeholder_game(game_name))
                play_game(game_func)
            elif choice_num == len(play_counts) + 1:
                clear_screen()
                print("📘 GAME INSTRUCTIONS MENU 📘")
                for i, game in enumerate(play_counts.keys(), 1):
                    print(f"{i:2}. {game}")
                print(f"{len(play_counts)+1:2}. 🔙 Return to Main Menu")
                try:
                    instr_choice = int(input("Select a game number to view instructions: ").strip())
                    if 1 <= instr_choice <= len(play_counts):
                        game_name = list(play_counts.keys())[instr_choice - 1]
                        show_instructions(game_name)
                    elif instr_choice == len(play_counts) + 1:
                        continue
                    else:
                        print("❗ Invalid selection. Returning to main menu.")
                        time.sleep(1)
                except ValueError:
                    print("❗ Please enter a valid number.")
                    time.sleep(1)

            elif choice_num == len(play_counts) + 2:
                print("👋 Thanks for playing! See you again!")
                break
            else:
                print("❗ Invalid choice. Try again.")
                time.sleep(1)
        except ValueError:
            print("❗ Please enter a valid number.")
            time.sleep(1)
    
if __name__ == "__main__":
    game_menu()

