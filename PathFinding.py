import math
#import moveTest
from matplotlib import pyplot
import multiprocessing
import random

def displayPath(env, path):
    print('displaying path...')
    obstList = []
    bfMap = [[0 for col in row] for row in env]
    for yindex, row in enumerate(env):
        for xindex, col in enumerate(row):
            # if col != 254:
            if col == 0:
                obstList.append((xindex, yindex))
                bfMap[yindex][xindex] = 1
            else:
                bfMap[yindex][xindex] = 0

    for state in path[:-1]:
        bfMap[state[1]][state[0]] = 5

    pyplot.imshow(bfMap, pyplot.cm.gray)
    print('Done converting to image')
    pyplot.show()

def gradientDescent(env, start, goal, bfarr, wfarr):
    #bfarr = brushfire(map)
    path = [start]
    current = []
    print('Adding bf and wf arrs')

    bfarr = [[min(50, x) for x in row] for row in bfarr]
    bfmax = max(map(max, bfarr))
    wfmax = max(map(max, wfarr))

    bfnorm = []
    wfnorm = []

    for bfrow, wfrow in zip(bfarr, wfarr):
        bfnorm.append([col / bfmax for col in bfrow])
        wfnorm.append([col / wfmax for col in wfrow])

    pyplot.imshow(wfnorm, pyplot.cm.gray)
    pyplot.show()
    pyplot.imshow(bfnorm, pyplot.cm.gray)
    pyplot.show()
    farr = [[2 * w - b for w, b in zip(wrow, brow)] for wrow, brow in zip(wfnorm, bfnorm)]
    #farr = bfnorm + wfnorm
    print('Done adding arrs, converting to image...')

    pyplot.imshow(farr, pyplot.cm.gray)
    print('Done converting to image...')
    pyplot.show()
    print('Performing gd algorithm...')
    while not path[-1] == goal:
        if (not path[-1]) or path[-1] in path[:-1]:
            displayPath(env, path)
            return None
        current = path[-1]
        repVec = gradientRep(bfarr, current[0], current[1])
        nextStates = validNext(current, env)

        minscore = math.inf
        minnext = []
        for next in nextStates:
            if next and (manhattan(next, goal) + manhattan(next, start)) + farr[next[1]][next[0]] < minscore and next not in path:
                minnext = next
                minscore = manhattan(minnext, goal) + manhattan(next, start) + farr[next[1]][next[0]]
        path.append(minnext)

        #moveTest.move((current[0], current[1]), (minnext[0], minnext[1]))
        # diffx = current[0] - minnext[0]
        # diffy = current[1] - minnext[1]
    print('gd alglorithm complete...')
    displayPath(env, path)
    return path

def _bfworker(current, bfMap, env, frontier):
    xMax = len(env[0]) - 1
    yMax = len(env) - 1
    if current[0][0] > 0:
        x = current[0][0] - 1
        y = current[0][1]
        if env[y][x] == 254 and bfMap[y][x] > current[1] + 1:
            bfMap[y][x] = current[1] + 1
            if (x, y) not in [x[0] for x in frontier]:
                frontier.append([(x, y), current[1] + 1])
    if current[0][0] < xMax:
        x = current[0][0] + 1
        y = current[0][1]
        if env[y][x] == 254 and bfMap[y][x] > current[1] + 1:
            bfMap[y][x] = current[1] + 1
            if (x, y) not in [x[0] for x in frontier]:
                frontier.append([(x, y), current[1] + 1])
    if current[0][1] > 0:
        x = current[0][0]
        y = current[0][1] - 1
        if env[y][x] == 254 and bfMap[y][x] > current[1] + 1:
            bfMap[y][x] = current[1] + 1
            if (x, y) not in [x[0] for x in frontier]:
                frontier.append([(x, y), current[1] + 1])
    if current[0][1] < yMax:
        x = current[0][0]
        y = current[0][1] + 1
        if env[y][x] == 254 and bfMap[y][x] > current[1] + 1:
            bfMap[y][x] = current[1] + 1
            if (x, y) not in [x[0] for x in frontier]:
                frontier.append([(x, y), current[1] + 1])

