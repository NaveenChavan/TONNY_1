import tkinter as tk

class ChessBoard:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Chess Board")
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
        piece_types = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        piece_colors = ["black", "black", "black", "black", "black", "black", "black", "black"]

        # Draw black pieces
        for i in range(8):
            self.canvas.create_oval(50 + i * 100, 50, 50 + i * 100 + piece_size, 50 + piece_size, fill=piece_colors[i])
            self.canvas.create_text(75 + i * 100, 75, text=piece_types[i][0].upper(), font=("Arial", 24))

        # Draw white pieces
        piece_types = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        piece_colors = ["white", "white", "white", "white", "white", "white", "white", "white"]
        for i in range(8):
            self.canvas.create_oval(50 + i * 100, 750, 50 + i * 100 + piece_size, 750 + piece_size, fill=piece_colors[i])
            self.canvas.create_text(75 + i * 100, 775, text=piece_types[i][0].upper(), font=("Arial", 24))

        # Draw pawns
        for i in range(8):
            self.canvas.create_oval(50 + i * 100, 150, 50 + i * 100 + piece_size, 150 + piece_size, fill="black")
            self.canvas.create_text(75 + i * 100, 175, text="P", font=("Arial", 24))
            self.canvas.create_oval(50 + i * 100, 650, 50 + i * 100 + piece_size, 650 + piece_size, fill="white")
            self.canvas.create_text(75 + i * 100, 675, text="P", font=("Arial", 24))

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    chess_board = ChessBoard()
    chess_board.run()