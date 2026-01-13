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
    "Dice Roller": 0,
    "Typing Test": 0,
    "Car Racing": 0,
    "Snake": 0,
    "Tic-Tac-Toe": 0,
    "Rock Paper Scissors": 0,
    "Memory Puzzle": 0,
    "2048": 0,
    "Minesweeper": 0,
    "Sudoku": 0,
    "Battleship": 0,
    "Hangman": 0,
    "Connect Four": 0,
    "Flappy Bird": 0,
    "Whack-a-Mole": 0,
    "Simon Says": 0,
    "Trivia Quiz": 0,
    "Math Quiz": 0,
    "Bingo": 0,
    "Jigsaw Puzzle": 0,
    "Word Search": 0,
    "Crossword Puzzle": 0,
    "Tetris": 0,
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

# --- Game 1: Dice Roller ---
def roll_dice():
    clear_screen()
    print("🎲 Welcome to Dice Roller 🎲")
    print("🔢 You can roll any dice with custom sides.")
    while True:
        try:
            sides = int(input("Enter number of sides on the dice: "))
            rolls = int(input("How many times to roll? "))
            print("\n🎯 Rolling...")
            for i in range(rolls):
                print(f"Roll {i+1}: 🎲 {random.randint(1, sides)}")
            break
        except ValueError:
            print("❗ Please enter valid numbers.")

# --- Game 2: Typing Speed Test ---
def typing_speed_test():
    clear_screen()
    test_text = "The quick brown fox jumps over the lazy dog."
    print("⌨️ Typing Speed Test ⌨️")
    print("👆 Type the sentence below as fast as you can:")
    print(f"\n📝 \"{test_text}\"\n")
    input("⏳ Press Enter to start...")
    clear_screen()
    print("Go!")
    start = time.time()
    typed = input("\nYour typing: ")
    end = time.time()
    elapsed = end - start
    words = len(typed.split())
    wpm = (words / elapsed) * 60 if elapsed > 0 else 0
    print("\n⌛ Time: {:.2f} seconds".format(elapsed))
    print("⚡ Words per minute (WPM): {:.2f}".format(wpm))

# --- Game 3: Car Racing ---
def car_racing_game():
    clear_screen()
    pygame.init()
    width, height = 500, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("🚗 Car Racing Game")
    WHITE, RED, BLUE = (255, 255, 255), (200, 0, 0), (0, 0, 200)
    car_width, car_height = 50, 100
    car_x = width // 2 - car_width // 2
    car_y = height - car_height - 10
    car_speed = 5
    obstacle_width, obstacle_height = 50, 50
    obstacle_x = random.randint(0, width - obstacle_width)
    obstacle_y = -obstacle_height
    obstacle_speed = 5
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 0:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < width - car_width:
            car_x += car_speed
        obstacle_y += obstacle_speed
        if obstacle_y > height:
            obstacle_y = -obstacle_height
            obstacle_x = random.randint(0, width - obstacle_width)
        car_rect = pygame.Rect(car_x, car_y, car_width, car_height)
        obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
        if car_rect.colliderect(obstacle_rect):
            print("💥 Crash! Game Over.")
            time.sleep(2)
            running = False
        pygame.draw.rect(screen, BLUE, (car_x, car_y, car_width, car_height))
        pygame.draw.rect(screen, RED, (obstacle_x, obstacle_y, obstacle_width, obstacle_height))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

