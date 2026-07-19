#!/usr/bin/env python3
"""
Simple Tic Tac Toe game for two players.
Players take turns entering numbers 1-9 to place their mark.
"""


def print_board(board):
    """Print the current game board."""
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("-----------")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("-----------")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")


def check_winner(board):
    """Check if there's a winner or a tie."""
    # Check rows
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] != " ":
            return board[i]

    # Check columns
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] != " ":
            return board[i]

    # Check diagonals
    if board[0] == board[4] == board[8] != " ":
        return board[0]
    if board[2] == board[4] == board[6] != " ":
        return board[2]

    # Check for tie
    if " " not in board:
        return "Tie"

    return None


def get_player_move(player, board):
    """Get valid move from player."""
    while True:
        try:
            move = int(input(f"Player {player}, enter your move (1-9): ")) - 1
            if 0 <= move <= 8 and board[move] == " ":
                return move
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Please enter a number between 1 and 9.")


def play_game():
    """Main game loop."""
    board = [" " for _ in range(9)]
    current_player = "X"

    print("Welcome to Tic Tac Toe!")
    print("Enter numbers 1-9 to make your move:")
    print(" 1 | 2 | 3 ")
    print("-----------")
    print(" 4 | 5 | 6 ")
    print("-----------")
    print(" 7 | 8 | 9 ")
    print("\nLet's begin!\n")

    while True:
        print_board(board)
        move = get_player_move(current_player, board)
        board[move] = current_player

        winner = check_winner(board)
        if winner:
            print_board(board)
            if winner == "Tie":
                print("It's a tie!")
            else:
                print(f"Player {winner} wins!")
            break

        # Switch players
        current_player = "O" if current_player == "X" else "X"


def main():
    """Run the game."""
    while True:
        play_game()
        play_again = input("\nPlay again? (y/n): ").lower()
        if play_again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
