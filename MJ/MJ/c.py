import tkinter as tk
from tkinter import messagebox

class ChessGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Chess Game")
        self.window.geometry("800x800")
        self.player_turn = "white"
        self.selected_piece = None
        self.pieces = self.initialize_pieces()
        self.buttons = self.create_buttons()
        self.update_buttons()

    def initialize_pieces(self):
        pieces = []
        for i in range(8):
            row = []
            for j in range(8):
                if i == 1:
                    row.append("black_pawn")
                elif i == 6:
                    row.append("white_pawn")
                elif i == 0:
                    if j in [0, 7]:
                        row.append("black_rook")
                    elif j in [1, 6]:
                        row.append("black_knight")
                    elif j in [2, 5]:
                        row.append("black_bishop")
                    elif j == 3:
                        row.append("black_queen")
                    elif j == 4:
                        row.append("black_king")
                elif i == 7:
                    if j in [0, 7]:
                        row.append("white_rook")
                    elif j in [1, 6]:
                        row.append("white_knight")
                    elif j in [2, 5]:
                        row.append("white_bishop")
                    elif j == 3:
                        row.append("white_queen")
                    elif j == 4:
                        row.append("white_king")
                else:
                    row.append("empty")
            pieces.append(row)
        return pieces

    def create_buttons(self):
        buttons = []
        for i in range(8):
            row = []
            for j in range(8):
                button = tk.Button(self.window, command=lambda i=i, j=j: self.click(i, j), height=3, width=6)
                button.grid(row=i, column=j)
                row.append(button)
            buttons.append(row)     
        return buttons

    def update_buttons(self):
        for i in range(8):
            for j in range(8):
                piece = self.pieces[i][j]
                if piece == "empty":
                    self.buttons[i][j].config(text="", bg="gray")
                elif piece == "black_pawn":
                    self.buttons[i][j].config(text="P", bg="black", fg="white")
                elif piece == "white_pawn":
                    self.buttons[i][j].config(text="P", bg="white", fg="black")
                elif piece == "black_rook":
                    self.buttons[i][j].config(text="R", bg="black", fg="white")
                elif piece == "white_rook":
                    self.buttons[i][j].config(text="R", bg="white", fg="black")
                elif piece == "black_knight":
                    self.buttons[i][j].config(text="N", bg="black", fg="white")
                elif piece == "white_knight":
                    self.buttons[i][j].config(text="N", bg="white", fg="black")
                elif piece == "black_bishop":
                    self.buttons[i][j].config(text="B", bg="black", fg="white")
                elif piece == "white_bishop":
                    self.buttons[i][j].config(text="B", bg="white", fg="black")
                elif piece == "black_queen":
                    self.buttons[i][j].config(text="Q", bg="black", fg="white")
                elif piece == "white_queen":
                    self.buttons[i][j].config(text="Q", bg="white", fg="black")
                elif piece == "black_king":
                    self.buttons[i][j].config(text="K", bg="black", fg="white")
                elif piece == "white_king":
                    self.buttons[i][j].config(text="K", bg="white", fg="black")

    def click(self, i, j):
        if self.selected_piece is None:
            if self.pieces[i][j] != "empty" and self.pieces[i][j].split("_")[0] == self.player_turn:
                self.selected_piece = (i, j)
                self.buttons[i][j].config(bg="blue")
            else:
                messagebox.showerror("Invalid move", "You must select one of your pieces")
        else:
            if self.pieces[i][j] == "empty" or self.pieces[i][j].split("_")[0] != self.player_turn:
                if self.is_valid_move(self.selected_piece, (i, j)):
                    self.pieces[i][j] = self.pieces[self.selected_piece[0]][self.selected_piece[1]]
                    self.pieces[self.selected_piece[0]][self.selected_piece[1]] = "empty"
                    self.update_buttons()
                    self.selected_piece = None
                    self.player_turn = "black" if self.player_turn == "white" else "white"
                else:
                    messagebox.showerror("Invalid move", "You cannot move that piece there")
            else:
                messagebox.showerror("Invalid move", "You cannot capture your own piece")
            self.buttons[self.selected_piece[0]][self.selected_piece[1]].config(bg="gray")
            self.selected_piece = None

    def is_valid_move(self, start, end):
        piece = self.pieces[start[0]][start[1]]
        if piece == "black_pawn" or piece == "white_pawn":
            return self.is_valid_pawn_move(start, end)
        elif piece == "black_rook" or piece == "white_rook":
            return self.is_valid_rook_move(start, end)
        elif piece == "black_knight" or piece == "white_knight":
            return self.is_valid_knight_move(start, end)
        elif piece == "black_bishop" or piece == "white_bishop":
            return self.is_valid_bishop_move(start, end)
        elif piece == "black_queen" or piece == "white_queen":
            return self.is_valid_queen_move(start, end)
        elif piece == "black_king" or piece == "white_king":
            return self.is_valid_king_move(start, end)

    def is_valid_pawn_move(self, start, end):
        if self.pieces[start[0]][start[1]].split("_")[0] == "white":
            if start[1] == end[1] and end[0] == start[0] + 1 and self.pieces[end[0]][end[1]] == "empty":
                return True
            elif start[1] == end[1] and end[0] == start[0] + 2 and self.pieces[end[0]][end[1]] == "empty" and self.pieces[end[0] - 1][end[1]] == "empty" and start[0] == 6:
                return True
            elif abs(start[1] - end[1]) == 1 and end[0] == start[0] + 1 and self.pieces[end[0]][end[1]].split("_")[0] == "black":
                return True
        else:
            if start[1] == end[1] and end[0] == start[0] - 1 and self.pieces[end[0]][end[1]] == "empty":
                return True
            elif start[1] == end[1] and end[0] == start[0] - 2 and self.pieces[end[0]][end[1]] == "empty" and self.pieces[end[0] + 1][end[1]] == "empty" and start[0] == 1:
                return True
            elif abs(start[1] - end[1]) == 1 and end[0] == start[0] - 1 and self.pieces[end[0]][end[1]].split("_")[0] == "white":
                return True
        return False

    def is_valid_rook_move(self, start, end):
        if start[0] == end[0]:
            for i in range(min(start[1], end[1]) + 1, max(start[1], end[1])):
                if self.pieces[start[0]][i] != "empty":
                    return False
            return True
        elif start[1] == end[1]:
            for i in range(min(start[0], end[0]) + 1, max(start[0], end[0])):
                if self.pieces[i][start[1]] != "empty":
                    return False
            return True
        return False

    def is_valid_knight_move(self, start, end):
        if abs(start[0] - end[0]) == 2 and abs(start[1] - end[1]) == 1:
            return True
        elif abs(start[0] - end[0]) == 1 and abs(start[1] - end[1]) == 2:
            return True
        return False

    def is_valid_bishop_move(self, start, end):
        if abs(start[0] - end[0]) == abs(start[1] - end[1]):
            x = 1 if end[0] > start[0] else -1
            y = 1 if end[1] > start[1] else -1
            for i in range(1, abs(start[0] - end[0])):
                if self.pieces[start[0] + i * x][start[1] + i * y] != "empty":
                    return False
            return True
        return False

    def is_valid_queen_move(self, start, end):
        return self.is_valid_rook_move(start, end) or self.is_valid_bishop_move(start, end)

    def is_valid_king_move(self, start, end):
        if abs(start[0] - end[0]) <= 1 and abs(start[1] - end[1]) <= 1:
            return True
        return False

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = ChessGame()
    game.run()