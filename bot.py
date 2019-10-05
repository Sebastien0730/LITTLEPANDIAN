from helper.data import *

class Bot(object):
    # Code here
    def get_next_action(self, game_info):

        findValidPosition(game_info)

        return Direction.RIGHT



def findValidPositions(self, game_info):

    mapObject = game_info.map
    hostObject = game_info.host_player

    map = mapObject.tiles
    hostPosition = hostObject.position

    print(hostPosition.x)
    lastMove = hostObject.last_move

    if lastMove == Direction.UP:
        possiblePositions = [(1, 0), (0, -1), (-1, 0)]
    elif lastMove == Direction.RIGHT:
        possiblePositions = [(0, 1), (0, -1), (-1, 0)]
    elif lastMove == Direction.DOWN:
        possiblePositions = [(0, 1), (1, 0), (-1, 0)]
    elif lastMove == Direction.LEFT:
        possiblePositions = [(0, 1), (1, 0), (0, -1)]

    for newPosition in possiblePositions:

        nodePosition = (
        hostPosition.x + newPosition[0], hostPosition.y + newPosition[1])

        if nodePosition[0] > 15 or nodePosition[0] < 0 or nodePosition[
            1] > 15 or nodePosition[1] < 15:  # Wall
            continue

        if map[nodePosition[0]][nodePosition[
            1]].team_tail is not None:  # Tail, expend to be able to enter enemy tail
            continue

        if map[nodePosition[0]][nodePosition[1]]

    tail = mapObject.get_tail_length(1)