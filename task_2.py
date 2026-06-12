#Tic Tac Toe game with Minimax AI
import math

#  BOARD UTILITIES

def create_board():
    return [' '] * 9

def print_board(board):
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n  Position guide:")
    print("  1 | 2 | 3")
    print(" ---+---+---")
    print("  4 | 5 | 6")
    print(" ---+---+---")
    print("  7 | 8 | 9\n")

def check_winner(board):
    winning_lines = [
        [0,1,2], [3,4,5], [6,7,8],  # rows
        [0,3,6], [1,4,7], [2,5,8],  # columns
        [0,4,8], [2,4,6]             # diagonals
    ]
    for line in winning_lines:
        a, b, c = line
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]  # returns 'X' or 'O'
    return None

def is_board_full(board):
    return ' ' not in board

def get_available_moves(board):
    return [i for i, cell in enumerate(board) if cell == ' ']

#  MINIMAX WITH ALPHA-BETA PRUNING

def minimax(board, depth, alpha, beta, is_maximizing):
    """
    Minimax algorithm with Alpha-Beta Pruning.

    - AI  = 'O' → Maximizer (wants highest score)
    - Human = 'X' → Minimizer (wants lowest score)

    Scores:
      +10 - depth  →  AI wins  (faster win = higher score)
      -10 + depth  →  Human wins (faster loss = lower score)
       0           →  Draw
    """
    winner = check_winner(board)
    if winner == 'O':
        return 10 - depth
    if winner == 'X':
        return depth - 10
    if is_board_full(board):
        return 0

    if is_maximizing:  # AI's turn
        best_score = -math.inf
        for move in get_available_moves(board):
            board[move] = 'O'
            score = minimax(board, depth + 1, alpha, beta, False)
            board[move] = ' '
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break  # Alpha-Beta Prune ✂️
        return best_score

    else:  # Human's turn
        best_score = math.inf
        for move in get_available_moves(board):
            board[move] = 'X'
            score = minimax(board, depth + 1, alpha, beta, True)
            board[move] = ' '
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break  # Alpha-Beta Prune ✂️
        return best_score

def get_best_move(board):
    """Finds the best move for the AI using Minimax."""
    best_score = -math.inf
    best_move = -1
    for move in get_available_moves(board):
        board[move] = 'O'
        score = minimax(board, 0, -math.inf, math.inf, False)
        board[move] = ' '
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

#  GAME LOOP

def get_human_move(board):
    while True:
        try:
            move = int(input("Enter your move (1-9): ")) - 1
            if move < 0 or move > 8:
                print("Invalid! Enter a number between 1 and 9.")
            elif board[move] != ' ':
                print("That cell is already taken. Try again.")
            else:
                return move
        except ValueError:
            print("Invalid input. Please enter a number.")

def play_game():
    print("=" * 35)
    print("    TIC-TAC-TOE — AI vs Human")
    print("    Algorithm: Minimax + Alpha-Beta")
    print("=" * 35)
    print("You are X  |  AI is O")

    board = create_board()
    print_board(board)

    for turn in range(9):
        if turn % 2 == 0:
            # Human's turn
            print("Your turn (X):")
            move = get_human_move(board)
            board[move] = 'X'
        else:
            # AI's turn
            print("AI is thinking...")
            move = get_best_move(board)
            board[move] = 'O'
            print(f"AI placed O at position {move + 1}")

        print_board(board)

        winner = check_winner(board)
        if winner:
            if winner == 'X':
                print(" You win! (That shouldn't happen against a perfect AI!)")
            else:
                print(" AI wins!")
            return

        if is_board_full(board):
            print("It's a draw! Well played.")
            return

    print("Game over.")

def main():
    while True:
        play_game()
        again = input("Play again? (y/n): ").strip().lower()
        if again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()