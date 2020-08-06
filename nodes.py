import pygame

# Color constants:
GRID_COLOR = (175, 216, 248)
START_COLOR = (191, 0, 255)
END_COLOR = (255, 191, 0)
WALL_COLOR = (27, 42, 53)
PATH_COLOR = (255, 0, 0)
CLEAR_COLOR = (255, 255, 255)
OPEN_COLOR = (0, 255, 0)
CLOSED_COLOR = (64, 206, 227)


class PathNode:
    def __init__(self, row, col, width, total_row_nr):
        self.row = row
        self.col = col
        self.width = width
        self.x = row * width
        self.y = col * width
        self.total_row_nr = total_row_nr
        self.color = CLEAR_COLOR
        self.neighbors = []

    def is_open(self):
        return self.color == OPEN_COLOR

    def is_closed(self):
        return self.color == CLOSED_COLOR

    def is_wall(self):
        return self.color == WALL_COLOR

    def is_start(self):
        return self.color == START_COLOR

    def is_end(self):
        return self.color == END_COLOR

    def get_pos(self):
        return self.row, self.col

    def reset_node(self):
        self.color = CLEAR_COLOR

    def make_open(self):
        self.color = OPEN_COLOR

    def make_close(self):
        self.color = CLOSED_COLOR

    def make_start(self):
        self.color = START_COLOR

    def make_end(self):
        self.color = END_COLOR

    def make_wall(self):
        self.color = WALL_COLOR

    def make_path(self):
        self.color = PATH_COLOR

    def __lt__(self, other):
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, node_list):
        self.neighbors = []
        if self.row > 0 and not node_list[self.row - 1][self.col].is_wall():                         #Top Neighbor
            self.neighbors.append(node_list[self.row - 1][self.col])
        if self.row < self.total_row_nr - 1 and not node_list[self.row + 1][self.col].is_wall():     #Down Neighbor
            self.neighbors.append(node_list[self.row + 1][self.col])
        if self.col > 0 and not node_list[self.row][self.col - 1].is_wall():                         #Left Neighbor
            self.neighbors.append(node_list[self.row][self.col - 1])
        if self.col < self.total_row_nr - 1 and not node_list[self.row][self.col + 1].is_wall():     #Right Neighbor
            self.neighbors.append(node_list[self.row][self.col + 1])