def bfPar(env):

    obstList = []
    bfMap = [[0 for col in row] for row in env]
    for yindex, row in enumerate(env):
        for xindex, col in enumerate(row):
            # if col != 254:
            if col == 0:
                obstList.append((xindex, yindex))
                bfMap[yindex][xindex] = 1
            else:
                bfMap[yindex][xindex] = 0

    frontier = [[item, 1] for item in obstList]

    print(len(obstList))
    curFront = frontier
    curLen = 0
    while frontier:
        curFront = frontier
        p = multiprocessing.Pool(processes=8)
        p.starmap(_bfworker, [(current, env, bfMap, frontier) for current in curFront])
        p.join()
        p.close()
        #current = frontier.pop(0)
        curLen = curFront[1][1]
        print(curLen)
        print(len(frontier))



    return bfMap

def wavefront(env, goal):
    print('Performing wavefront...')
    xMax = len(env[0]) - 1
    yMax = len(env) - 1
    wfMap = [[0 for col in row] for row in env]
    for yindex, row in enumerate(env):
        for xindex, col in enumerate(row):
            if col == 0:
                wfMap[yindex][xindex] = -1
            else:
                wfMap[yindex][xindex] = 0

    frontier = [[goal, 1]]

    pyplot.imshow(wfMap, pyplot.cm.gray)
    print('Done converting to image')
    pyplot.show()
    # curLen = 0
    while len(frontier) > 0:
        current = frontier.pop(0)
        # if current[1] > curLen:
        #     curLen = current[1]
        #     print(curLen)
        #     print(len(frontier))

        if current[0][0] > 0:
            x = current[0][0] - 1
            y = current[0][1]
            if env[y][x] == 254 and wfMap[y][x] == 0:
                wfMap[y][x] = current[1] + 1
                if (x, y) not in [x[0] for x in frontier]:
                    frontier.append([(x, y), current[1] + 1])
        if current[0][0] < xMax:
            x = current[0][0] + 1
            y = current[0][1]
            if env[y][x] == 254 and wfMap[y][x] == 0:
                wfMap[y][x] = current[1] + 1
                if (x, y) not in [x[0] for x in frontier]:
                    frontier.append([(x, y), current[1] + 1])
        if current[0][1] > 0:
            x = current[0][0]
            y = current[0][1] - 1
            if env[y][x] == 254 and wfMap[y][x] == 0:
                wfMap[y][x] = current[1] + 1
                if (x, y) not in [x[0] for x in frontier]:
                    frontier.append([(x, y), current[1] + 1])
        if current[0][1] < yMax:
            x = current[0][0]
            y = current[0][1] + 1
            if env[y][x] == 254 and wfMap[y][x] == 0:
                wfMap[y][x] = current[1] + 1
                if (x, y) not in [x[0] for x in frontier]:
                    frontier.append([(x, y), current[1] + 1])
    pyplot.imshow(wfMap, pyplot.cm.gray)
    print('Done converting to image')
    pyplot.show()
    print('Done performing wavefront.')
    return wfMap

def brushfire(env):
    xMax = len(env[0]) - 1
    yMax = len(env) - 1
    obstList = []
    bfMap = [[0 for col in row] for row in env]
    for yindex, row in enumerate(env):
        for xindex, col in enumerate(row):
            #if col != 254:
            if col == 0:
                obstList.append((xindex, yindex))
                bfMap[yindex][xindex] = 1
            else:
                bfMap[yindex][xindex] = 0

    frontier = [[item, 1] for item in obstList]

    print(len(obstList))

    pyplot.imshow(bfMap, pyplot.cm.gray)
    print('Done converting to image')
    pyplot.show()
    curLen = 0
    while len(frontier) > 0:
        current = frontier.pop(0)
        if current[1] > curLen:
            curLen= current[1]
            print(curLen)
            print(len(frontier))

        if current[0][0] > 0:
            x = current[0][0] - 1
            y = current[0][1]
            if env[y][x] == 254 and bfMap[y][x] == 0:
                bfMap[y][x] = current[1] + 1
                if (x, y) not in [x[0] for x in frontier]:
                    frontier.append([(x, y), current[1] + 1])
        if current[0][0] < xMax:
            x = current[0][0] + 1
            y = current[0][1]
            if env[y][x] == 254 and bfMap[y][x] == 0:
                bfMap[y][x] = current[1] + 1
                if (x, y) not in [x[0] for x in frontier]:
                    frontier.append([(x, y), current[1] + 1])
        if current[0][1] > 0:
            x = current[0][0]
            y = current[0][1] - 1
            if env[y][x] == 254 and bfMap[y][x] == 0:
                bfMap[y][x] = current[1] + 1
                if (x, y) not in [x[0] for x in frontier]:
                    frontier.append([(x, y), current[1] + 1])
        if current[0][1] < yMax:
            x = current[0][0]
            y = current[0][1] + 1
            if env[y][x] == 254 and bfMap[y][x] == 0:
                bfMap[y][x] = current[1] + 1
                if (x, y) not in [x[0] for x in frontier]:
                    frontier.append([(x, y), current[1] + 1])
    pyplot.imshow(bfMap, pyplot.cm.gray)
    print('Done converting to image')
    pyplot.show()
    return bfMap

