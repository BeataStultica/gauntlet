
from main import GauntletGame
from GauntletAgent import AgentDQN


def start_train():
    agent = AgentDQN({
        "width": 23,
        "height": 15,
        "numTraining": 1000
    })
    for i in range(1000):
        game = GauntletGame()
        result, player = game.test_game(agent)
        print(result)
        agent.registerInitialState()


start_train()
