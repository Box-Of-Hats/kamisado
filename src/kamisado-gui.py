from kamisado import Kamisado, Piece, Colors, Players
import tkinter as tk

color_mappings = {
    Colors.ORANGE: "orange",
    Colors.BLUE: "blue",
    Colors.PURPLE: "purple",
    Colors.PINK: "pink",
    Colors.YELLOW: "yellow",
    Colors.RED: "red",
    Colors.GREEN: "green",
    Colors.BROWN: "brown"
}

player_mappings = {
    Players.BLACK: "black",
    Players.WHITE: "white"
}


class KamisadoGui():
    def __init__(self, master, game):
        self.selected_cell = None
        self.master = master
        self.game = game

        master.config(padx=6, pady=6)

        board_region = tk.Frame(self.master)
        board_region.pack(side=tk.LEFT)

        sidebar_region = tk.Frame(self.master)
        sidebar_region.pack(side=tk.RIGHT, padx=6, pady=6)

        self.sidebar_region = sidebar_region
        self.board_region = board_region

        self.draw_sidebar(sidebar_region)
        self.draw_board(board_region)

    def cell_clicked(self, loc):
        if (self.selected_cell == None):
            if self.game.get_moving_piece(loc) != None:
                self.selected_cell = loc
        else:
            self.game.move_piece(self.selected_cell, loc)
            self.selected_cell = None

        self.draw_board(self.board_region)
        # self.draw_sidebar(self.sidebar_region)

    def draw_sidebar(self, master):
        for child in master.winfo_children():
            child.destroy()

        self.current_turn_label = tk.Label(
            master, text="Turn: {}".format(self.game.current_turn_player))
        self.current_turn_label.pack(fill="x", side=tk.TOP)

        self.current_color_label = tk.Label(master)
        self.current_color_label.pack(fill="x", side=tk.TOP)

    def draw_board(self, master):
        for child in master.winfo_children():
            child.destroy()
        for y, row in enumerate(self.game.gameboard):
            for x, cell in enumerate(row):
                if isinstance(cell, Piece):
                    cell_value = "■"
                    cell_background = color_mappings[cell.color]

                    cell_foreground = player_mappings[cell.owner_id]
                    cell_relief = tk.SOLID

                    # Auto select the next piece
                    if self.game.current_turn_player == cell.owner_id and self.game.current_turn_color == cell.color:
                        self.selected_cell = (x, y)
                else:
                    cell_value = ""
                    cell_background = color_mappings[self.game.cell_colors[y][x]]
                    cell_foreground = color_mappings[self.game.cell_colors[y][x]]
                    cell_relief = tk.FLAT

                if self.selected_cell != None:
                    if (x, y) == self.selected_cell:
                        cell_relief = tk.RIDGE

                button = tk.Button(master, width=3, command=lambda x=x,
                                   y=y: self.cell_clicked((x, y)), text=cell_value)

                button.config(background=cell_background,
                              foreground=cell_foreground,
                              relief=cell_relief,
                              borderwidth=4)
                button.grid(row=y, column=x)

        # Update labels
        self.current_turn_label.configure(
            text="Turn: {}".format(self.game.current_turn_player))

        if (self.game.current_turn_color != Colors.ANY):
            self.current_color_label.configure(
                background=color_mappings[self.game.current_turn_color])

        winner = self.game.get_winner()
        if winner != None:
            tk.Label(self.sidebar_region,
                     text="Winner! - {}".format(winner)).pack(fill="x")
    #         tk.Button(self.sidebar_region, text="Reset",
    #                   command=lambda: self.reset()).pack(fill="x")

    # def reset(self):
    #     self.game = Kamisado()
    #     self.draw_board(self.board_region)


if __name__ == "__main__":
    root = tk.Tk()
    game = Kamisado()
    gui = KamisadoGui(root, game)
    root.mainloop()
