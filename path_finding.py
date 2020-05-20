try:
    import pygame
    import sys
    import math
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
    import os
except:
    import install_requirements  # install packages

    import pygame
    import sys
    import math
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
    import os

screen = pygame.display.set_mode((800, 800))


class spot:
    def __init__(self, x, y):
        self.i = x
        self.j = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.nxtgrid = []
        self.previous = None
        self.obs = False
        self.closed = False
        self.value = 1

    def show(self, color, st):
        if self.closed == False:
            pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
            pygame.display.update()

    def path(self, color, st):
        pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
        pygame.display.update()

    def addnxtgrid(self, grid):
        i = self.i
        j = self.j
        if i < cols - 1 and grid[self.i + 1][j].obs == False:
            self.nxtgrid.append(grid[self.i + 1][j])
        if i > 0 and grid[self.i - 1][j].obs == False:
            self.nxtgrid.append(grid[self.i - 1][j])
        if j < row - 1 and grid[self.i][j + 1].obs == False:
            self.nxtgrid.append(grid[self.i][j + 1])
        if j > 0 and grid[self.i][j - 1].obs == False:
            self.nxtgrid.append(grid[self.i][j - 1])


cols = 50
grid = [0 for i in range(cols)]
row = 50
open_Set = []
closed_Set = []
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (220, 220, 220)
light_blue = (0, 204, 204)
w = 800 / cols
h = 800 / row
cameFrom = []

# creating a 2d array
for i in range(cols):
    grid[i] = [0 for i in range(row)]

# Creating the initial and final points
for i in range(cols):
    for j in range(row):
        grid[i][j] = spot(i, j)

# Setting of starting and ending node
start = grid[12][5]
end = grid[3][6]
# SHOW RECT
for i in range(cols):
    for j in range(row):
        grid[i][j].show((25, 255, 255), 1)

for i in range(0, row):
    grid[0][i].show(light_blue, 0)
    grid[0][i].obs = True
    grid[cols - 1][i].obs = True
    grid[cols - 1][i].show(light_blue, 0)
    grid[i][row - 1].show(light_blue, 0)
    grid[i][0].show(light_blue, 0)
    grid[i][0].obs = True
    grid[i][row - 1].obs = True


def onsubmit():
    global start
    global end
    st = start_node.get().split(',')
    ed = end_node.get().split(',')
    start = grid[int(st[0])][int(st[1])]
    end = grid[int(ed[0])][int(ed[1])]
    window.quit()
    window.destroy()


window = Tk()
label = Label(window, text='start state(x,y): ')
start_node = Entry(window)
label1 = Label(window, text='goal state(x,y): ')
end_node = Entry(window)
var = IntVar()
showPath = ttk.Checkbutton(window, text='Show visualisation :', onvalue=1, offvalue=0, variable=var)

submit = Button(window, text='Submit', command=onsubmit)

showPath.grid(columnspan=2, row=2)
submit.grid(columnspan=2, row=3)
label1.grid(row=1, pady=3)
end_node.grid(row=1, column=1, pady=3)
start_node.grid(row=0, column=1, pady=3)
label.grid(row=0, pady=3)

window.update()
mainloop()

pygame.init()
open_Set.append(start)


def mousePress(x):
    t = x[0]
    w = x[1]
    g1 = t // (800 // cols)
    g2 = w // (800 // row)
    acess = grid[g1][g2]
    if acess != start and acess != end:
        if acess.obs == False:
            acess.obs = True
            acess.show((255, 255, 255), 5)


end.show((255, 8, 127), 0)
start.show((255, 5, 127), 0)

loop = True
while loop:
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mousePress(pos)
            except AttributeError:
                pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                loop = False
                break

for i in range(cols):
    for j in range(row):
        grid[i][j].addnxtgrid(grid)


def heuristic_val(n, e):
    d = math.sqrt((n.i - e.i) ** 2 + (n.j - e.j) ** 2)
    # d = abs(n.i - e.i) + abs(n.j - e.j)
    return d


def main_func():
    end.show((62, 8, 127), 0)
    start.show((255, 5, 127), 0)
    k = 0
    if len(open_Set) > 0:
        lIndx = 0
        # for i in range(len(open_Set)):
        while k < len(open_Set):
            if open_Set[k].f < open_Set[lIndx].f:
                lIndx = k
            k += 1
        current_val = open_Set[lIndx]
        if current_val == end:
            print('done', current_val.f)
            start.show((255, 125, 127), 0)
            temp = current_val.f
            j = 0
            for i in range(round(current_val.f)):
                current_val.closed = False
                current_val.show((0, 127, 255), 1)
                current_val = current_val.previous
            end.show((255, 128, 127), 0)

            if confirm(temp) == True:
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                ag = True
                while ag:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            ag = False
                            break
            quit()

        open_Set.pop(lIndx)
        closed_Set.append(current_val)

        nxtgrid = current_val.nxtgrid
        for i in range(len(nxtgrid)):
            neighbor = nxtgrid[i]
            if neighbor not in closed_Set:
                tgrid = current_val.g + current_val.value
                if neighbor in open_Set:
                    if neighbor.g > tgrid:
                        neighbor.g = tgrid
                else:
                    neighbor.g = tgrid
                    open_Set.append(neighbor)

            neighbor.h = heuristic_val(neighbor, end)
            neighbor.f = neighbor.g + neighbor.h

            if neighbor.previous == None:
                neighbor.previous = current_val
    if var.get():
        l = 0
        while l < len(open_Set):
            open_Set[l].show(green, 0)
            l += 1

        for i in range(len(closed_Set)):
            if closed_Set[i] != start:
                closed_Set[i].show(red, 0)
    current_val.closed = True


def confirm(temp):
    Tk().wm_withdraw()
    return messagebox.askokcancel('Program Finished', (
            'The SHORTEST DISTANCE IS FOUND, the shortest distance \n to the given points is ' + str(
        temp) + ' grids away, \n would you like to re run the program?'))


def quit():
    pygame.quit()


while True:
    ev = pygame.event.poll()

    if ev.type == pygame.QUIT:
        quit()
    pygame.display.update()
    main_func()
