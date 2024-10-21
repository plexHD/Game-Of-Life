import pygame
import time
import os

window_width = 600
window_height = 600
enabledGrid = 1
steptime = 150
path = os.path.dirname(__file__)

# read settings

try:
    with open(os.path.dirname(__file__) + "\\settings.txt", "r") as settings:
        settingsString = settings.read()
        settingsArr = []
        attributes = []
        for char in settingsString:
            attributes.append(char)
            if char == "=":
                attributes = []
            if char == "\n":
                string = ""
                for i in attributes:
                    string += i
                settingsArr.append(int(string))
        print("Successfully read settings-file: ", settingsArr)
        enabledGrid = settingsArr[0]
        steptime = settingsArr[1]
except:
    print("Settings could not be loaded or are not correctly formatted. Default values will apply.")

def main():
    pygame.init()

    screen = pygame.display.set_mode([window_width, window_height])
    pygame.display.set_caption("Game of Life")
    font = pygame.font.Font(path + "\\Symtext.ttf", 10)

    if enabledGrid == 1:
        screen.fill((255, 255, 255))
    else:
        screen.fill((0, 0, 0))

    clock = pygame.time.Clock()
    timer = 0

    grid = [] # x, y, state (0: dead, 1: alive)
    baseGrid = [] # grid saved before simulation
    sizeFactor = 30

    for i in range(int(window_height / sizeFactor)):
        row = []
        for j in range(int(window_width / sizeFactor)):
            row.append(0)
        grid.append(row)
    
    running = True
    mode = 0 # 0: drawing mode, 1: simulation mode
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                if event.key == pygame.K_SPACE:
                    if mode == 0:
                        print("simulation started")
                        print(grid)
                        baseGrid = grid
                        mode = 1
                    else:
                        print("simulation reset")
                        mode = 0
                        for y in range(len(grid)):
                            for x in range(len(grid[y])):
                                grid[y][x] = 0
        timer += clock.tick()
        if mode == 0:
            if pygame.mouse.get_pressed()[0] == True:
                for y in range(len(grid)):
                    for x in range(len(grid[y])):
                        if x * sizeFactor < pygame.mouse.get_pos()[0] < x * sizeFactor + sizeFactor:
                            if y * sizeFactor < pygame.mouse.get_pos()[1] < y * sizeFactor + sizeFactor:
                                if grid[y][x] == 0:
                                    grid[y][x] = 1
        elif mode == 1 and timer >= steptime:
            timer = 0
            gridCopy = []
            for y in range(len(grid)):
                row = []
                for x in range(len(grid[y])):
                    row.append(grid[y][x])
                gridCopy.append(row)
            for y in range(len(grid)):
                for x in range(len(grid[y])):
                    aliveNeighbours = 0
                    for yValue in range(y -1, y +2):
                        if yValue not in range(len(grid)): continue
                        for xValue in range(x -1, x +2):
                            if xValue not in range(len(grid[y])): continue
                            if xValue == x and yValue == y: continue
                            if grid[yValue][xValue] == 1:
                                aliveNeighbours += 1

                    if grid[y][x] == 1:
                        if aliveNeighbours < 2:
                            gridCopy[y][x] = 0
                        elif aliveNeighbours > 3:
                            gridCopy[y][x] = 0
                        elif 2 < aliveNeighbours < 3:
                            gridCopy[y][x] = 1
                    elif grid[y][x] == 0:
                        if aliveNeighbours == 3:
                            gridCopy[y][x] = 1
            grid = []
            for y in range(len(gridCopy)):
                row = []
                for x in range(len(gridCopy[y])):
                    row.append(gridCopy[y][x])
                grid.append(row)
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == 0:
                    tileColor = (0, 0, 0)
                elif grid[y][x] == 1:
                    tileColor = (255, 255, 255)
                pygame.draw.rect(screen, tileColor, pygame.Rect([x * sizeFactor +1, y * sizeFactor +1], (sizeFactor -2, sizeFactor -2)))
        pygame.display.update()
main()