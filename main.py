#first imports of modules that will be in work
#os module is only for hiding pygame "hello" stuff
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import time

#trying to import pygame module, otherwise error will occure
try:
    import pygame
    pygame.font.init()
except Exception as e:
    raise e

#setting constants for all purpose
FPS = 120
MAIN_BUTTON_WIDTH = 150
MAIN_BUTTON_HEIGHT = 50
BACK_BUTTON_WIDTH = 50
BACK_BUTTON_HEIGHT = 50

WIN_HEIGHT = 600
WIN_WIDTH = 800

#setting colours for everything
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

#Node class that will be a "block" on the grid
class Node:
    #takes parent and position of the node, except start and end nodes where parents are None
    def __init__(self, parent, position):
        self.parent = parent
        self.pos = self.position = position

        #setting costs and length of path
        self.gCost = 0
        self.hCost = 0
        self.fCost = 0
        self.length = 0

        #checking is parent exists (not start and end) and makes g cost and f cost
        if self.parent is not None:
            a = abs(self.pos[0] - end_node.pos[0])
            b = abs(self.pos[1] - end_node.pos[1])

            self.gCost = parent.gCost + ((self.position[0]-parent.position[0])**2 + (self.position[1]-parent.position[1])**2 )**0.5
            self.length = ((self.position[0]-parent.position[0])**2 + (self.position[1]-parent.position[1])**2 )**0.5
            self.hCost = a+b

            self.fCost = self.gCost + self.hCost

    #speciall class that makes comparacing available between nodes
    def __eq__(self, others):
        return self.pos == others.pos

