from board import Board
# from AI_Guara import AIAgent
from state_space_gen import StateSpaceGen
import time

import time
# def display_board(board, width, height):
#   """
#   This function displays the abalone board on a pygame window and waits for user input to close.
#
#   Args:
#       board: An instance of the Board class.
#       width: The width of the display window.
#       height: The height of the display window.
#   """
#
#   # Marble radius
#   marble_radius = 20
#
#   # Color constants
#   black_color = (0, 0, 0)
#   white_color = (255, 255, 255)
#   empty_space_color = (181, 154, 126)
#
#   # Initialize pygame
#   pygame.init()
#   screen = pygame.display.set_mode((width, height))
#   pygame.display.set_caption('Abalone Board')
#
#   # Function to convert board coordinates to pixel coordinates
#   def board_to_pixel(coord):
#     row, col = coord
#     max_row = 9  # Maximum row number
#     max_col = 9  # Maximum column number
#     total_board_width = (marble_radius * 2.5) * (max_col - 1) + marble_radius * 2
#     start_x = total_board_width // 2  # Center the board horizontally
#     start_y = 50
#     x_spacing = (row - 1) * (marble_radius * 2.5) // 2
#     x_pixel = start_x + (col - 3) * (marble_radius * 2.5) - x_spacing
#     y_pixel = start_y + (max_row - row + 2) * (marble_radius * math.sqrt(5))
#     return x_pixel, y_pixel
#
#   # Draw the board
#   screen.fill((200, 200, 200))
#   for row, col in board.BOARD_COORD:
#     x_pixel, y_pixel = board_to_pixel((row, col))
#     color = board.get_circle(row, col)
#
#     if color == 'b':
#       color = black_color
#     elif color == 'w':
#       color = white_color
#     else:
#       color = empty_space_color
#
#     pygame.draw.circle(screen, color, (x_pixel, y_pixel), marble_radius)
#
#   # Event loop to keep the window open
#   running = True
#   while running:
#     for event in pygame.event.get():
#       if event.type == pygame.QUIT:
#         running = False
#
#
#       # Update the display
#       pygame.display.flip()
#
#   # Quit pygame
#   pygame.quit()
#
# # Example usage
# board = Board()  # Create a board instance (replace with your initialization)
# display_board(board, 800, 600)

