from helper.data import *
import random
import collections
from queue import Queue


class Bot(object):
    # Code here
    def get_next_action(self, game_info):
        '''
        last = game_info.host_player.last_move
        print(last)
        if last == 4:
            last = Direction.RIGHT

        if last == 1:
            return Direction.DOWN
        elif last == 2:
            return Direction.LEFT
        elif last == 3:
            return Direction.UP
        elif last == 0:
            return Direction.RIGHT
'''

        mapObject = game_info.map
        hostObject = game_info.host_player

        map = mapObject.tiles
        hostPosition = hostObject.position

        lastMove = hostObject.last_move
        possiblePositions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        if lastMove == Direction.UP:
            possiblePositions = [(1, 0), (0, 1), (-1, 0)]
        elif lastMove == Direction.RIGHT:
            possiblePositions = [(0, 1), (0, -1), (-1, 0)]
        elif lastMove == Direction.DOWN:
            possiblePositions = [(0, -1), (1, 0), (-1, 0)]
        elif lastMove == Direction.LEFT:
            possiblePositions = [(0, 1), (1, 0), (0, -1)]

        teamNum = hostObject.team_number


        # Si movement left is less than 3, then on path find vers le plus proche body
        if hostObject.movement_left < 5:
            endPos = outPath(game_info, teamNum)
            nx = endPos[1]
            ny = endPos[0]

            path = findPath(map, (hostPosition.x, hostPosition.y), teamNum, endPos, game_info)

            if len(path) == 1:
                newPath = endPos
            else:
                newPath = path[1]

            nextMove = (newPath[0] - hostPosition.x, newPath[1] - hostPosition.y)
        else:
            pos = []

            for newPosition in possiblePositions:
                nodePosition = (hostPosition.x + newPosition[0], hostPosition.y + newPosition[1])
                #print(nodePosition)
                if nodePosition[0] > 15 or nodePosition[0] < 0 or nodePosition[1] > 15 or nodePosition[1] < 0:  # Wall
                    #print("Outside of wall")
                    continue

                if map[nodePosition[0]][nodePosition[1]].team_tail is not None:  # Tail, expend to be able to enter enemy tail
                    #print("tail in front")
                    continue

                # if remaining steps < half: do path finding to come back

                # if remaining steps > half: continue same direction

                pos.append(newPosition)

            #print(pos)
            rand = random.randint(0, len(pos) - 1)

            nextMove = pos[rand]

        print("Next move == "+str(nextMove))
        if nextMove == (1,0):
            return Direction.RIGHT
        elif nextMove == (0,-1):
            return Direction.UP
        elif nextMove == (-1,0):
            return Direction.LEFT
        elif nextMove == (0,1):
            return Direction.DOWN

        #return Direction.RIGHT


def findPath(map, start, teamNum, end, game_info):
    start_node = Node(None, start)
    end_node = Node(None, end)
    open_set = []
    closed_set = []

    # Add start node in open set
    open_set.append(start_node)

    while len(open_set) > 0:

        current_node = open_set[0]
        current_index = 0

        # Get current node
        for index, item in enumerate(open_set):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_set.pop(current_index)
        closed_set.append(current_node)

        nx = current_node.position[0]
        ny = current_node.position[1]
        if current_node == end_node:
        #if map[nx][ny].team_owner == teamNum and map[nx][ny].team_tail is None and map[nx][ny].team_head is None:  # end condition
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            newPath = path[::-1]  # Return reversed path
            return newPath

        # Generate children
        children = []

        lastMove = game_info.host_player.last_move
        possiblePositions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        if lastMove == Direction.UP:
            possiblePositions = [(1, 0), (0, 1), (-1, 0)]
        elif lastMove == Direction.RIGHT:
            possiblePositions = [(0, 1), (0, -1), (-1, 0)]
        elif lastMove == Direction.DOWN:
            possiblePositions = [(0, -1), (1, 0), (-1, 0)]
        elif lastMove == Direction.LEFT:
            possiblePositions = [(0, 1), (1, 0), (0, -1)]

        for new_position in possiblePositions:

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            newNode = Node(current_node, node_position)



            if newNode == end_node or map[node_position[1]][node_position[0]].team_owner == teamNum:
                # if map[nx][ny].team_owner == teamNum and map[nx][ny].team_tail is None and map[nx][ny].team_head is None:  # end condition
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                newPath = path[::-1]  # Return reversed path
                print(newPath)
                return newPath

            # Verify that node is not outside maze
            if node_position[0] > 15 or node_position[0] < 0 or node_position[1] > 15 or node_position[1] < 0:
                continue

            # Verify that node is walkable terrain
            if map[node_position[1]][node_position[0]].team_tail is not None or map[node_position[1]][node_position[0]].team_head is not None:
                continue

            # Crete new node
            new_node = Node(current_node, node_position)

            children.append(new_node)

        for child in children:

            for closed_child in closed_set:
                if child == closed_child:
                    continue

            # Create f, g, h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_set:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_set.append(child)


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def outPath(game_info, team):
    frontier = Queue()
    x = game_info.host_player.position.x
    y = game_info.host_player.position.y
    frontier.put((x,y))
    came_from = {}
    came_from[(x,y)] = None

    while not frontier.empty():
        current = frontier.get()
        tile = game_info.map.tiles[current[1]][current[0]].team_owner
        if tile == team:
            print("Current: " + str(current))
            return current

        for next in getPossiblePositionsOutside(game_info, current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current


#Seb
def getPossiblePositionsOutside(game_info, current):
    #print("inside possible")
    possiblePositions = []
    host = game_info.host_player
    lastMove = host.last_move
    possibleMoves = [(1, 0), (0, -1), (-1, 0), (0,1)]
    if lastMove == Direction.UP:
       possibleMoves = [(1, 0), (0, -1), (-1, 0)]
    elif lastMove == Direction.RIGHT:
       possibleMoves = [(0, 1), (0, -1), (-1, 0)]
    elif lastMove == Direction.DOWN:
       possibleMoves = [(0, 1), (1, 0), (-1, 0)]
    elif lastMove == Direction.LEFT:
       possibleMoves = [(0, 1), (1, 0), (0, -1)]

    for moves in possibleMoves:
        tilePosition = (current[0] + moves[0], current[1] + moves[1])

        if tilePosition[0] > 15 or tilePosition[0] < 0 or tilePosition[1] > 15 or tilePosition[1] < 0:
            continue
        elif game_info.map.tiles[tilePosition[1]][tilePosition[0]].team_tail is not None or game_info.map.tiles[tilePosition[1]][tilePosition[0]].team_head is not None:
            continue

        possiblePositions.append(tilePosition)
    return possiblePositions


'''


def square(game_info):
    last = game_info.host_player.last_move
    print(last)
    if last == 4:
        last = 1

    if last == 1:
        return 2
    elif last == 2:
        return 3
    elif last == 3:
        return 0
    elif last == 0:
        return 1
'''
