import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

BLACK = (0, 0, 0)           # walls
WHITE = (255, 255, 255)     # Grid
GREEN = (0, 255, 0)         # Start Node
RED =   (255, 0, 0)         # End node
BLUE =  (0, 0, 255)         # Parent
LIGHT_BLUE = (18, 231, 255 )# children Node
YELLOW = (255,255,0)        #solved root

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

class BuildGrid:
    def __init__(self, size_of_square):
        self.size = size_of_square
        self.grid = [[0 for i in range(WINDOW_WIDTH//size)] for j in range(WINDOW_HEIGHT//size)]
        self.grid[0][0] = start_node_number
        self.grid[-1][-1] = end_node_number
        self.start_node = self.get_node_pos(start_node_number)
        self.end_node = self.get_node_pos(end_node_number)


    def move_node(self,number, position):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == number:
                    y,x = position
                    if self.grid[y][x] not in [1,2]:
                        self.grid[i][j] = 0
                        self.grid[y][x] = number
                        return

    def display(self):
        win.fill(WHITE)             #fills everything with white(plain grig with nothing on it)
        colours = [WHITE, start_node_colour, end_node_colour, child_node_colour, parent_node_colour, solved_root_colour, wall_colour]
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):     #searches throught 2D array(text base)
                index = self.grid[i][j]
                colour = colours[index]
                if index != 0:
                    pygame.draw.rect(win, colour, (self.size*j, self.size*i, self.size, self.size))

                pygame.draw.line(win, BLACK, (0, self.size*i), (WINDOW_WIDTH, self.size*i))
                pygame.draw.line(win, BLACK, (self.size*j, 0), (self.size*j, WINDOW_HEIGHT))



    def on_grid_pos(self, coordinates):
        self.column = coordinates[1]
        self.row = coordinates[0]
        result = (self.column//self.size, self.row//self.size)
        if 0 <= result[0] < len(self.grid) and 0 <= result[1] < len(self.grid[0]):
            return result
        else:
            return None


    def clear(self, walls):
        if walls == True:
            nums = [-1,3,4,5]   # list of all possible colours(nodes) that can meet up(at the very top)
        else:
            nums = [3,4,5]
        for i_y, val_y in enumerate(self.grid):
            for i_x, val_x in enumerate(self.grid[i_y]):
                if self.grid[i_y][i_x] in nums:
                    self.grid[i_y][i_x] = 0             #if node in anything except white its deleted

        # self.start_node = self.get_node_pos(start_node_number)
        # self.end_node = self.get_node_pos(end_node_number)


    def get_node_pos(self,node):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == node:
                    return (i,j)
        return None

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

def get_children(position, current_node):
    n = (0,1,2,3,4,5)
    y,x = position
    down = False
    up = False
    left_up = False
    left_down = False
    right_up = False
    right_down = False
    h_len = len(grid.grid[0]) # x, pos[1] #
    v_len = len(grid.grid) # y, pos[0] #
    children = []
    if y < v_len-1:
        y1 = y+1
        x1 = x
        down = True
        if grid.grid[y1][x1] in n:
            children.append(Node(current_node, (y1, x1)))
            left_down = True
            right_down = True

    if y > 0:
        y1 = y-1
        x1 = x
        up = True
        if grid.grid[y1][x1] in n:
            children.append(Node(current_node, (y1, x1)))
            left_up = True
            right_up = True

    if x < h_len-1:
        y1 = y
        x1 = x+1
        if grid.grid[y1][x1] in n:
            children.append(Node(current_node, (y1, x1)))
            right_up = True
            right_down = True

        else:
            right_up = False
            right_down = False
        if right_up and up:
            y1 = y-1
            if grid.grid[y1][x1] in n:
                children.append(Node(current_node, (y1, x1)))
        if right_down and down:
            y1 = y+1
            if grid.grid[y1][x1] in n:
                children.append(Node(current_node, (y1, x1)))
    if x > 0:
        y1 = y
        x1 = x-1
        if grid.grid[y1][x1] in n:
            children.append(Node(current_node, (y1, x1)))
            left_up = True
            left_down = True

        if left_up and up:
            y1 = y-1
            if grid.grid[y1][x1] in n:
                children.append(Node(current_node, (y1, x1)))
        if left_down and down:
            y1 = y+1
            if grid.grid[y1][x1] in n:
                children.append(Node(current_node, (y1, x1)))

    return children


def get_children2(position, current_node):
    allowed = (0,1,2,3,4,5)
    y1, x1 = position
    children = []
    for y in (-1,0,1):
        for x in (-1,0,1):
            if (y,x) == (0,0):
                continue
            try:
                y2 = abs(y1+y)
                x2 = abs(x1+x)
                if grid.grid[y2][x2] != -1:
                    children.append(Node(current_node, (y2, x2)))
            except:
                pass

    return children

def check2(list,object):
    try:
        return list.index(object)
    except:
        return -1


def check(list, object):
    if len(list) > 0:
        for i, val in enumerate(list):
            if object.position == val.position:
                return i
    return -1


def solve_grid():
    global start_node, end_node
    clock = pygame.time.Clock()
    solve = True
    start_node = Node(None, grid.get_node_pos(start_node_number))
    end_node = Node(None, grid.get_node_pos(end_node_number))

    open_list = []      #children
    closed_list = []    #parents

    open_list.append(start_node)

    while solve:
        if not open_list:
            print('no path found')
            solve = False
            return


        current_node = open_list[-1]
        # current_index = open_list.index(current_node)
        current_index = -1

        for val in open_list:
            if val.fCost < current_node.fCost:
                current_node = val
                current_index = open_list.index(val)


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

            index1 = check2(open_list, child)
            index2 = check2(closed_list, child)

            if index1 >= 0 and open_list[index1].fCost > child.fCost:

                open_list.pop(index1)
                open_list.append(child)

            if index1 >= 0 and closed_list[index2].fCost > child.fCost:

                closed_list.pop(index2)
                open_list.append(child)

            if index1 == -1 and index2 == -1:
                open_list.append(child)


        for node in closed_list:
            y,x = node.pos
            if grid.grid[y][x] in [1,2]:
                pass
            else:
                grid.grid[y][x] = parent_node_number


        for node in open_list:
            y,x = node.pos
            if node.pos in [1,2]:
                pass
            else:
                grid.grid[y][x] = child_node_number

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        grid.display()
        pygame.display.flip()



    path = []
    while current_node is not None:
        y,x = current_node.pos
        if grid.grid[y][x] in [0,3,4,5] and (y,x) != start_node.position:
            path.append(current_node)
        current_node = current_node.parent

    path = reversed(path)
    for elem in path:
        y, x = elem.position
        grid.grid[y][x] = solved_root_number
        grid.display()
        pygame.display.flip()

    return




size = 0
while not 10 <= size <= 50:
    size = int(input('Size of a square (integer)'))

grid = BuildGrid(size)
start_node = grid.get_node_pos(start_node_number) # calls funtion to retreive position
end_node = grid.get_node_pos(end_node_number)

def main():
    grid.display()
    run = True
    editing = False
    deleting = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                return
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_c:
                    grid.clear(True)

                elif event.key == pygame.K_SPACE:
                    grid.clear(False)
                    start = time.time()
                    solve_grid()
                    end = time.time()
                    print(end-start)
                    pygame.event.clear()
                    grid.display()

                elif event.key == pygame.K_s:
                    m_pos = pygame.mouse.get_pos()
                    grid_pos = grid.on_grid_pos(m_pos)
                    if grid_pos is not None:
                        if 0 <= grid_pos[0] < len(grid.grid) and 0 <= grid_pos[1] < len(grid.grid[0]):
                            grid.move_node(start_node_number, grid_pos)


                elif event.key == pygame.K_e:
                        m_pos = pygame.mouse.get_pos()
                        grid_pos = grid.on_grid_pos(m_pos)
                        if grid_pos is not None:
                            if 0 <= grid_pos[0] < len(grid.grid) and 0 <= grid_pos[1] < len(grid.grid[0]):
                                grid.move_node(end_node_number, grid_pos)



            if event.type == pygame.MOUSEBUTTONDOWN:    #mouse is down
                if event.button == 1:

                    cursor_position = pygame.mouse.get_pos()
                    cursor_position = grid.on_grid_pos(cursor_position)

                    if cursor_position is not None:
                        y,x = cursor_position
                        value = grid.grid[y][x]

                        if value in [0,3,4,5,-1]:
                            editing = True
                            grid.grid[y][x] = -1


                elif event.button == 3:
                     cursor_position = pygame.mouse.get_pos()
                     cursor_position = grid.on_grid_pos(cursor_position)

                     if cursor_position is not None:
                         y,x = cursor_position
                         value = grid.grid[y][x]
                         if value == -1:
                             deleting = True

            elif event.type == pygame.MOUSEBUTTONUP:
                deleting = False
                editing = False


            if deleting or editing:
                position = pygame.mouse.get_pos()
                position = grid.on_grid_pos(position)


                if position is not None:
                    y,x = position
                    val = grid.grid[y][x]

                    if editing == True:
                        if val in [0,3,4,5]:
                            grid.grid[y][x] = -1

                    if deleting == True:
                        if val in [-1, 0]:
                            grid.grid[y][x] = 0


        grid.display()
        pygame.display.flip()


win = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('A* path finder visualisation')

main()
