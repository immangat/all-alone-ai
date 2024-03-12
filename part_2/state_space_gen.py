from board import Board
from directions import Direction
from move import Move
import copy

class StateSpaceGen:
    def __init__(self):
        self.board = None
        self.curr_player = None
        self.moves =[]
        self.boards =[]

    def get_boards(self):
        return self.boards

    def get_moves(self):
        return self.moves

    def clear_states(self):
        self.__init__()

    def generate_state_space(self, board, player_color):
        self.board = board
        self.curr_player = player_color

        curr_marbles = self.board.get_marbles_by_color(self.curr_player)

        self.check_single_marble(curr_marbles)

    def check_single_marble(self, curr_marbles):

        for marble in curr_marbles:
            for direction in Direction:
                next_marble_logic = self.get_direction_logic(direction)
                neighbor = (marble[0] + next_marble_logic[0], marble[1] + next_marble_logic[1])
                if neighbor in Board.BOARD_COORD:
                    if self.board.get_marble(neighbor) == self.curr_player:
                        two_marbles = [marble, neighbor]
                        self.check_mult_marbles(two_marbles, direction)
                    elif self.board.get_marble(neighbor) == None:
                        new_move = Move("i", direction, [marble])
                        new_board = copy.deepcopy(self.board)
                        new_board.set_marble(neighbor, self.curr_player)
                        new_board.set_marble(marble, None)
                        self.moves.append(new_move)
                        self.boards.append(new_board)


    def check_mult_marbles(self, coords, direction):

        #check inline movement
        inline_logic = self.get_direction_logic(direction)
        next_in_line = (coords[-1][0] + inline_logic[0], coords[-1][1] + inline_logic[1])
        if next_in_line in Board.BOARD_COORD:
            if self.board.get_marble(next_in_line) == self.curr_player:
                if len(coords) < 3:
                    three_marbles = coords +[next_in_line]
                    self.check_mult_marbles(three_marbles, direction)
            elif self.board.get_marble(next_in_line) == None:
                new_move = Move("i", direction, coords)
                new_board = copy.deepcopy(self.board)
                new_board.set_marble(next_in_line, self.curr_player)
                new_board.set_marble(coords[0], None)
                self.moves.append(new_move)
                self.boards.append(new_board)
            else:
                self.check_sumito(coords, direction)

        #now check side movement
        opposite_inline = self.get_inline_opposite(direction)
        possible_side = [posDir for posDir in Direction if posDir != direction and posDir != opposite_inline]
        duplicate_check = True if coords[-1][1] < coords[0][1] or coords[-1][0] < coords[0][0] else False
        if not duplicate_check:
            for posDir in possible_side:
                direction_logic = self.get_direction_logic(posDir)
                blocked = False
                for coord in coords:
                    next_in_side = (coord[0] + direction_logic[0], coord[1] + direction_logic[1])
                    if next_in_side not in Board.BOARD_COORD or self.board.get_marble(next_in_side) != None:
                        blocked = True
                        break
                if not blocked:
                    new_board = copy.deepcopy(self.board)
                    for coord in coords:
                        next_in_side = (coord[0] + direction_logic[0], coord[1] + direction_logic[1])
                        new_board.set_marble(next_in_side, self.curr_player)
                        new_board.set_marble(coord, None)
                    new_move = Move("s", posDir, coords)
                    self.moves.append(new_move)
                    self.boards.append(new_board)


    def check_sumito (self, coords, direction):
        inline_logic = self.get_direction_logic(direction)
        next_coord = (coords[-1][0] + inline_logic[0], coords[-1][1] + inline_logic[1])
        opponent_marbles = 1
        pushable = True
        while next_coord in Board.BOARD_COORD and self.board.get_marble(next_coord) != None:
            next_coord_marble = self.board.get_marble(next_coord)
            if next_coord_marble == self.curr_player or opponent_marbles > 2 or len(coords) <= opponent_marbles:
                pushable = False
                break
            next_coord = (next_coord[0] + inline_logic[0], next_coord[1] + inline_logic[1])
            opponent_marbles +=1
        if pushable:
            new_move = Move("i", direction, coords)
            opponent_color = self.board.get_marble((coords[-1][0] + inline_logic[0], coords[-1][1] + inline_logic[1]))
            new_board = copy.deepcopy(self.board)
            if next_coord in Board.BOARD_COORD:
                new_board.set_marble(next_coord, opponent_color)
            new_board.set_marble((coords[-1][0] + inline_logic[0], coords[-1][1] + inline_logic[1]), self.curr_player)
            new_board.set_marble(coords[0], None)
            self.moves.append(new_move)
            self.boards.append(new_board)

    def get_inline_opposite(self, direction):
        opposite_map = {
            Direction.UP_LEFT: Direction.DOWN_RIGHT,
            Direction.DOWN_RIGHT: Direction.UP_LEFT,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
            Direction.UP_RIGHT: Direction.DOWN_LEFT,
            Direction.DOWN_LEFT: Direction.UP_RIGHT
        }
        return opposite_map.get(direction, None)

    def get_direction_logic(self, direction):
        if direction == Direction.UP_RIGHT:
            return (1, 1)
        elif direction == Direction.RIGHT:
            return (0, 1)
        elif direction == Direction.DOWN_RIGHT:
            return (-1, 0)
        elif direction == Direction.DOWN_LEFT:
            return (-1, -1)
        elif direction == Direction.LEFT:
            return (0, -1)
        else:
            return (1, 0)

    def get_neighbors(self, coord):
        neighbors = []
        neighbors_directions = [direction for direction in Direction]
        x= coord[0]
        y = coord[1]
        temp =[(x +1, y+1), (x, y+1), (x-1, y), (x-1, y-1), (x, y-1), (x + 1, y)]
        for neighbor in temp:
            if neighbor in Board.BOARD_COORD:
                neighbors.append(neighbor)
            else:
                del neighbors_directions[temp.index(neighbor)]
        return (neighbors, neighbors_directions)
