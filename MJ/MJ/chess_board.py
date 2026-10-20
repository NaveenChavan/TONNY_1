import tkinter as tk
from tkinter import messagebox

class ChessBoard:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Attractive Chessboard")
        self.window.geometry("800x800")
        self.canvas = tk.Canvas(self.window, width=800, height=800)
        self.canvas.pack()
        self.draw_board()

    def draw_board(self):
        square_size = 100
        for row in range(8):
            for col in range(8):
                color = "gray" if (row + col) % 2 == 0 else "white"
                self.canvas.create_rectangle(col * square_size, row * square_size, (col + 1) * square_size, (row + 1) * square_size, fill=color)

        # Draw pieces
        self.draw_pieces()

    def draw_pieces(self):
        piece_size = 80
        piece_types = ["R", "N", "B", "Q", "K", "B", "N", "R"]
        for i, piece_type in enumerate(piece_types):
            self.canvas.create_text(i * 100 + 50, 50, text=piece_type, font=("Arial", 40))
            self.canvas.create_text(i * 100 + 50, 750, text=piece_type.lower(), font=("Arial", 40))

        for i in range(8):
            self.canvas.create_text(i * 100 + 50, 150, text="P", font=("Arial", 40))
            self.canvas.create_text(i * 100 + 50, 650, text="p", font=("Arial", 40))

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    chess_board = ChessBoard()
    chess_board.run()