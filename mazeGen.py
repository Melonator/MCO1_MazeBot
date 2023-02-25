# Maze generator -- Randomized Prim Algorithm

## Imports
import random
import time


## Functions
class mazeGenerator:
    mazeSize = int
    maze = []
    wall = '#'
    cell = '.'
    unvisited = 'u'

    # Find number of surrounding cells
    def surroundingCells(self, rand_wall):
        s_cells = 0
        if (self.maze[rand_wall[0] - 1][rand_wall[1]] == self.cell):
            s_cells += 1
        if (self.maze[rand_wall[0] + 1][rand_wall[1]] == self.cell):
            s_cells += 1
        if (self.maze[rand_wall[0]][rand_wall[1] - 1] == self.cell):
            s_cells += 1
        if (self.maze[rand_wall[0]][rand_wall[1] + 1] == self.cell):
            s_cells += 1

        return s_cells

    def generateMaze(self):
        height = self.mazeSize
        width = height

        # Denote all cells as unvisited
        for i in range(0, height):
            line = []
            for j in range(0, width):
                line.append(self.unvisited)
            self.maze.append(line)

        # Randomize starting point and set it a cell
        starting_height = int(random.random() * height)
        starting_width = int(random.random() * width)
        if (starting_height == 0):
            starting_height += 1
        if (starting_height == height - 1):
            starting_height -= 1
        if (starting_width == 0):
            starting_width += 1
        if (starting_width == width - 1):
            starting_width -= 1

        # Mark it as cell and add surrounding walls to the list
        self.maze[starting_height][starting_width] = self.cell
        walls = []
        walls.append([starting_height - 1, starting_width])
        walls.append([starting_height, starting_width - 1])
        walls.append([starting_height, starting_width + 1])
        walls.append([starting_height + 1, starting_width])

        # Denote walls in maze
        self.maze[starting_height - 1][starting_width] = self.wall
        self.maze[starting_height][starting_width - 1] = self.wall
        self.maze[starting_height][starting_width + 1] = self.wall
        self.maze[starting_height + 1][starting_width] = self.wall

        while (walls):
            # Pick a random wall
            rand_wall = walls[int(random.random() * len(walls)) - 1]

            # Check if it is a left wall
            if (rand_wall[1] != 0):
                if (self.maze[rand_wall[0]][rand_wall[1] - 1] == self.unvisited and self.maze[rand_wall[0]][
                    rand_wall[1] + 1] == self.cell):
                    # Find the number of surrounding cells
                    s_cells = self.surroundingCells(rand_wall)

                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.cell

                        # Mark the new walls
                        # Upper cell
                        if (rand_wall[0] != 0):
                            if (self.maze[rand_wall[0] - 1][rand_wall[1]] != self.cell):
                                self.maze[rand_wall[0] - 1][rand_wall[1]] = self.wall
                            if ([rand_wall[0] - 1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0] - 1, rand_wall[1]])

                        # Bottom cell
                        if (rand_wall[0] != height - 1):
                            if (self.maze[rand_wall[0] + 1][rand_wall[1]] != self.cell):
                                self.maze[rand_wall[0] + 1][rand_wall[1]] = self.wall
                            if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0] + 1, rand_wall[1]])

                        # Leftmost cell
                        if (rand_wall[1] != 0):
                            if (self.maze[rand_wall[0]][rand_wall[1] - 1] != self.cell):
                                self.maze[rand_wall[0]][rand_wall[1] - 1] = self.wall
                            if ([rand_wall[0], rand_wall[1] - 1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1] - 1])

                    # Delete wall
                    for w_wall in walls:
                        if (w_wall[0] == rand_wall[0] and w_wall[1] == rand_wall[1]):
                            walls.remove(w_wall)

                    continue

            # Check if it is an upper wall
            if (rand_wall[0] != 0):
                if (self.maze[rand_wall[0] - 1][rand_wall[1]] == self.unvisited and self.maze[rand_wall[0] + 1][
                    rand_wall[1]] == self.cell):

                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.cell

                        # Mark the new walls
                        # Upper cell
                        if (rand_wall[0] != 0):
                            if (self.maze[rand_wall[0] - 1][rand_wall[1]] != self.cell):
                                self.maze[rand_wall[0] - 1][rand_wall[1]] = self.wall
                            if ([rand_wall[0] - 1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0] - 1, rand_wall[1]])

                        # Leftmost cell
                        if (rand_wall[1] != 0):
                            if (self.maze[rand_wall[0]][rand_wall[1] - 1] != self.cell):
                                self.maze[rand_wall[0]][rand_wall[1] - 1] = self.wall
                            if ([rand_wall[0], rand_wall[1] - 1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1] - 1])

                        # Rightmost cell
                        if (rand_wall[1] != width - 1):
                            if (self.maze[rand_wall[0]][rand_wall[1] + 1] != self.cell):
                                self.maze[rand_wall[0]][rand_wall[1] + 1] = self.wall
                            if ([rand_wall[0], rand_wall[1] + 1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1] + 1])

                    # Delete wall
                    for w_wall in walls:
                        if (w_wall[0] == rand_wall[0] and w_wall[1] == rand_wall[1]):
                            walls.remove(w_wall)

                    continue

            # Check the bottom wall
            if (rand_wall[0] != height - 1):
                if (self.maze[rand_wall[0] + 1][rand_wall[1]] == self.unvisited and self.maze[rand_wall[0] - 1][
                    rand_wall[1]] == self.cell):

                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.cell

                        # Mark the new walls
                        if (rand_wall[0] != height - 1):
                            if (self.maze[rand_wall[0] + 1][rand_wall[1]] != self.cell):
                                self.maze[rand_wall[0] + 1][rand_wall[1]] = self.wall
                            if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0] + 1, rand_wall[1]])
                        if (rand_wall[1] != 0):
                            if (self.maze[rand_wall[0]][rand_wall[1] - 1] != self.cell):
                                self.maze[rand_wall[0]][rand_wall[1] - 1] = self.wall
                            if ([rand_wall[0], rand_wall[1] - 1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1] - 1])
                        if (rand_wall[1] != width - 1):
                            if (self.maze[rand_wall[0]][rand_wall[1] + 1] != self.cell):
                                self.maze[rand_wall[0]][rand_wall[1] + 1] = self.wall
                            if ([rand_wall[0], rand_wall[1] + 1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1] + 1])

                    # Delete wall
                    for w_wall in walls:
                        if (w_wall[0] == rand_wall[0] and w_wall[1] == rand_wall[1]):
                            walls.remove(w_wall)

                    continue

            # Check the right wall
            if (rand_wall[1] != width - 1):
                if (self.maze[rand_wall[0]][rand_wall[1] + 1] == 'u' and self.maze[rand_wall[0]][
                    rand_wall[1] - 1] == self.cell):

                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = self.cell

                        # Mark the new walls
                        if (rand_wall[1] != width - 1):
                            if (self.maze[rand_wall[0]][rand_wall[1] + 1] != self.cell):
                                self.maze[rand_wall[0]][rand_wall[1] + 1] = self.wall
                            if ([rand_wall[0], rand_wall[1] + 1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1] + 1])
                        if (rand_wall[0] != height - 1):
                            if (self.maze[rand_wall[0] + 1][rand_wall[1]] != self.cell):
                                self.maze[rand_wall[0] + 1][rand_wall[1]] = self.wall
                            if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0] + 1, rand_wall[1]])
                        if (rand_wall[0] != 0):
                            if (self.maze[rand_wall[0] - 1][rand_wall[1]] != self.cell):
                                self.maze[rand_wall[0] - 1][rand_wall[1]] = self.wall
                            if ([rand_wall[0] - 1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0] - 1, rand_wall[1]])

                    # Delete wall
                    for w_wall in walls:
                        if (w_wall[0] == rand_wall[0] and w_wall[1] == rand_wall[1]):
                            walls.remove(w_wall)

                    continue

            # Delete the wall from the list anyway
            for w_wall in walls:
                if (w_wall[0] == rand_wall[0] and w_wall[1] == rand_wall[1]):
                    walls.remove(w_wall)

        # Mark the remaining unvisited cells as walls
        for i in range(0, height):
            for j in range(0, width):
                if (self.maze[i][j] == 'u'):
                    self.maze[i][j] = self.wall

        # Set entrance and exit
        for i in range(0, width):
            if (self.maze[1][i] == self.cell):
                self.maze[0][i] = self.cell
                break

        for i in range(width - 1, 0, -1):
            if (self.maze[height - 2][i] == self.cell):
                self.maze[height - 1][i] = self.cell
                break

        return self.maze
## Main code
# Init variables
