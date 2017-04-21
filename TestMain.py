import PathFinding
import re
import numpy

def read_pgm(filename, byteorder='>'):
    """Return image data from a raw PGM file as numpy array.

    Format specification: http://netpbm.sourceforge.net/doc/pgm.html

    """
    with open(filename, 'rb') as f:
        buffer = f.read()
    try:
        header, width, height, maxval = re.search(
            b"(^P5\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n])*"
            b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
    except AttributeError:
        raise ValueError("Not a raw PGM file: '%s'" % filename)
    return numpy.frombuffer(buffer,
                            dtype='u1' if int(maxval) < 256 else byteorder+'u2',
                            count=int(width)*int(height),
                            offset=len(header)
                            ).reshape((int(height), int(width)))


def convertToMap(fileName):
    map = [[]]
    image = read_pgm(fileName, byteorder='<')
    for y, line in enumerate(image):
        map.append([])
        for x, item in enumerate(line):
            if item == 255:
                map[y].append(True)
            elif item == 205:
                map[y].append(False)
            else:
                map[y].append(None)
    return map

def convertToImg(map):
    image = [[]]
    for y, line in enumerate(image):
        image.append([])
        for x, item in enumerate(line):
            if item == True:
                image[y].append(255)
            elif item == False:
                image[y].append(205)
            else:
                image[y].append(0)

if __name__ == '__main__':

    map2 = [[254, 254, 254, 254],
            [254, 0, 0, 254],
            [254, 254, 0, 254],
            [0, 254, 254, 254]]

    from matplotlib import pyplot
    print('Converting to map')
    #map = convertToMap('thirdFloorMap.pgm')
    print('Done converting to map')

    map = read_pgm('minimap.pgm', byteorder='<')
    print('Converting to image')
    pyplot.imshow(map, pyplot.cm.gray)
    print('Done converting to image')
    pyplot.show()
    colors = []
    for row in map:
        for item in row:
            if item not in colors:
                colors.append(item)
    print(colors)
    coordStart = (962, 621)
    coordGoal = (1133, 561)

    coordFlipStart = (621, 962)
    coordFlipGoal = (561, 1133)

#    print(map[coordStart[1]][coordStart[0]])
#    print(map[coordGoal[1]][coordGoal[0]])

    print(PathFinding.gradientDescent(map, (3,2), (7,6)))
    #print(PathFinding.gradientDescent(map, (1000,525), (3200,2100)))
    #print(PathFinding.gradientDescent(map, coordStart, coordGoal))

    #print(PathFinding.gradientDescent(map2, coordStart, coordGoal))





# if __name__ == '__main__':
#     with open('thirdFloorMap.pgm') as mapImg:
#         for line in mapImg.readlines():
#             print(line)