#class grid that draws the grid itself with lines and so one
class Grid:
    #initialising grid with square size that was set in the very beginning
    def __init__(self, size_of_square):
        self.size = size_of_square
        #making grid with all 0s
        self.grid = [[0 for i in range(WIN_WIDTH//size)] for j in range(WIN_HEIGHT//size)]
        #setting start position at top left corner
        self.grid[0][0] = start_node_number
        #setting end node position at the bottom right corner
        self.grid[-1][-1] = end_node_number

        self.start_node = self.get_node_pos(start_node_number)
        self.end_node = self.get_node_pos(end_node_number)


    #function to retreive position of node on the grid (brute force)
    def get_node_pos(self, number):
        for row in range(len(self.grid)):
            try:
                return (self.grid[row].index(number), row)
            except:
                pass


    #basic grid draw from top-left to borrom right corner
    def display(self, win):
        win.fill(WHITE)     #fills screen with white colour
        #makes array of colours that corresponds to numbers on the grid
        colours = [WHITE, start_node_colour, end_node_colour, child_node_colour, parent_node_colour, solved_root_colour, wall_colour]
        #basic brute force colouring grid
        for row in range(len(self.grid)):
            for column in range(len(self.grid[row])):
                index = self.grid[row][column]
                colour = colours[index]
                #if cell isn`t 0 (white) it colours it at the space counted
                if index!=0:
                    pygame.draw.rect(win, colour, (self.size * column, self.size * row, self.size, self.size))
                #draws vertical and horizontal lines throung out all rows and columns
                pygame.draw.line(win, GREY, (0, self.size * row), (WIN_WIDTH, self.size*row))
                pygame.draw.line(win, GREY, (self.size*column, 0), (self.size*column, WIN_HEIGHT))

    #function that clears either walls and path or path only, depending on where it`s called from
    def clear(self, win, walls = True):
        if walls == True:
            nums = [-1,3,4,5]
        else:
            nums = [3,4,5]

        #for each posiiton on grid, sets it to 0 (white)
        for row in range(len(self.grid)):
            for column in range(len(self.grid[row])):
                if self.grid[row][column] in nums:
                    self.grid[row][column] = 0


    #function that depending on real mouse positon returns positon on the grid in row/column
    def get_pos_on_grid(self, position):
        x, y = position
        result = (x//self.size, y//self.size)

        if 0 <= result[1] < len(self.grid) and 0 <= result[0] < len(self.grid[0]):
            return result
        else:
            return None


    #function to move node
    def move_node(self, number, position):
        #gets position of node and places it there
        pos_x, pos_y = position
        if self.grid[pos_y][pos_x] not in [1,2]:
            x, y = self.get_node_pos(number)
            self.grid[y][x] = 0
            self.grid[pos_y][pos_x] = number

#colours child and parent nodes
def display_found(open_list, closed_list):

    #searches througn open list(where cnildren are stored)
    for node in open_list:
        y, x = node.pos
        if grid.grid[x][y] in [1,2]:
            pass
        else:
            grid.grid[x][y] = child_node_number


    #searches througn closed list(where parents are stored)
    for node in closed_list:
        y, x = node.pos
        if grid.grid[x][y] in [1,2]:
            pass
        else:
            grid.grid[x][y] = parent_node_number

    #updates the screen and refreshes it
    pygame.display.update()
    grid.display(win)

#function to display solved root (final path)
def display_root(current_node):
    path = []
    length = 0
    #unconditional loop that stops only at start node
    while current_node is not None:
        x, y  = current_node.pos
        if grid.grid[y][x] in (0,3,4,5) and (y,x) != start_node.pos:
            path.append(current_node)
            grid.grid[y][x] = solved_root_number
        length += current_node.length
        current_node = current_node.parent

    pygame.display.update()
    return length

#function to get posiible locations to place children
#it avoids cutting corners (going through them)
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

#basic function to check if item is in the list
#faster method rather than linear search as it takes O(1)
def check_list(list, object):
    try:
        return list.index(object)
    except:
        return -1
#button class that is used only in main menu
class Button:
    #declares variables for buttons
    def __init__(self, x, y, width, height, text, colour = None, font = None):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.text = text

        if colour:
            self.colour = colour
        else:
            self.colour = (0,0,0)

        self.copy = self.colour

        if font:
            self.font = font
        else:
            self.font = pygame.font.SysFont('comsicsans', 40)

    #displays button on window
    def draw(self, win, outline = (0,0,0)):
        if self.text:
            writing = self.font.render(self.text, 1, self.colour)
        #if outline exists it will draw outline
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 3)
        # pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height), 0)
        win.blit(writing, (self.x + (self.width//2 - writing.get_width()//2), self.y + (self.height//2 - writing.get_height()//2)))
        pygame.display.update()

    #checks if cursor is over the button
    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

def blit_text(surface, text, pos = (0,0), font = None, max_width = 0, padding_left = 0, padding_right = 0, colour=pygame.Color('black')):
    #function must take 2 arguments: window itself and text, optional are: position of the text`s top left corner, pygame font, width of the text e.g. width of block in css/html
            #padding from both sides to control positions better and colour of the font
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.

    #if max_width wasn`t changet, it declares it as window`s width-padding
    if max_width == 0:
        max_width = surface.get_width() - padding_right - padding_right

    max_height = surface.get_height()

    #changes x-position of the pos tuple to add the paddinf up
    pos = list(pos)
    pos[0] += padding_left
    x, y = pos


    #iterates through each line in the 2D array
    for line in words:
        #iterates through each word in line
        for word in line:
            word_surface = font.render(word, 0, colour)
            word_width, word_height = word_surface.get_size()
            #checks if starting coordinate + width of the word is less than maximal width available
            # BUG: text can go off the edge because of max_width and starting position, however it won`t go off is starting positon is 0
            if x + word_width >= max_width + pos[0]:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space*2
        x = pos[0]  # Reset the x.
        y += word_height


#sets main function where everything will be run
def main():
    #sets 2 types of font
    font = pygame.font.SysFont('comsicsans', 60)
    sub_font = pygame.font.SysFont('comsicsans', 40)
    buttons = []
    #3 buttons only, for 2 types of algoritms yet and exit button
    astar_btn = Button(x = win.get_width()//2 - MAIN_BUTTON_WIDTH//2, y = 300, width = MAIN_BUTTON_WIDTH, height = MAIN_BUTTON_HEIGHT, text = 'A* (star)')
    dijkstra_btn = Button(x = win.get_width()//2 - MAIN_BUTTON_WIDTH//2, y = 400, width = MAIN_BUTTON_WIDTH, height = MAIN_BUTTON_HEIGHT, text = 'Dijkstra`s')
    exit_button = Button(x = 10, y = win.get_height() - 100, width = BACK_BUTTON_WIDTH, height = BACK_BUTTON_HEIGHT, text = 'Quit', colour = (0, 0, 0), font = (pygame.font.SysFont('comsicsans', 30)))

    buttons.extend([astar_btn, dijkstra_btn, exit_button])

    welcome_text = font.render('Path finding algorithms', 1, (0, 0, 0))
    #displays texts only
    text = '"Spacebar" - start; "S" - place the start node; "E" - place the end node; "C" - clear walls and root'
    win.fill((255,255,255))
    blit_text(win, text, pos = (60, 200), font = sub_font, max_width = 700)
    win.blit(welcome_text, (win.get_width()//2 - welcome_text.get_width()//2, 100))


    #mail infinate loop
    run = True
    while run:
        #gets postion on mouse
        pos = pygame.mouse.get_pos()
        #loops through pygame event
        for event in pygame.event.get():
            #if window closes - loops breaks and everything ends
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break
            #looping throung buttons and if mouse is over button it changes colour
            for btn in buttons:

                if btn.is_over(pos):
                    btn.colour = (255,0,0)
                else:
                    btn.colour = btn.copy


                #if mouse is clicked it checks is mouse position is over button it starts function
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if btn.is_over(pos):
                        if btn.text == 'A* (star)':
                            main_game('Astar')
                            win.blit(welcome_text, (win.get_width()//2 - welcome_text.get_width()//2, 100))
                            blit_text(win, text, pos = (60, 200), font = sub_font, max_width = 700)



                        if btn.text == 'Dijkstra`s':
                            main_game('Dijkstra')
                            win.blit(welcome_text, (win.get_width()//2 - welcome_text.get_width()//2, 100))
                            blit_text(win, text, pos = (60, 200), font = sub_font, max_width = 700)
                        #if quit is clicked - loop ends and everything closes
                        if btn.text == 'Quit':
                            run = False

                btn.draw(win)

    pygame.quit()

#main game function
def main_game(way):

    run = True
    editing = False
    deleting = False
    clock = pygame.time.Clock()

    #main loop
    while run:
        #sets clock ticks
        clock.tick(FPS)
        #loops througn pygame events
        for event in pygame.event.get():
            #if window closes - everything clears and goes to main menu with the same layout saved
            if event.type == pygame.QUIT:
                run = False

            #checks key pressed
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_c:
                    grid.clear(win, walls = True)


                elif event.key == pygame.K_SPACE:
                    grid.clear(win, walls = False)

                    #sets the starter time
                    start = time.time()

                    if way == 'Astar':
                        length = Astar(win)

                    elif way == 'Dijkstra':
                        length = Dijkstra(win)

                    end = time.time()
                    #sets the ending time

                    #tries to print length of path with its time, otherwise it will pring time only
                    try:
                        print(way, ': ', round(length, 3),'units in',round(end-start, 6), 'seconds')
                    except:
                        print(way, ': ', round(end-start, 6), 'seconds')


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


            #if left click: it will start editing
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


                #if right click: deleting starts
                elif event.button == 3:


                    mouse_pos = pygame.mouse.get_pos()
                    pos_on_grid = grid.get_pos_on_grid(mouse_pos)

                    if pos_on_grid is not None:
                        x,y = pos_on_grid
                        value = grid.grid[y][x]

                    if value in [-1, 0]:
                        deleting = True
                        grid.grid[y][x] = 0

            #if mouse if up - it ends editing and deleting
            elif event.type == pygame.MOUSEBUTTONUP:

                deleting = False
                editing = False


        #if any deleting or editing starts
        if deleting or editing:
            mouse_pos = pygame.mouse.get_pos()
            pos_on_grid = grid.get_pos_on_grid(mouse_pos)

            if pos_on_grid is not None:
                x, y = pos_on_grid
                value = grid.grid[y][x]

                #if editing: replaces value in grid with wall number
                if editing == True:
                    if value in [0,3,4,5]:
                        grid.grid[y][x] = wall_number

                # if deleting: replaces in grid with empty value (0)
                if deleting == True:
                    if value in [-1, 0]:
                            grid.grid[y][x] = 0

        grid.display(win)
        pygame.display.update()

    win.fill((255,255,255))

#function for A* algoritm
def Astar(win):
    clock = pygame.time.Clock()
    #sets global value for end and start nodes, the only way i foung out not to include them in every function
    global end_node, start_node
    solve = True

    start_node = Node(None, grid.get_node_pos(start_node_number))
    end_node = Node(None, grid.get_node_pos(end_node_number))

    open_list = [start_node]
    closed_list = []
    #infinate root in solving
    while solve == True:
        #checks pygame event
        for event in pygame.event.get():
            #if red cross is clicked - grid clears and returns
            if event.type == pygame.QUIT:
                solve = False
                grid.clear(win, walls = True)
                return

        clock.tick(FPS)
        #early exit
        if not open_list:
            print('No path found')
            solve = False
            return
        #sets current node with min function (O(1), faster than linear search) depending on total cost
        current_node = min(open_list, key = lambda x: x.fCost)
        current_index = open_list.index(current_node)

        #checks is positon of minimal node with f value is the same sa end node
        if current_node.pos == end_node.pos:
            solve = False
            break

        #generates children from current node, maximum of 8 (all aroung the node)
        children = get_children(current_node.pos, current_node)

        open_list.pop(current_index)
        closed_list.append(current_node)

        #loops througn all children
        for child in children:

            index1 = check_list(open_list, child)
            index2 = check_list(closed_list, child)


            if index1 >= 0 and open_list[index1].fCost > child.fCost:
                open_list.pop(index1)
                closed_list.append(child)

            if index1 >= 0 and closed_list[index2].fCost > child.fCost:
                closed_list.pop(index2)
                open_list.append(child)

            if index1 == -1 and index2 == -1:
                open_list.append(child)

        display_found(open_list, closed_list)

    length = display_root(current_node)
    return length


def Dijkstra(win):
    clock = pygame.time.Clock()
    #sets global variables for end and start node - only way i found
    global end_node, start_node
    solve = True

    start_node = Node(None, grid.get_node_pos(start_node_number))
    end_node = Node(None, grid.get_node_pos(end_node_number))

    open_list = [start_node]
    closed_list = []
    #infinate loop for solving
    while solve == True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                solve = False
                grid.clear(win, walls = True)
                return

        clock.tick(FPS*2)
        #if nothing is in the open list, where children should be, algorithm ends
        if not open_list:
            print('No path found')
            solve = False
            return

        current_node = min(open_list, key = lambda x: x.gCost)
        current_index = open_list.index(current_node)

        if current_node.pos == end_node.pos:
            solve = False
            break


        children = get_children(current_node.pos, current_node)

        open_list.pop(current_index)
        closed_list.append(current_node)


        for child in children:


            index1 = check_list(open_list, child)
            index2 = check_list(closed_list, child)

            if index1 >= 0 and open_list[index1].gCost > child.gCost:
                open_list.pop(index1)
                open_list.append(child)


            if index1 >= 0 and closed_list[index2].gCost > child.gCost:
                closed_list.pop(index2)
                open_list.append(child)

            if index1 == -1 and index2 == -1:
                open_list.append(child)

        display_found(open_list, closed_list)
    length = display_root(current_node)
    return length

size = 20


if __name__ == '__main__':
    grid = Grid(size)

    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    pygame.display.set_caption('path finder visualisation')

    main()