def gradientRep(bf, x, y):
    map = {0:0, 1:90, 2:180, 3: 270}

    neighbors = [99, 99, 99, 99]
    neighbors[0] = bf[y][x + 1]
    neighbors[2] = bf[y][x - 1]
    neighbors[3] = bf[y + 1][x]
    neighbors[1] = bf[y - 1][x]

    maxNeigh = max(neighbors)
    maxIndex = neighbors.index(maxNeigh)
    vec = map[maxIndex]

    return vec

def gradientAtr(bf, x, y):
    map = {0:0, 1:90, 2:180, 3: 270}

    neighbors = [99, 99, 99, 99]
    neighbors[0] = bf[y][x + 1]

    neighbors[2] = bf[y][x - 1]

    neighbors[3] = bf[y + 1][x]

    neighbors[1] = bf[y - 1][x]

    maxNeigh = min(neighbors)
    maxIndex = neighbors.index(maxNeigh)
    vec = map[maxIndex]
    if maxIndex == 0:
        return (x + 1, y)
    elif maxIndex == 1:
        return (x, y - 1)
    elif maxIndex == 2:
        return (x-1, y)
    elif maxIndex == 3:
        return (x, y + 1)

    raise ValueError
    #return vec


def distance(newArr):
    gy = int(input("Enter goal x pos: "))
    gx = int(input("Enter goal y pos: "))
    for x in range(6):
        for y in range(7):
            distance = math.sqrt((x - gx) ** 2 + (y - gy) ** 2)
            newArr[x][y] = round(distance, 2)
    print(newArr)
    grad = gradientAtr(newArr, 6, 5)
    for line in grad:
        print(line)
    with open("attractive_result.txt", "w") as tf:
        for x in range(6):
            for y in range(7):
                tf.write(str(newArr[x][y]) + " ")
            tf.write('\n')
    tf.close()

def read():
    envArr = []
    with open("inputFile.txt") as file:
        for line in file:
            tempArr = []
            for char in line.strip():
                if char != '1' and char != '0':
                    print("Bad input")
                    exit(0)
                tempArr.append(int(char))
            envArr.append(tempArr)
    return envArr


def aStar(occGrid, start, goal):
    closedSet = []
    openSet = [[start]]
    current = []
    #current.append((1,2))
    #current.append(start)
    goalFound = False

    while len(openSet) > 0:
        current = findMin(openSet, start, goal)
        openSet.remove(current)
        if current[-1] == goal:
            return current
        else:
            closedSet.append(current[-1])
            for successor in validNext(current[-1], occGrid):
                if successor not in closedSet:
                    openSet.append(current + [successor])

def manhattan(current, goal):
    return (abs(current[0] - goal[0]) + abs(current[1] - goal[1]))

def findMin(frontier,start, goal):
    minscore = math.inf
    minpath = []
    for path in frontier:
        if manhattan(path[-1], goal) + manhattan(path[-1], start) < minscore:
            minpath = path
            minscore = manhattan(path[-1], goal) + manhattan(path[-1], start) < minscore

    return minpath


def validNext(state, occGrid):
    retList = []
    try:
        if occGrid[state[1] + 1][state[0]] == 254:
            retList.append((state[0], state[1] + 1))
    except:
        pass
    try:
        if occGrid[state[1] - 1][state[0]] == 254 and state[1] - 1 > 0:
            retList.append((state[0], state[1] - 1))
    except:
        pass
    try:
        if occGrid[state[1]][state[0] + 1] == 254:
            retList.append((state[0] + 1, state[1]))
    except:
        pass
    try:
        if occGrid[state[1]][state[0] - 1] == 254 and state[0] - 1 > 0:
            retList.append((state[0] - 1, state[1]))
    except:
        pass
    return retList