if __name__ == '__main__':
    # board = Board()
    # board.setup_board("German Daisy")
    # generator = StateSpaceGen()
    # generator.generate_state_space(board, "b")
    # moves = generator.get_moves()
    # boards = generator.get_boards()
    # for move in moves:
    #     print(move)
    # for board in boards:
    #     print(board)

    # string_list = [
    #     "C5b", "D5b", "E4b", "E5b", "E6b", "F5b", "F6b", "F7b", "F8b", "G6b", "H6b",
    #     "C3w", "C4w", "D3w", "D4w", "D6w", "E7w", "F4w", "G5w", "G7w", "G8w", "G9w",
    #     "H7w", "H8w", "H9w"
    # ]
    # new_board = Board.create_custom_board(string_list)
    # agent2 = AIAgent()
    # score = agent2.board_evaluation(new_board)
    # print(f"score {score}")
    # print(new_board)
    # new_generator = StateSpaceGen()
    # valid_move1_black = Move("i",direction=Direction.UP_LEFT, marbles=[(8, 6)])
    # valid_move2_black = Move("i", direction=Direction.DOWN_RIGHT, marbles=[(4, 5), (3, 5)])
    # invalid_move1_black = Move("s", direction=Direction.RIGHT, marbles=[(5, 5), (4, 5), (3, 5)])
    # valid_move1_white = Move("s", direction=Direction.UP_LEFT, marbles=[(8, 9), (8, 8), (8, 7)])
    # valid_move2_white = Move("s", direction=Direction.RIGHT, marbles=[(4, 6), (5, 7)])
    # invalid_move1_white = Move("s", direction=Direction.UP_RIGHT, marbles=[(4, 6), (5, 7)])
    # results1 = new_generator.validate_move(new_board, valid_move1_black.get_marbles(), valid_move1_black.get_direction())
    # print(f"{results1[0]} -> {results1[1]}")
    # results2 = new_generator.validate_move(new_board, valid_move2_black.get_marbles(), valid_move2_black.get_direction())
    # print(f"{results2[0]} -> {results2[1]}")
    # results3 = new_generator.validate_move(new_board, invalid_move1_black.get_marbles(), invalid_move1_black.get_direction())
    # print(f"{results3[0]} -> {results3[1]}")
    # results4 = new_generator.validate_move(new_board, valid_move1_white.get_marbles(),
    #                                        valid_move1_white.get_direction())
    # print(f"{results4[0]} -> {results4[1]}")
    # results5 = new_generator.validate_move(new_board, valid_move2_white.get_marbles(),
    #                                        valid_move2_white.get_direction())
    # print(f"{results5[0]} -> {results5[1]}")
    # results6 = new_generator.validate_move(new_board, invalid_move1_white.get_marbles(),
    #                                        invalid_move1_white.get_direction())
    # print(f"{results6[0]} -> {results6[1]}")
    # new_generator.generate_state_space(new_board, "w")
    # new_moves = new_generator.get_moves()
    # new_boards = new_generator.get_boards()
    # for move in new_moves:
    #     print(move)
    #     # print(move.get_marbles())
    #     # print(move.get_direction())
    # for board in new_boards:
    #     print(board)
    #
    # handler = IOHandler()
    # handler.create_outcomes_from_board_file("Test3.input")

    # string_list = [
    #     "C5b", "D5b", "E4b", "E5b", "E6b", "F5b", "F6b", "F7b", "F8b", "G6b", "H6b",
    #     "C3w", "C4w", "D3w", "D4w", "D6w", "E7w", "F4w", "G5w", "G7w", "G8w", "G9w",
    #     "H7w", "H8w", "H9w"
    # ]
    # new_board = Board.create_custom_board(string_list)
    # new_generator = StateSpaceGen()
    # display_board(new_board, 800, 600)  # Call the function with desired dimensions
    # valid_move1_black = Move("i", direction=Direction.UP_LEFT, marbles=[(8, 6)])
    # valid_move2_black = Move("i", direction=Direction.DOWN_RIGHT, marbles=[(4, 5), (3, 5)])
    # invalid_move1_black = Move("s", direction=Direction.RIGHT, marbles=[(5, 5), (4, 5), (3, 5)])
    # valid_move1_white = Move("s", direction=Direction.UP_LEFT, marbles=[(8, 9), (8, 8), (8, 7)])
    # valid_move2_white = Move("s", direction=Direction.RIGHT, marbles=[(4, 6), (5, 7)])
    # invalid_move1_white = Move("s", direction=Direction.UP_RIGHT, marbles=[(4, 6), (5, 7)])
    # sumito_test = Move("i", direction=Direction.UP_RIGHT, marbles=[(4, 5), (5, 6), (6, 7)])
    # print(new_board)
    # results1 = new_generator.validate_move(new_board, valid_move1_black.get_marbles(),
    #                                        valid_move1_black.get_direction())
    # print(results1[0])
    # display_board(results1[1], 800, 600)
    # results2 = new_generator.validate_move(new_board, valid_move2_black.get_marbles(),
    #                                        valid_move2_black.get_direction())
    # print(results2[0])
    # display_board(results2[1], 800, 600)
    # results4 = new_generator.validate_move(new_board, valid_move1_white.get_marbles(),
    #                                        valid_move1_white.get_direction())
    # print(results4[0])
    # display_board(results4[1], 800, 600)
    # results5 = new_generator.validate_move(new_board, valid_move2_white.get_marbles(),
    #                                        valid_move2_white.get_direction())
    # print(results5[0])
    # display_board(results5[1], 800, 600)
    # results6 = new_generator.validate_move(new_board, sumito_test.get_marbles(),
    #                                        sumito_test.get_direction())
    # print(results6[0])
    # display_board(results6[1], 800, 600)

    # input("press any key to continue")
    # print(results1[0])
    # game.board = results1[1]
    # input("press any key to continue")
    # print(results2[0])
    # game.board = results2[1]
    # input("press any key to continue")
    # print(results3[0])
    # game.board = results3[1]
    # input("press any key to continue")
    # print(results4[0])
    # game.board = results4[1]
    # input("press any key to continue")
    # print(results5[0])
    # game.board = results5[1]
    # input("press any key to continue")
    # print(results6[0])
    # game.board = results6[1]
    # input("press any key to continue")

    board = Board()
    board.setup_board()
    # gen = StateSpaceGen()
    # start_time = time.time()
    # gen.generate_state_space(board, "b")
    # final_time = time.time()-start_time
    # print(final_time)

    # gen = StateSpaceGen()
    # gen.generate_state_space(board, "b")
    # agent = AIAgent("Black", "b")
    # print(f"Initial Board: {board}")
    # print(f"Initial hash {board.hash_board()}")
    #
    # for circles in gen.get_boards():
    #     new_board = Board()
    #     new_board.set_circles(circles)
    #     print(f"Board: {new_board}")
    #     hash = new_board.hash_board()
    #     print(f"Hash {hash}")

    # agent = AIAgent("White", "b")
    # agent2 = AIAgent("Black", "w")
    # start = time.process_time()
    # limit = 10000000
    # depth = 4
    # move = agent.get_best_move(board, depth, limit)
    # print(f"{agent.get_color()}:{move[0]}")
    # print(time.process_time() - start)
    # start = time.process_time()
    # move = agent2.get_best_move(move[1], depth, limit)
    # print(f"{agent2.get_color()}:{move[0]}")
    # print(time.process_time() - start)
    # start = time.process_time()
    # player = next_player(player)
    # move = agent.get_best_move(move[1], player, 4, limit)
    # print(f"b:{move[0]}")
    # print(time.process_time() - start)
    # start = time.process_time()
    # player = next_player(player)
    # move = agent2.get_best_move(move[1], player, 4, limit)
    # print(f"w:{move[0]}")
    # print(time.process_time() - start)
    # start = time.process_time()
    # player = next_player(player)
    # move = agent.get_best_move(move[1], player, 4, limit)
    # print(f"b:{move[0]}")
    # print(time.process_time() - start)
    # start = time.process_time()
    # player = next_player(player)
    # move = agent2.get_best_move(move[1], player, 4, limit)
    # print(f"w:{move[0]}")
    # print(time.process_time() - start)
