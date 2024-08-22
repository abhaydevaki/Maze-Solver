import tkinter as tk
from tkinter import messagebox
import queue
import time

maze = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", "O", " ", "#", " ", " ", " ", "#", " ", "#", " ", " ", "#"],
    ["#", " ", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", "#"],
    ["#", " ", "#", "#", " ", "#", " ", "#", " ", "#", " ", " ", "#"],
    ["#", " ", "#", " ", " ", " ", " ", " ", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", "#", "#", "#", "#", "#", "#", " ", " ", "#"],
    ["#", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", "#", "#"],
    ["#", "#", "#", " ", "#", " ", "#", "#", "#", "#", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", "#", " ", " ", "#", " ", "#", "#"],
    ["#", "#", "#", "#", "#", " ", "#", " ", "#", "#", " ", " ", "#"],
    ["#", " ", " ", " ", "#", " ", " ", " ", "#", " ", " ", "#", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#", " ", " ", " ", "#"],
    ["#", " ", "#", "#", "#", "#", "#", " ", "#", "#", "#", "X", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
]

class MazeSolver:
    def __init__(self, maze, app):
        self.maze = maze
        self.app = app
        self.start_pos = self.find_start('O')
        self.end_pos = self.find_start('X')

    def find_start(self, symbol):
        for i, row in enumerate(self.maze):
            for j, value in enumerate(row):
                if value == symbol:
                    return i, j
        return None

    def find_path(self):
        start = self.start_pos
        end = self.end_pos
        q = queue.Queue()
        q.put((start, [start]))

        visited = set()

        while not q.empty():
            current_pos, path = q.get()
            row, col = current_pos

            self.app.update_maze(path)

            if self.maze[row][col] == 'X':
                return path

            neighbors = self.find_neighbors(row, col)
            for neighbor in neighbors:
                if neighbor in visited:
                    continue

                r, c = neighbor
                if self.maze[r][c] == "#":
                    continue

                new_path = path + [neighbor]
                q.put((neighbor, new_path))
                visited.add(neighbor)

            time.sleep(0.2)  # Slow down the visualization for better viewing

        return []

    def find_neighbors(self, row, col):
        neighbors = []

        if row > 0:  # UP
            neighbors.append((row - 1, col))
        if row + 1 < len(self.maze):  # DOWN
            neighbors.append((row + 1, col))
        if col > 0:  # LEFT
            neighbors.append((row, col - 1))
        if col + 1 < len(self.maze[0]):  # RIGHT
            neighbors.append((row, col + 1))

        return neighbors

class MazeApp:
    def __init__(self, root, maze):
        self.root = root
        self.maze = maze
        self.solver = MazeSolver(maze, self)
        self.path = []
        self.cell_size = 30
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=len(self.maze[0]) * self.cell_size, height=len(self.maze) * self.cell_size)
        self.canvas.pack()

        self.solve_button = tk.Button(self.root, text="Solve Maze", command=self.solve_maze)
        self.solve_button.pack()

        self.draw_maze()

    def draw_maze(self):
        self.canvas.delete("all")
        for i, row in enumerate(self.maze):
            for j, value in enumerate(row):
                color = "white"
                if value == "#":
                    color = "black"
                elif value == "O":
                    color = "red"
                elif value == "X":
                    color = "green"
                self.canvas.create_rectangle(j * self.cell_size, i * self.cell_size, (j + 1) * self.cell_size, (i + 1) * self.cell_size, fill=color)

    def solve_maze(self):
        self.path = self.solver.find_path()
        if self.path:
            self.show_solution()
        else:
            messagebox.showinfo("No Solution", "No path found in the maze!")

    def update_maze(self, path):
        self.draw_maze()
        for pos in path:
            row, col = pos
            self.canvas.create_rectangle(col * self.cell_size, row * self.cell_size, (col + 1) * self.cell_size, (row + 1) * self.cell_size, fill="blue")
        self.root.update()

    def show_solution(self):
        for pos in self.path:
            row, col = pos
            self.canvas.create_rectangle(col * self.cell_size, row * self.cell_size, (col + 1) * self.cell_size, (row + 1) * self.cell_size, fill="green")
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root, maze)
    root.mainloop()





















# import curses
# from curses import wrapper
# import queue
# import time

# maze = [
#     ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
#     ["#", "O", " ", "#", " ", " ", " ", "#", " ", "#", " ", " ", "#"],
#     ["#", " ", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", "#"],
#     ["#", " ", "#", "#", " ", "#", " ", "#", " ", "#", " ", " ", "#"],
#     ["#", " ", "#", " ", " ", " ", " ", " ", " ", "#", "#", " ", "#"],
#     ["#", " ", "#", " ", "#", "#", "#", "#", "#", "#", " ", " ", "#"],
#     ["#", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", "#", "#"],
#     ["#", "#", "#", " ", "#", " ", "#", "#", "#", "#", " ", " ", "#"],
#     ["#", " ", " ", " ", " ", " ", "#", " ", " ", "#", " ", "#", "#"],
#     ["#", "#", "#", "#", "#", " ", "#", " ", "#", "#", " ", " ", "#"],
#     ["#", " ", " ", " ", "#", " ", " ", " ", "#", " ", " ", "#", "#"],
#     ["#", " ", "#", " ", " ", " ", "#", " ", "#", " ", " ", " ", "#"],
#     ["#", " ", "#", "#", "#", "#", "#", " ", "#", "#", "#", "X", "#"],
#     ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
# ]

# def print_maze(maze, stdscr, path=[]):
#     BLUE = curses.color_pair(1)
#     RED = curses.color_pair(2)

#     height, width = stdscr.getmaxyx()

#     for i, row in enumerate(maze):
#         for j, value in enumerate(row):
#             if i >= height or j*2 >= width - 1:
#                 continue  # Skip if out of bounds
#             if (i, j) in path:
#                 stdscr.addstr(i, j*2, "X", RED)
#             else:
#                 stdscr.addstr(i, j*2, value, BLUE)

# def find_start(maze, start):
#     for i, row in enumerate(maze):
#         for j, value in enumerate(row):
#             if value == start:
#                 return i, j
#     return None

# def find_path(maze, stdscr):
#     start = "O"
#     end = "X"
#     start_pos = find_start(maze, start)

#     q = queue.Queue()
#     q.put((start_pos, [start_pos]))

#     visited = set()

#     while not q.empty():
#         current_pos, path = q.get()
#         row, col = current_pos

#         stdscr.clear()
#         print_maze(maze, stdscr, path)
#         stdscr.refresh()
#         time.sleep(0.5)

#         if maze[row][col] == end:
#             return path

#         neighbors = find_neighbors(maze, row, col)
#         for neighbor in neighbors:
#             if neighbor in visited:
#                 continue

#             r, c = neighbor
#             if maze[r][c] == "#":
#                 continue

#             new_path = path + [neighbor]
#             q.put((neighbor, new_path))
#             visited.add(neighbor)

# def find_neighbors(maze, row, col):
#     neighbors = []

#     if row > 0:  # UP
#         neighbors.append((row - 1, col))
#     if row + 1 < len(maze):  # DOWN
#         neighbors.append((row + 1, col))
#     if col > 0:  # LEFT
#         neighbors.append((row, col - 1))
#     if col + 1 < len(maze[0]):  # RIGHT
#         neighbors.append((row, col + 1))

#     return neighbors

# def main(stdscr):
#     curses.curs_set(0)  # Hide cursor
#     stdscr.clear()
#     stdscr.refresh()

#     curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
#     curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

#     find_path(maze, stdscr)
#     stdscr.getch()

# wrapper(main)


# # maze = [
# #     ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
# #     ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
# #     ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
# #     ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
# #     ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
# #     ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
# #     ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
# #     ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
# #     ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
# # ]
