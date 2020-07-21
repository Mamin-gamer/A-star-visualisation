import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import time
FPS = 120


try:
    import pygame
except Exception as e:
    raise e


WIN_HEIGHT = 600
WIN_WIDTH = 800

BLACK = (0, 0, 0)           # Walls
WHITE = (255, 255, 255)     # Grid
GREEN = (0, 255, 0)         # Start Node
RED =   (255, 0, 0)         # End node
BLUE =  (0, 0, 255)         # Parent
LIGHT_BLUE = (18, 231, 255 )# Children Node
YELLOW = (255,255,0)        # Solved root
GREY = (163, 163, 163)      # Separation on the grid

wall_number = -1
start_node_number = 1
end_node_number = 2
child_node_number = 3
parent_node_number = 4
solved_root_number = 5

wall_colour = BLACK
start_node_colour = GREEN
end_node_colour = RED
child_node_colour = LIGHT_BLUE
parent_node_colour = BLUE
solved_root_colour = YELLOW


class Node:

    def __init__(self, parent, position):
        self.parent = parent
        self.pos = self.position = position

        self.gCost = 0
        self.hCost = 0
        self.fCost = 0

        if self.parent is not None:
            a = abs(self.pos[0] - end_node.pos[0])
            b = abs(self.pos[1] - end_node.pos[1])

            self.gCost = parent.gCost + ((self.position[0]-parent.position[0])**2 + (self.position[1]-parent.position[1])**2 )**0.5
            self.hCost = a+b

            self.fCost = self.gCost + self.hCost


    def __eq__(self, others):
        if self.pos == others.pos:
            return True
        else:
            return False




