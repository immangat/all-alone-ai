import board
from AI_Guara import AIAgentTester
import random
from state_space_gen import StateSpaceGen

def simulate_game(board_list, range):
    ai_agent1 = AIAgentTester("b")
    ai_agent2 = AIAgentTester("w")

    for board in board_list:
        gen = StateSpaceGen()
        move = random.choice(gen.get_boards())
        for turn in range(80):
            move = ai_agent2.get_best_move(move[1])
            move = ai_agent1.get_best_move(move[1])
        print(f"Initial board: {board}")
        print(f"final board: {move[1]}")


if __name__ == "__main__":
    pass