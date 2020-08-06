import pygame
import nodes
from queue import PriorityQueue


def heuristic_fn(p1, p2):
    x1, x2 = p1
    y1, y2 = p2
    return abs(y2 - y1) + abs(x2 - x1)


def nodes_list(total_rows, width):
    list_node = []
    node_size = width // total_rows

    for i in range(total_rows):
        list_node.append([])
        for j in range(total_rows):
            node = nodes.PathNode(row=i, col=j, width=node_size, total_row_nr=total_rows)
            list_node[i].append(node)

    return list_node


def draw_grid(surface, total_rows, screen_width):
    node_size = screen_width // total_rows
    for i in range(total_rows):
        pygame.draw.line(surface, nodes.GRID_COLOR, (0, i * node_size), (screen_width, i * node_size))

        for j in range(total_rows):
            pygame.draw.line(surface, nodes.GRID_COLOR, (j * node_size, 0), (j * node_size, screen_width))


def draw(surface, grid, total_rows, screen_width):
    surface.fill(nodes.CLEAR_COLOR)

    for row in grid:
        for node in row:
            node.draw(surface)

    draw_grid(surface, total_rows, screen_width)
    pygame.display.update()


def get_clicked_position(mouse_position, total_rows, screen_width):
    x, y = mouse_position
    node_size = screen_width // total_rows
    row = x // node_size
    col = y // node_size

    return row, col


def algorithm(draw, node_list, start, end):
    insert_index = 0
    pq = PriorityQueue()
    pq.put((0, insert_index, start))
    node_came_from = {}
    g_score = {node: float("inf") for row in node_list for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in node_list for node in row}
    f_score[start] = heuristic_fn(start.get_pos(), end.get_pos())
    # set to keep track of nodes in PQ
    open_set = {start}
    while not pq.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr_node = pq.get()[2]  # pop
        open_set.remove(curr_node)  # remove from set

        if curr_node == end:
            create_path(node_came_from, end, draw)
            start.make_start()
            end.make_end()
            return True

        for neighbor in curr_node.neighbors:
            g_score_temp = g_score[curr_node] + 1

            if g_score_temp < g_score[neighbor]:
                node_came_from[neighbor] = curr_node
                g_score[neighbor] = g_score_temp
                f_score[neighbor] = g_score_temp + heuristic_fn(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set:
                    insert_index = insert_index + 1
                    pq.put((f_score[neighbor], insert_index, neighbor))
                    open_set.add(neighbor)
                    neighbor.make_open()

        draw()

        if curr_node != start:
            curr_node.make_close()

    return False


def create_path(node_came_from, curr_node, draw):
    # create path from end to start, recursively
    while curr_node in node_came_from:
        curr_node = node_came_from[curr_node]
        curr_node.make_path()
        draw()


def path_finder(surface, screen_width, nr_grid_rows):
    node_list = nodes_list(nr_grid_rows, screen_width)

    start = None  # starting node
    end = None  # ending node

    is_running = True  # boolean check for loop run

    while is_running:
        draw(surface, node_list, nr_grid_rows, screen_width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if pygame.mouse.get_pressed()[0]:  # Left Click
                clicked_position = pygame.mouse.get_pos()
                row, col = get_clicked_position(clicked_position, total_rows=nr_grid_rows, screen_width=screen_width)
                clicked_node = node_list[row][col]

                if not start and clicked_node != end:
                    start = clicked_node
                    start.make_start()  # Starting node
                elif not end and clicked_node != start:
                    end = clicked_node
                    end.make_end()  # Ending node
                else:
                    clicked_node.make_wall()

            elif pygame.mouse.get_pressed()[2]:  # Right Click, clear nodes
                clicked_position = pygame.mouse.get_pos()
                row, col = get_clicked_position(mouse_position=clicked_position, total_rows=nr_grid_rows,
                                                screen_width=screen_width)
                clicked_node = node_list[row][col]
                clicked_node.reset_node()

                if clicked_node == start:
                    start = None
                elif clicked_node == end:
                    end = None

            # Start visualizer on return key:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and start and end:
                    for row in node_list:
                        for node in row:
                            node.update_neighbors(node_list)

                    algorithm(lambda: draw(surface, node_list, nr_grid_rows, screen_width), node_list, start, end)

                if event.key == pygame.K_SPACE:
                    start = None
                    end = None
                    # overwrite node list with a list of grids
                    node_list = nodes_list(total_rows=nr_grid_rows, width=screen_width)

    pygame.quit()
