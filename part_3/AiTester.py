from board import Board
from AI_Guara import AIAgentTester
from IO_handler import IOHandler
import json


def runFiller(boardList, depth, turns):
    agent1 = AIAgentTester("b", depth)
    agent2 = AIAgentTester("w", depth)
    for board in boardList:
        print(f"Starting board num {boardList.index(board)}")
        randomFirstMove = AIAgentTester.get_random_move(board, "b")
        secondBoard = Board()
        secondBoard.set_circles(randomFirstMove)
        moveBoard = (None, secondBoard)
        for move in range(turns):
            moveBoard = agent2.get_best_move(moveBoard[1])
            moveBoard = agent1.get_best_move(moveBoard[1])


def board_list_creator():
    boardList = []
    default_board = Board()
    default_board.setup_board()
    boardList.append(default_board)
    belgium_board = Board()
    belgium_board.setup_board("Belgian Daisy")
    boardList.append(belgium_board)
    german_board = Board()
    german_board.setup_board("German Daisy")
    boardList.append(german_board)
    string_list = [
        "C5b", "D5b", "E4b", "E5b", "E6b", "F5b", "F6b", "F7b", "F8b", "G6b", "H6b",
        "C3w", "C4w", "D3w", "D4w", "D6w", "E7w", "F4w", "G5w", "G7w", "G8w", "G9w",
        "H7w", "H8w", "H9w"
    ]
    boardA = Board.create_custom_board(string_list)
    boardList.append(boardA)
    xmas_star = [
        "A3b", "B3b", "B4b", "C5b", "E3b", "F3b", "F4b", "F7b", "F8b", "G3b", "G4b", "G7b", "G8b", "G9b",
        "C1w", "C2w", "C3w", "C6w", "C7w", "D2w", "D3w", "D6w", "D7w", "E7w", "G5w", "H6w", "H7w", "I7w"
    ]
    xmas_star_board = Board.create_custom_board(xmas_star)
    boardList.append(xmas_star_board)
    domination_daisy = [
        "B1b", "C1b", "C2b", "D1b", "D2b", "D3b", "E4b", "E6b", "F7b", "F8b", "F9b", "G8b", "G9b", "H9b",
        "B5w", "B6w", "C5w", "C6w", "C7w", "D6w", "D7w", "F3w", "F4w", "G3w", "G4w", "G5w", "H4w", "H5w"
    ]
    domination_daisy_board = Board.create_custom_board(domination_daisy)
    boardList.append(domination_daisy_board)
    crown = [
        "A3b", "B1b", "B3b", "B4b", "B6b", "C2b", "C3b", "C5b", "C6b", "D3b", "D4b", "D5b", "D6b", "G6b",
        "C4w", "F4w", "F5w", "F6w", "F7w", "G4w", "G5w", "G7w", "G8w", "H4w", "H6w", "H7w", "H9w", "I7w"
    ]
    crown_board = Board.create_custom_board(crown)
    boardList.append(crown_board)
    pyramid = [
        "A1b", "A2b", "A3b", "A4b", "A5b", "B2b", "B3b", "B4b", "B5b", "C3b", "C4b", "C5b", "D4b", "D5b",
        "F5w", "F6w", "G5w", "G6w", "G7w", "H5w", "H6w", "H7w", "H8w", "I5w", "I6w", "I7w", "I8w", "I9w"
    ]
    pyramid_board = Board.create_custom_board(pyramid)
    boardList.append(pyramid_board)

    return boardList

def read_table_from_file(file):
    try:
        with open(file, 'r') as file:
            transposition_table = json.load(file)
            transposition_table = {int(key): value for key, value in transposition_table.items()}
            print(f"Transposition table for player loaded successfully.")
            return transposition_table
    except FileNotFoundError:
        print(f"No transposition table found for player .")
        return None

def save_table(transposition_table_data, file):
    table_name = file
    with open(table_name, 'w') as file:
        json.dump(transposition_table_data, file, indent=None)
        print(f"Transposition table saved successfully.")

if __name__ == '__main__':
    # boardList = board_list_creator()
    # new_board = Board()
    # new_board.setup_board("Belgian Daisy")
    # boardList = []
    # new_board2 = Board()
    # new_board2.setup_board("Belgian Daisy")
    # new_board3 = Board()
    # new_board3.setup_board("Belgian Daisy")
    # boardList.append(new_board)
    # boardList.append(new_board2)
    # boardList.append(new_board3)
    # for _ in range(2):
    #     runFiller(boardList, 5, 80)

    tomek_file_b = "TranspositionTableb.json"
    mangat_file_b = "TranspositionTableb1.json"
    vitor_file_b = "TranspositionTableb2.json"
    third_file_b = "TranspositionTableb3.json"
    tomek_b_table = read_table_from_file(tomek_file_b)
    mangat_b_table = read_table_from_file(mangat_file_b)
    vitor_b_table = read_table_from_file(vitor_file_b)
    third_file_b = read_table_from_file(third_file_b)
    tomek_b_table.update(mangat_b_table)
    tomek_b_table.update(vitor_b_table)
    tomek_b_table.update(third_file_b)
    output = "TranspositionTableb.json"
    save_table(tomek_b_table, output)