# --- Game 4: Snake ---
def snake_game():
    clear_screen()
    pygame.init()
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("🐍 Snake Game")

    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)

    block_size = 20
    clock = pygame.time.Clock()
    speed = 10

    x, y = width // 2, height // 2
    dx, dy = block_size, 0  # Start moving to the right
    snake = [(x, y)]
    snake_length = 1

    food = (
        random.randrange(0, width - block_size, block_size),
        random.randrange(0, height - block_size, block_size)
    )

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -block_size, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = block_size, 0
                elif event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -block_size
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, block_size

        if not game_over:
            x += dx
            y += dy
            head = (x, y)

            if (
                x < 0 or x >= width or y < 0 or y >= height
                or head in snake
            ):
                game_over = True
            else:
                snake.append(head)
                if len(snake) > snake_length:
                    del snake[0]

                if head == food:
                    snake_length += 1
                    food = (
                        random.randrange(0, width - block_size, block_size),
                        random.randrange(0, height - block_size, block_size)
                    )

        screen.fill(WHITE)

        for segment in snake:
            pygame.draw.rect(screen, GREEN, (*segment, block_size, block_size))

        pygame.draw.rect(screen, RED, (*food, block_size, block_size))

        if game_over:
            font = pygame.font.SysFont(None, 48)
            msg = font.render("💀 Game Over!", True, (255, 0, 0))
            screen.blit(msg, (width // 2 - msg.get_width() // 2, height // 2 - msg.get_height() // 2))

        pygame.display.flip()
        clock.tick(speed)

        if game_over:
            pygame.time.wait(2000)
            break

    pygame.quit()


# --- Game 5: Tic-Tac-Toe ---
def tic_tac_toe():
    clear_screen()
    print("❌⭕ Welcome to Tic-Tac-Toe ⭕❌")

    board = [" " for _ in range(9)]

    def print_board():
        print("\n")
        for i in range(3):
            print(" " + " | ".join(board[i*3:(i+1)*3]))
            if i < 2:
                print("---|---|---")
        print("\n")

    def check_winner(player):
        wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        return any(all(board[i] == player for i in combo) for combo in wins)

    def is_draw():
        return all(cell != " " for cell in board)

    current_player = "X"
    while True:
        clear_screen()
        print("❌⭕ Tic-Tac-Toe ⭕❌")
        print_board()
        try:
            move = int(input(f"Player {current_player}, choose a cell (1-9): ")) - 1
            if board[move] == " ":
                board[move] = current_player
                if check_winner(current_player):
                    clear_screen()
                    print_board()
                    print(f"🎉 Player {current_player} wins!")
                    break
                elif is_draw():
                    clear_screen()
                    print_board()
                    print("🤝 It's a draw!")
                    break
                current_player = "O" if current_player == "X" else "X"
            else:
                print("❗ That cell is already taken. Try again.")
                time.sleep(1)
        except (ValueError, IndexError):
            print("❗ Invalid input. Enter a number between 1 and 9.")
            time.sleep(1)

# --- Game 6: Rock Paper Scissors ---
def rock_paper_scissors():
    clear_screen()
    print("✊✋✌️ Welcome to Rock Paper Scissors!")

    choices = ["rock", "paper", "scissors"]

    def determine_winner(player, computer):
        if player == computer:
            return "draw"
        elif (player == "rock" and computer == "scissors") or \
             (player == "paper" and computer == "rock") or \
             (player == "scissors" and computer == "paper"):
            return "player"
        else:
            return "computer"

    while True:
        print("\nChoose: rock, paper, or scissors")
        player_choice = input("👉 Your choice: ").strip().lower()

        if player_choice not in choices:
            print("❗ Invalid choice. Please choose rock, paper, or scissors.")
            continue

        computer_choice = random.choice(choices)
        print(f"🖥️ Computer chose: {computer_choice}")

        winner = determine_winner(player_choice, computer_choice)
        if winner == "draw":
            print("🤝 It's a draw!")
        elif winner == "player":
            print("🎉 You win!")
        else:
            print("💻 Computer wins!")
            break

# --- Game 7: Memory Puzzle ---
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
        display_board()

        second = input("Pick the second card (e.g., B3): ").strip()
        pos2 = parse_input(second)
        if not pos2 or revealed[pos2[0]][pos2[1]] or pos2 == pos1:
            print("❗ Invalid or already revealed position.")
            revealed[pos1[0]][pos1[1]] = False
            continue
        
        revealed[pos2[0]][pos2[1]] = True
        clear_screen()
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

    print(f"🏆 Congratulations! You matched all pairs in {attempts} attempts.")

# --- Game 8: 2048 ---
def game_2048():
    clear_screen()
    print("🧮 Welcome to 2048!")
    print("Use W (up), A (left), S (down), D (right) to move the tiles.\n")

    size = 4
    board = [[0]*size for _ in range(size)]

    def add_tile():
        empty = [(r,c) for r in range(size) for c in range(size) if board[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            board[r][c] = 2 if random.random() < 0.9 else 4

    def print_board():
        print("\n+" + "------+"*size)
        for row in board:
            print("|" + "".join(f"{(str(num) if num != 0 else ' '):^6}|" for num in row))
            print("+" + "------+"*size)

    def compress(row):
        new_row = [num for num in row if num != 0]
        new_row += [0]*(size - len(new_row))
        return new_row

    def merge(row):
        for i in range(size-1):
            if row[i] != 0 and row[i] == row[i+1]:
                row[i] *= 2
                row[i+1] = 0
        return row

    def move_left(board):
        new_board = []
        for row in board:
            compressed = compress(row)
            merged = merge(compressed)
            new_row = compress(merged)
            new_board.append(new_row)
        return new_board

    def reverse(board):
        return [row[::-1] for row in board]

    def transpose(board):
        return [list(row) for row in zip(*board)]

    def move_right(board):
        return reverse(move_left(reverse(board)))

    def move_up(board):
        return transpose(move_left(transpose(board)))

    def move_down(board):
        return transpose(move_right(transpose(board)))

    def boards_equal(b1, b2):
        for r in range(size):
            for c in range(size):
                if b1[r][c] != b2[r][c]:
                    return False
        return True

    def can_move(board):
        for r in range(size):
            for c in range(size):
                if board[r][c] == 0:
                    return True
                if c < size-1 and board[r][c] == board[r][c+1]:
                    return True
                if r < size-1 and board[r][c] == board[r+1][c]:
                    return True
        return False

    add_tile()
    add_tile()

    while True:
        print_board()
        move = input("Your move (W/A/S/D): ").strip().upper()
        if move not in ['W', 'A', 'S', 'D']:
            print("❗ Invalid input. Use W, A, S, or D.")
            continue

        if move == 'W':
            new_board = move_up(board)
        elif move == 'A':
            new_board = move_left(board)
        elif move == 'S':
            new_board = move_down(board)
        else:
            new_board = move_right(board)

        if boards_equal(board, new_board):
            print("⚠️ Move not possible, try a different direction.")
            continue

        board = new_board
        add_tile()
        clear_screen()

        if not can_move(board):
            print_board()
            print("💥 Game Over! No more moves left.")
            break

# --- Game 9: Minesweeper ---
def minesweeper():
    clear_screen()
    print("💣 Welcome to Minesweeper!")
    print("Enter coordinates like A1, B3 to reveal cells.\n")

    size = 5
    mines_count = 5

    # Initialize board with zeros
    board = [[0]*size for _ in range(size)]
    revealed = [[False]*size for _ in range(size)]
    flagged = [[False]*size for _ in range(size)]

    # Place mines randomly
    mines = set()
    while len(mines) < mines_count:
        r = random.randint(0, size-1)
        c = random.randint(0, size-1)
        mines.add((r,c))
        board[r][c] = -1  # -1 represents a mine

    # Calculate numbers for non-mine cells
    for r in range(size):
        for c in range(size):
            if board[r][c] == -1:
                continue
            count = 0
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < size and 0 <= nc < size:
                        if board[nr][nc] == -1:
                            count += 1
            board[r][c] = count

    def print_board(show_mines=False):
        print("\n   " + "  ".join(str(i+1) for i in range(size)))
        for r in range(size):
            row_display = []
            for c in range(size):
                if revealed[r][c]:
                    if board[r][c] == -1:
                        row_display.append("💣")
                    elif board[r][c] == 0:
                        row_display.append(" ")
                    else:
                        row_display.append(str(board[r][c]))
                else:
                    if show_mines and board[r][c] == -1:
                        row_display.append("💣")
                    else:
                        row_display.append("*")
            print(chr(65 + r) + "  " + "  ".join(row_display))

    def parse_input(pos):
        if len(pos) < 2:
            return None
        row = ord(pos[0].upper()) - 65
        try:
            col = int(pos[1:]) - 1
        except ValueError:
            return None
        if 0 <= row < size and 0 <= col < size:
            return row, col
        return None

    def reveal_cell(r, c):
        if revealed[r][c]:
            return
        revealed[r][c] = True
        if board[r][c] == 0:
            # Recursively reveal neighbors if no adjacent mines
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < size and 0 <= nc < size and not revealed[nr][nc]:
                        reveal_cell(nr, nc)

    cells_to_reveal = size*size - mines_count

    while True:
        print_board()
        move = input("Reveal cell (e.g., A1) or type 'quit' to exit: ").strip()
        if move.lower() == "quit":
            print("👋 Thanks for playing Minesweeper!")
            break

        pos = parse_input(move)
        if not pos:
            print("❗ Invalid input, try again.")
            continue

        r, c = pos

        if revealed[r][c]:
            print("⚠️ Cell already revealed. Pick another.")
            continue

        if board[r][c] == -1:
            # Mine triggered
            revealed[r][c] = True
            print_board(show_mines=True)
            print("💥 Boom! You hit a mine. Game over.")
            break

        # Reveal cells and update counter
        reveal_cell(r, c)
        cells_to_reveal = sum(
            1 for rr in range(size) for cc in range(size)
            if not revealed[rr][cc] and board[rr][cc] != -1
        )

        if cells_to_reveal == 0:
            print_board(show_mines=True)
            print("🎉 Congratulations! You cleared all safe cells!")
            break


# --- Game 10: Sudoku ---
def sudoku():
    clear_screen()
    print("🔢 Welcome to Sudoku!")
    print("Fill the grid with numbers 1-9 so that each row, column, and 3x3 box contains all digits.")
    print("Enter moves as row (A-I), column (1-9), and number (1-9), e.g., A15 means row A, column 1, number 5.\n")
    
    size = 9
    box_size = 3

    # A simple starting board (0 = empty)
    # You can replace this with a generated or predefined puzzle
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    def print_board():
        print("    " + "  ".join(str(i+1) for i in range(size)))
        for r in range(size):
            if r % box_size == 0 and r != 0:
                print("   " + "-" * 25)
            row = ""
            for c in range(size):
                if c % box_size == 0 and c != 0:
                    row += "| "
                val = board[r][c]
                row += str(val) if val != 0 else "."
                row += "  "
            print(chr(65 + r) + "  " + row)

    def is_valid_move(r, c, num):
        # Check row
        if any(board[r][x] == num for x in range(size)):
            return False
        # Check column
        if any(board[x][c] == num for x in range(size)):
            return False
        # Check box
        box_row_start = (r // box_size) * box_size
        box_col_start = (c // box_size) * box_size
        for i in range(box_row_start, box_row_start + box_size):
            for j in range(box_col_start, box_col_start + box_size):
                if board[i][j] == num:
                    return False
        return True

    def is_complete():
        for row in board:
            if 0 in row:
                return False
        return True

    while True:
        clear_screen()
        print_board()
        if is_complete():
            print("\n🎉 Congratulations! You solved the Sudoku!")
            break
        move = input("Enter move (e.g., A15 to put 5 in A1) or 'quit' to exit: ").strip()
        if move.lower() == "quit":
            print("👋 Thanks for playing Sudoku!")
            break
        if len(move) < 3:
            print("❗ Invalid input format. Try again.")
            time.sleep(1)
            continue
        row_char = move[0].upper()
        if row_char < 'A' or row_char > 'I':
            print("❗ Invalid row letter. Use A-I.")
            time.sleep(1)
            continue
        try:
            col = int(move[1]) - 1
            num = int(move[2])
        except ValueError:
            print("❗ Invalid column or number. Use digits 1-9.")
            time.sleep(1)
            continue
        row = ord(row_char) - 65
        if not (0 <= col < 9 and 1 <= num <= 9):
            print("❗ Column and number must be between 1 and 9.")
            time.sleep(1)
            continue
        if board[row][col] != 0:
            print("⚠️ Cell is already filled. Choose another cell.")
            time.sleep(1)
            continue
        if not is_valid_move(row, col, num):
            print("❌ Invalid move according to Sudoku rules.")
            time.sleep(1)
            continue
        board[row][col] = num

# --- Game 11: Battleship ---
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
            continue
        row = ord(move[0]) - 65
        col = int(move[1:]) - 1
        if not (0 <= row < size and 0 <= col < size):
            print("❗ Coordinates out of range.")
            time.sleep(1)
            clear_screen()
            continue
        if board[row][col] != "~":
            print("⚠️ You already guessed that spot!")
            time.sleep(1)
            clear_screen()
            continue

        attempts += 1
        if row == ship_row and col == ship_col:
            board[row][col] = "X"
            clear_screen()
            print_board(show_ship=True)
            print("\n🎉 Hit! You sank the enemy ship! You win!")
            break
        else:
            board[row][col] = "O"
            print("\n❌ Miss!")
            time.sleep(1)
            clear_screen()

    else:
        print_board(show_ship=True)
        print("\n💥 Game Over! You ran out of attempts.")
        print(f"The ship was at {chr(ship_row + 65)}{ship_col + 1}.")


# --- Game 12: Hangman ---
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
    

# --- Game 13: Connect Four ---
def connect_four():
    clear_screen()
    print("🔴🟡 Welcome to Connect Four!")
    
    ROWS, COLS = 6, 7
    board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
    
    def print_board():
        print("\n  " + " ".join(str(i+1) for i in range(COLS)))
        for row in board:
            print("|" + "|".join(row) + "|")
        print("-" * (COLS * 2 + 1))
    
    def is_valid_col(col):
        return 0 <= col < COLS and board[0][col] == " "
    
    def drop_piece(col, piece):
        for row in reversed(range(ROWS)):
            if board[row][col] == " ":
                board[row][col] = piece
                return row, col
    
    def check_win(piece):
        # Check horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(board[r][c+i] == piece for i in range(4)):
                    return True
        # Check vertical
        for r in range(ROWS - 3):
            for c in range(COLS):
                if all(board[r+i][c] == piece for i in range(4)):
                    return True
        # Check diagonal /
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(board[r - i][c + i] == piece for i in range(4)):
                    return True
        # Check diagonal \
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(board[r + i][c + i] == piece for i in range(4)):
                    return True
        return False
    
    turn = 0
    while True:
        print_board()
        player = "🔴" if turn % 2 == 0 else "🟡"
        try:
            col_choice = input(f"Player {player}, choose a column (1-{COLS}): ").strip()
            col = int(col_choice) - 1
            if not is_valid_col(col):
                print("❗ Column full or invalid. Try again.")
                continue
        except ValueError:
            print("❗ Enter a valid column number.")
            continue
        
        row, col = drop_piece(col, player)
        if check_win(player):
            print_board()
            print(f"🎉 Player {player} wins! Congratulations!")
            break
        
        if all(board[0][c] != " " for c in range(COLS)):
            print_board()
            print("🤝 It's a draw!")
            break
        
        turn += 1
        

# --- Game 14: Flappy Bird ---
def flappy_bird():
    import pygame
    import random
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

# --- Game 15: Whack-a-Mole ---
def whack_a_mole():
    pygame.init()

    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🕳️ Whack-a-Mole")

    clock = pygame.time.Clock()
    FONT = pygame.font.SysFont(None, 36)

    HOLE_RADIUS = 40
    MOLE_RADIUS = 30
    MOLE_TIME = 1000  # milliseconds mole stays visible

    holes = [
        (100, 150), (250, 150), (400, 150), (550, 150),
        (100, 300), (250, 300), (400, 300), (550, 300)
    ]

    mole_pos = random.choice(holes)
    mole_visible = True
    mole_timer = pygame.time.get_ticks()

    score = 0
    running = True

    while running:
        screen.fill((34, 139, 34))  # green background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and mole_visible:
                mouse_x, mouse_y = event.pos
                mx, my = mole_pos
                dist = ((mouse_x - mx) ** 2 + (mouse_y - my) ** 2) ** 0.5
                if dist <= MOLE_RADIUS:
                    score += 1
                    mole_visible = False
                    mole_timer = pygame.time.get_ticks()

        # Draw holes
        for hx, hy in holes:
            pygame.draw.circle(screen, (139, 69, 19), (hx, hy), HOLE_RADIUS)

        # Draw mole
        if mole_visible:
            pygame.draw.circle(screen, (0, 0, 0), mole_pos, MOLE_RADIUS)

        # Handle mole visibility timing
        current_time = pygame.time.get_ticks()
        if not mole_visible and current_time - mole_timer > 500:
            mole_pos = random.choice(holes)
            mole_visible = True
            mole_timer = current_time
        elif mole_visible and current_time - mole_timer > MOLE_TIME:
            mole_visible = False
            mole_timer = current_time

        # Display score
        score_surface = FONT.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


# --- Game 16: Simon Says ---
def simon_says():
    pygame.init()
    WIDTH, HEIGHT = 600, 650
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🧠 Simon Says")

    COLORS = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
    }
    BUTTONS = {
        "red": pygame.Rect(50, 50, 220, 220),
        "green": pygame.Rect(330, 50, 220, 220),
        "blue": pygame.Rect(50, 330, 220, 220),
        "yellow": pygame.Rect(330, 330, 220, 220),
    }

    FONT = pygame.font.SysFont(None, 40)
    BIG_FONT = pygame.font.SysFont(None, 60)
    clock = pygame.time.Clock()

    sequence = []
    user_sequence = []
    wait_time = 700  # milliseconds to show each color
    playing = False
    message = "Press SPACE to start"
    score = 0

    def draw_buttons(highlight=None):
        for color, rect in BUTTONS.items():
            base_color = COLORS[color]
            if highlight == color:
                bright = tuple(min(255, c + 120) for c in base_color)
                pygame.draw.rect(screen, bright, rect)
            else:
                pygame.draw.rect(screen, base_color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 5)

    def flash_sequence(seq):
        for color in seq:
            draw_buttons(color)
            pygame.display.flip()
            pygame.time.delay(wait_time)
            draw_buttons()
            pygame.display.flip()
            pygame.time.delay(300)

    def show_message(msg, sub=None):
        screen.fill((30, 30, 30))
        draw_buttons()
        text = BIG_FONT.render(msg, True, (255, 255, 255))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT - 100))
        if sub:
            sub_text = FONT.render(sub, True, (200, 200, 200))
            screen.blit(sub_text, (WIDTH//2 - sub_text.get_width()//2, HEIGHT - 50))
        pygame.display.flip()

    running = True
    while running:
        screen.fill((30, 30, 30))
        draw_buttons()
        
        # Show current message and score
        msg_surface = FONT.render(message, True, (255, 255, 255))
        score_surface = FONT.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(msg_surface, (WIDTH//2 - msg_surface.get_width()//2, HEIGHT - 80))
        screen.blit(score_surface, (WIDTH//2 - score_surface.get_width()//2, HEIGHT - 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not playing:
                    sequence = []
                    user_sequence = []
                    score = 0
                    playing = True
                    message = "Watch the sequence!"
                    pygame.time.delay(600)
                    sequence.append(random.choice(list(COLORS.keys())))
                    flash_sequence(sequence)
                    message = "Repeat the sequence!"
            elif event.type == pygame.MOUSEBUTTONDOWN and playing:
                pos = event.pos
                clicked_color = None
                for color, rect in BUTTONS.items():
                    if rect.collidepoint(pos):
                        clicked_color = color
                        break

                if clicked_color:
                    user_sequence.append(clicked_color)
                    draw_buttons(clicked_color)
                    pygame.display.flip()
                    pygame.time.delay(300)
                    draw_buttons()
                    pygame.display.flip()

                    if user_sequence[-1] != sequence[len(user_sequence)-1]:
                        message = "❌ Wrong! Press SPACE to try again."
                        playing = False
                        user_sequence = []
                    elif len(user_sequence) == len(sequence):
                        score += 1
                        message = "✅ Good! Watch the next sequence."
                        pygame.time.delay(800)
                        user_sequence = []
                        sequence.append(random.choice(list(COLORS.keys())))
                        flash_sequence(sequence)
                        message = "Repeat the sequence!"

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


# --- Game 17: Trivia Quiz ---
def trivia_quiz():
    clear_screen()
    print("❓ Welcome to Trivia Quiz!")
    questions = [
        {
            "question": "What is the capital of France?",
            "choices": ["A) Berlin", "B) London", "C) Paris", "D) Madrid"],
            "answer": "C"
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "choices": ["A) Earth", "B) Mars", "C) Jupiter", "D) Venus"],
            "answer": "B"
        },
        {
            "question": "Who wrote 'Romeo and Juliet'?",
            "choices": ["A) Charles Dickens", "B) William Shakespeare", "C) Mark Twain", "D) Jane Austen"],
            "answer": "B"
        },
        {
            "question": "What is the largest ocean on Earth?",
            "choices": ["A) Atlantic Ocean", "B) Indian Ocean", "C) Arctic Ocean", "D) Pacific Ocean"],
            "answer": "D"
        },
        {
            "question": "Which element has the chemical symbol 'O'?",
            "choices": ["A) Gold", "B) Oxygen", "C) Silver", "D) Iron"],
            "answer": "B"
        }
    ]

    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}: {q['question']}")
        for choice in q["choices"]:
            print(choice)
        while True:
            answer = input("Your answer (A, B, C, D): ").strip().upper()
            if answer in ["A", "B", "C", "D"]:
                break
            else:
                print("❗ Please enter a valid choice: A, B, C, or D.")
        if answer == q["answer"]:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Wrong! The correct answer was {q['answer']}.")
        time.sleep(1.5)

    print(f"\n🏆 You scored {score} out of {len(questions)}.")


# --- Game 18: Math Quiz ---
def math_quiz():
    clear_screen()
    print("➕ Welcome to Math Quiz!")

    questions = [
        {"question": "What is 7 + 5?", "answer": 12},
        {"question": "What is 9 - 4?", "answer": 5},
        {"question": "What is 6 * 3?", "answer": 18},
        {"question": "What is 20 / 4?", "answer": 5},
        {"question": "What is 15 % 4?", "answer": 3},
    ]

    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i}: {q['question']}")
        while True:
            try:
                user_answer = float(input("Your answer: ").strip())
                break
            except ValueError:
                print("❗ Please enter a valid number.")

        if abs(user_answer - q["answer"]) < 1e-5:  # allow minor floating-point error
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Wrong! The correct answer was {q['answer']}.")
        time.sleep(1.5)

    print(f"\n🏆 You scored {score} out of {len(questions)}.")
    

# --- Game 19: Bingo ---
def bingo():
    clear_screen()
    print("🏆 Welcome to Bingo!")

    import random

    # Create a Bingo card: 5x5 grid with columns B, I, N, G, O
    # Numbers range: B(1-15), I(16-30), N(31-45), G(46-60), O(61-75)
    card = []
    ranges = [(1, 15), (16, 30), (31, 45), (46, 60), (61, 75)]
    for r in ranges:
        column_numbers = random.sample(range(r[0], r[1] + 1), 5)
        card.append(column_numbers)

    # Transpose to get rows
    card = list(map(list, zip(*card)))

    # Center free space
    card[2][2] = "FREE"

    called_numbers = set()
    marks = [[False]*5 for _ in range(5)]
    marks[2][2] = True  # free space always marked

    def display_card():
        print("\n B   I   N   G   O")
        for r in range(5):
            row_display = []
            for c in range(5):
                val = card[r][c]
                if marks[r][c]:
                    row_display.append(f"[{str(val).rjust(2)}]")
                else:
                    row_display.append(f" {str(val).rjust(2)} ")
            print(" ".join(row_display))

    def check_bingo():
        # Check rows
        for row in marks:
            if all(row):
                return True
        # Check columns
        for col in range(5):
            if all(marks[row][col] for row in range(5)):
                return True
        # Check diagonals
        if all(marks[i][i] for i in range(5)):
            return True
        if all(marks[i][4 - i] for i in range(5)):
            return True
        return False

    print("Instructions: Numbers will be called. Mark them if they appear on your card.")
    input("Press Enter to start...")

    while True:
        clear_screen()
        display_card()
        print("\nCalled numbers:", sorted(called_numbers))
        input("\nPress Enter to call a new number...")
        # Call a new number
        while True:
            new_num = random.randint(1, 75)
            if new_num not in called_numbers:
                called_numbers.add(new_num)
                break
        print(f"Number called: {new_num}")

        # Mark number if found
        for r in range(5):
            for c in range(5):
                if card[r][c] == new_num:
                    marks[r][c] = True
                    print(f"Marked {new_num} on your card!")

        if check_bingo():
            print("\n🎉 BINGO! You won!")
            break

        time.sleep(2)


# --- Game 20: Jigsaw Puzzle ---
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


# --- Game 21: Word Search ---
#def word_search():


# --- Game 22: Crossword Puzzle ---
#def crossword_puzzle():



# --- Game 23: Tetris ---
def tetris():
    clear_screen()
    print("🔲 Welcome to Tetris!")

    WIDTH, HEIGHT = 10, 20
    board = [[0] * WIDTH for _ in range(HEIGHT)]

    pieces = {
        'I': [[[1,1,1,1]], [[1],[1],[1],[1]]],
        'O': [[[1,1],[1,1]]],
        'T': [[[0,1,0],[1,1,1]], [[1,0],[1,1],[1,0]], [[1,1,1],[0,1,0]], [[0,1],[1,1],[0,1]]],
        'S': [[[0,1,1],[1,1,0]], [[1,0],[1,1],[0,1]]],
        'Z': [[[1,1,0],[0,1,1]], [[0,1],[1,1],[1,0]]],
        'J': [[[1,0,0],[1,1,1]], [[1,1],[1,0],[1,0]], [[1,1,1],[0,0,1]], [[0,1],[0,1],[1,1]]],
        'L': [[[0,0,1],[1,1,1]], [[1,0],[1,0],[1,1]], [[1,1,1],[1,0,0]], [[1,1],[0,1],[0,1]]],
    }

    current_piece = None
    current_rotation = 0
    current_pos = [0, 0]
    game_over = False
    score = 0
    drop_speed = 0.5
    last_drop_time = time.time()

    def draw_board():
        clear_screen()
        print(f"Score: {score}\n")
        for r in range(HEIGHT):
            row = ""
            for c in range(WIDTH):
                cell = board[r][c]
                # Check if current piece occupies this cell
                if current_piece:
                    piece_shape = pieces[current_piece][current_rotation]
                    pr, pc = r - current_pos[0], c - current_pos[1]
                    if 0 <= pr < len(piece_shape) and 0 <= pc < len(piece_shape[0]) and piece_shape[pr][pc] == 1:
                        cell = 2  # current falling piece cell
                row += "■ " if cell else ". "
            print(row)

    def can_move(piece, rotation, pos):
        shape = pieces[piece][rotation]
        for r in range(len(shape)):
            for c in range(len(shape[0])):
                if shape[r][c] == 0:
                    continue
                br, bc = pos[0] + r, pos[1] + c
                if bc < 0 or bc >= WIDTH or br >= HEIGHT:
                    return False
                if br >= 0 and board[br][bc] != 0:
                    return False
        return True

    def place_piece(piece, rotation, pos):
        shape = pieces[piece][rotation]
        for r in range(len(shape)):
            for c in range(len(shape[0])):
                if shape[r][c] == 1:
                    br, bc = pos[0] + r, pos[1] + c
                    if 0 <= br < HEIGHT and 0 <= bc < WIDTH:
                        board[br][bc] = 1

    def clear_lines():
        nonlocal score
        new_board = [row for row in board if any(cell == 0 for cell in row)]
        lines_cleared = HEIGHT - len(new_board)
        for _ in range(lines_cleared):
            new_board.insert(0, [0]*WIDTH)
        if lines_cleared > 0:
            score += lines_cleared * 100
        return new_board

    def spawn_piece():
        nonlocal current_piece, current_rotation, current_pos
        current_piece = random.choice(list(pieces.keys()))
        current_rotation = 0
        # Spawn piece at top center
        shape_width = len(pieces[current_piece][0][0])
        current_pos = [0, WIDTH // 2 - shape_width // 2]

    def input_thread():
        nonlocal current_pos, current_rotation, game_over
        while not game_over:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'a':  # left
                    new_pos = [current_pos[0], current_pos[1] - 1]
                    if can_move(current_piece, current_rotation, new_pos):
                        current_pos = new_pos
                elif key == b'd':  # right
                    new_pos = [current_pos[0], current_pos[1] + 1]
                    if can_move(current_piece, current_rotation, new_pos):
                        current_pos = new_pos
                elif key == b's':  # down faster
                    new_pos = [current_pos[0] + 1, current_pos[1]]
                    if can_move(current_piece, current_rotation, new_pos):
                        current_pos = new_pos
                elif key == b'w':  # rotate
                    new_rotation = (current_rotation + 1) % len(pieces[current_piece])
                    if can_move(current_piece, new_rotation, current_pos):
                        current_rotation = new_rotation
                elif key == b'q':  # quit
                    game_over = True
            time.sleep(0.05)

    spawn_piece()

    threading.Thread(target=input_thread, daemon=True).start()

    while not game_over:
        now = time.time()
        if now - last_drop_time > drop_speed:
            new_pos = [current_pos[0] + 1, current_pos[1]]
            if can_move(current_piece, current_rotation, new_pos):
                current_pos = new_pos
            else:
                place_piece(current_piece, current_rotation, current_pos)
                board[:] = clear_lines()
                spawn_piece()
                if not can_move(current_piece, current_rotation, current_pos):
                    game_over = True
            last_drop_time = now

        draw_board()
        time.sleep(0.1)

    print("\nGame Over! Thanks for playing Tetris!")


# --- Game 24: Pac-Man ---
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
        

# --- Game 25: Space Invaders ---
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
        "Dice Roller": """
        🎲 Dice Roller Instructions:
        - Enter the number of sides on the dice.
        - Enter how many times you want to roll.
        - View the results of each roll.
        """,
        "Typing Test": """
        ⌨️ Typing Speed Test Instructions:
        - Type the given sentence as fast as you can.
        - Your time and words per minute (WPM) will be displayed.
        """,
        "Car Racing": """
        🚗 Car Racing Game Instructions:
        - Use the LEFT and RIGHT arrow keys to move the car.
        - Avoid obstacles to prevent crashing.
        - The game ends when you crash into an obstacle.
        """,
        "Snake": """
        🐍 Snake Game Instructions:
        - Use the arrow keys to move the snake.
        - Eat food to grow longer.
        - Avoid hitting walls or your own tail.
        """,
        "Tic-Tac-Toe": """
        ❌⭕ Tic-Tac-Toe Instructions:
        - Players take turns to place their mark (X or O) on a 3x3 grid.
        - The first to get three marks in a row wins.
        """,
        "Rock Paper Scissors": """
        ✊✋✌️ Rock Paper Scissors Instructions:
        - Choose rock, paper, or scissors.
        - Rock beats scissors, scissors beats paper, paper beats rock.
        """,
        "Memory Puzzle": """
        🧠 Memory Puzzle Instructions:
        - Flip two cards at a time to find matching pairs.
        - Remember the positions of cards to match them.
        """,
        "2048": """
        🧮 2048 Instructions:
        - Use arrow keys to move tiles.
        - Combine matching tiles to reach 2048.
        """,
        "Minesweeper": """
        💣 Minesweeper Instructions:
        - Click on cells to reveal them.
        - Avoid clicking on mines.
        - Use numbers to deduce the locations of mines.
        """,
        "Sudoku": """
        🔢 Sudoku Instructions:
        - Fill the 9x9 grid with numbers 1-9.
        - Each number must appear once in each row, column, and 3x3 subgrid.
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
        "Connect Four": """
        🔴🟡 Connect Four Instructions:
        - Drop your colored disc into a column.
        - The first to get four in a row wins.
        """,
        "Flappy Bird": """
        🐦 Flappy Bird Instructions:
        - Press space to make the bird flap.
        - Avoid pipes to stay alive.
        """,
        "Whack-a-Mole": """
        🕳️ Whack-a-Mole Instructions:
        - Hit the moles that pop up.
        - Avoid hitting other objects.
        """,
        "Simon Says": """
        🧠 Simon Says Instructions:
        - Follow the sequence of colors and sounds.
        - Repeat the sequence correctly to continue.
        """,
        "Trivia Quiz": """
        ❓ Trivia Quiz Instructions:
        - Answer multiple-choice questions.
        - Score points for correct answers.
        """,
        "Math Quiz": """
        ➕ Math Quiz Instructions:
        - Solve the given math problems.
        - Score points for correct answers.
        """,
        "Bingo": """
        🏆 Bingo Instructions:
        - Mark numbers on your card as they are called.
        - Complete a row, column, or diagonal to win.
        """,
        "Jigsaw Puzzle": """
        🧩 Jigsaw Puzzle Instructions:
        - Arrange pieces to form the complete image.
        - Complete the puzzle to win.
        """,
        "Word Search": """
        🔍 Word Search Instructions:
        - Find the listed words in the grid.
        - Words can be horizontal, vertical, or diagonal.
        """,
        "Crossword Puzzle": """
        🧠 Crossword Puzzle Instructions:
        - Fill in the grid with words based on clues.
        - Complete all words to finish the puzzle.
        """,
        "Tetris": """
        🔲 Tetris Instructions:
        - Rotate and place falling blocks.
        - Complete lines to clear them.
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
    "Dice Roller": roll_dice,
    "Typing Test": typing_speed_test,
    "Car Racing": car_racing_game,
    "Snake": snake_game,  # Replace with actual snake_game function when implemented
    "Tic-Tac-Toe": tic_tac_toe,
    "Rock Paper Scissors": rock_paper_scissors,
    "Memory Puzzle": memory_puzzle,
    "2048": game_2048,  # Replace with actual 2048 game function
    "Minesweeper": minesweeper,
    "Sudoku": sudoku,
    "Battleship": battleship,
    "Hangman": hangman,
    "Connect Four": connect_four,
    "Flappy Bird": flappy_bird,
    "Whack-a-Mole": whack_a_mole,
    "Simon Says": simon_says,
    "Trivia Quiz": trivia_quiz,
    "Math Quiz": math_quiz,
    "Bingo": bingo,
    "Jigsaw Puzzle": jigsaw_puzzle,
    "Word Search": lambda: placeholder_game("Word Search"),#word_search,
    "Crossword Puzzle": lambda: placeholder_game("Crossword Puzzle"),#crossword_puzzle,
    "Tetris": tetris,
    "Pac-Man": pacman,
    "Space Invaders": space_invaders
    #"Memory Match": lambda: placeholder_game("Memory Match")
    # Add more implemented games here
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

