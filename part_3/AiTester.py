from board import Board
from AI_Guara import AIAgentTester


def runFiller(boardList, depth, moves):
    agent1 = AIAgentTester("b", depth)
    agent2 = AIAgentTester("w", depth)
    for board in boardList:
        print(f"Starting board num {boardList.index(board)}")
        randomFirstMove = AIAgentTester.get_random_move(board, "b")
        secondBoard = Board()
        secondBoard.set_circles(randomFirstMove)
        moveBoard = (None, secondBoard)
        for move in range(moves):
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


if __name__ == '__main__':
    boardList = board_list_creator()
    runFiller(boardList, 7, 80)