class Grid:
    def __init__(self, size_of_square):
        self.size = size_of_square
        self.grid = [[0 for i in range(WIN_WIDTH//size)] for j in range(WIN_HEIGHT//size)]
        self.grid[0][0] = start_node_number
        self.grid[-1][-1] = end_node_number

        self.start_node = self.get_node_pos(start_node_number)
        self.end_node = self.get_node_pos(end_node_number)



    def get_node_pos(self, number):
        for row in range(len(self.grid)):
            try:
                return (self.grid[row].index(number), row)
            except:
                pass



    def display(self, win):
        win.fill(WHITE)
        colours = [WHITE, start_node_colour, end_node_colour, child_node_colour, parent_node_colour, solved_root_colour, wall_colour]
        for row in range(len(self.grid)):
            for column in range(len(self.grid[row])):
                index = self.grid[row][column]
                colour = colours[index]

                if index!=0:
                    pygame.draw.rect(win, colour, (self.size * column, self.size * row, self.size, self.size))

                pygame.draw.line(win, GREY, (0, self.size * row), (WIN_WIDTH, self.size*row))
                pygame.draw.line(win, GREY, (self.size*column, 0), (self.size*column, WIN_HEIGHT))


    def clear(self, win, walls = True):
        if walls == True:
            nums = [-1,3,4,5]
        else:
            nums = [3,4,5]
        for row in range(len(self.grid)):
            for column in range(len(self.grid[row])):
                if self.grid[row][column] in nums:
                    self.grid[row][column] = 0



    def get_pos_on_grid(self, position):
        x, y = position
        result = (x//self.size, y//self.size)

        if 0 <= result[1] < len(self.grid) and 0 <= result[0] < len(self.grid[0]):
            return result
        else:
            return None



    def move_node(self, number, position):
        pos_x, pos_y = position
        if self.grid[pos_y][pos_x] not in [1,2]:
            x, y = self.get_node_pos(number)
            self.grid[y][x] = 0
            self.grid[pos_y][pos_x] = number



def get_children(position, current_node):
    n = (0,1,2,3,4,5)
    x, y = position
    down = False
    up = False
    left_up = False
    left_down = False
    right_up = False
    right_down = False
    h_len = len(grid.grid[0])
    v_len = len(grid.grid)
    children = []
    if y < v_len-1:
        y1 = y+1
        x1 = x
        down = True
        if grid.grid[y1][x1] in n:
            children.append(Node(current_node, (x1, y1)))
            left_down = True
            right_down = True

    if y > 0:
        y1 = y-1
        x1 = x
        up = True
        if grid.grid[y1][x1] in n:
            children.append(Node(current_node, (x1, y1)))
            left_up = True
            right_up = True

    if x < h_len-1:
        y1 = y
        x1 = x+1
        if grid.grid[y1][x1] in n:
            children.append(Node(current_node, (x1,y1)))
            right_up = True
            right_down = True

        else:
            right_up = False
            right_down = False
        if right_up and up:
            y1 = y-1
            if grid.grid[y1][x1] in n:
                children.append(Node(current_node, (x1,y1)))
        if right_down and down:
            y1 = y+1
            if grid.grid[y1][x1] in n:
                children.append(Node(current_node, (x1, y1)))
    if x > 0:
        y1 = y
        x1 = x-1
        if grid.grid[y1][x1] in n:
            children.append(Node(current_node, (x1, y1)))
            left_up = True
            left_down = True

        if left_up and up:
            y1 = y-1
            if grid.grid[y1][x1] in n:
                children.append(Node(current_node, (x1, y1)))
        if left_down and down:
            y1 = y+1
            if grid.grid[y1][x1] in n:
                children.append(Node(current_node, (x1, y1)))

    return children

def check_list(list, object):
    try:
        return list.index(object)
    except:
        return -1

def main():
    grid.display(win)
    run = True
    editing = False
    deleting = False
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                return

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_c:
                    grid.clear(win, walls = True)


                elif event.key == pygame.K_SPACE:
                    grid.clear(win, walls = False)


                    start = time.time()
                    solve_grid(win)
                    end = time.time()
                    print(end-start)

                    pygame.event.clear()
                    grid.display(win)


                elif event.key == pygame.K_s:
                    mouse_pos = pygame.mouse.get_pos()
                    pos_on_grid = grid.get_pos_on_grid(mouse_pos)

                    if pos_on_grid is not None:

                        if 0 <= pos_on_grid[1] < len(grid.grid) and 0 <= pos_on_grid[0] < len(grid.grid[0]):
                            grid.move_node(start_node_number, pos_on_grid)


                elif event.key == pygame.K_e:
                    mouse_pos = pygame.mouse.get_pos()
                    pos_on_grid = grid.get_pos_on_grid(mouse_pos)

                    if pos_on_grid is not None:

                        if 0 <= pos_on_grid[1] < len(grid.grid) and 0 <= pos_on_grid[1] < len(grid.grid[0]):
                            grid.move_node(end_node_number, pos_on_grid)

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    pos_on_grid = grid.get_pos_on_grid(mouse_pos)

                    if pos_on_grid is not None:
                        x, y = pos_on_grid
                        value = grid.grid[y][x]

                    if value in [0,3,4,5,-1]:
                        editing = True
                        grid.grid[y][x] = -1



                elif event.button == 3:


                    mouse_pos = pygame.mouse.get_pos()
                    pos_on_grid = grid.get_pos_on_grid(mouse_pos)

                    if pos_on_grid is not None:
                        x,y = pos_on_grid
                        value = grid.grid[y][x]

                    if value in [-1, 0]:
                        deleting = True
                        grid.grid[y][x] = 0


            elif event.type == pygame.MOUSEBUTTONUP:

                deleting = False
                editing = False

        if deleting or editing:
            mouse_pos = pygame.mouse.get_pos()
            pos_on_grid = grid.get_pos_on_grid(mouse_pos)

            if pos_on_grid is not None:
                x, y = pos_on_grid
                value = grid.grid[y][x]


                if editing == True:
                    if value in [0,3,4,5]:
                        grid.grid[y][x] = -1


                if deleting == True:
                    if value in [-1, 0]:
                            grid.grid[y][x] = 0

        grid.display(win)
        pygame.display.update()

def solve_grid(win):

    clock = pygame.time.Clock()
    global end_node, start_node
    solve = True

    start_node = Node(None, grid.get_node_pos(start_node_number))
    end_node = Node(None, grid.get_node_pos(end_node_number))

    open_list = [start_node]
    closed_list = []

    while solve == True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                solve = False
                grid.clear(win, walls = True)
                return

        clock.tick(FPS)

        if not open_list:
            print('No path found')
            solve = False
            return



        current_node = min(open_list, key = lambda x: x.fCost)
        current_index = open_list.index(current_node)

        if current_node.pos == end_node.pos:
            solve = False
            break


        children = get_children(current_node.pos, current_node)

        open_list.pop(current_index)
        closed_list.append(current_node)


        for child in children:

            if child.pos == end_node.pos:
                solve = False
                break

            index1 = check_list(open_list, child)
            index2 = check_list(closed_list, child)

            if index1 >= 0 and open_list[index1].fCost > child.fCost:
                open_list.pop(index1)
                open_list.append(child)


            if index1 >= 0 and closed_list[index2].fCost > child.fCost:
                closed_list.pop(index2)
                open_list.append(child)

            if index1 == -1 and index2 == -1:
                open_list.append(child)

            # if child in open_list:
            #     y,x = child.pos
            #     if grid.grid[x][y] in [1,2]:
            #         pass
            #     else:
            #         grid.grid[x][y] = child_node_number
            #
            #
            # if child in closed_list:
            #     y,x = child.pos
            #     if grid.grid[x][y] in [1,2]:
            #         pass
            #     else:
            #         grid.grid[x][y] = parent_node_number

        for node in open_list:
            y, x = node.pos
            if grid.grid[x][y] in [1,2]:
                pass
            else:
                grid.grid[x][y] = child_node_number


        for node in closed_list:
            y, x = node.pos
            if grid.grid[x][y] in [1,2]:
                pass
            else:
                grid.grid[x][y] = parent_node_number

        pygame.display.update()
        grid.display(win)




    path = []

    while current_node is not None:
        x, y  = current_node.pos
        if grid.grid[y][x] in (0,3,4,5) and (y,x) != start_node.pos:
            path.append(current_node)
            grid.grid[y][x] = solved_root_number
        current_node = current_node.parent

    pygame.display.update()


size = 0
while not 10 <= size <=50:
    try:
        size = int(input('Size of a square (Integer) between 10 and 50\n-->\t'))
    except:
        print('Number should be integer, try again\n\n')


if __name__ == '__main__':

    grid = Grid(size)

    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    pygame.display.set_caption('A* path finder visualisation')

    main()
