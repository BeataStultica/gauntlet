import time
import sys
from main import GauntletGame
from GauntletAgent import AgentDQN


def start_train(start_model=None, eps=1, eps_step=1000):
    agent = AgentDQN({
        "width": 23,
        "height": 15,
        "numTraining": 1000,
        "load_file": start_model,
        "eps": eps,
        "eps_step": eps_step
    })
    for i in range(1000):
        game = GauntletGame()
        result, player = game.test_game(agent)
        # Print stats
        log_file = open('./logs/'+str(agent.general_record_time)+'-l-'+str(agent.params['width'])+'-m-'+str(
            agent.params['height'])+'-x-'+str(agent.params['num_training'])+'.log', 'a')
        log_file.write("# %4d | steps: %5d | steps_t: %5d | t: %4f | r: %12f | e: %10f " %
                       (agent.numeps, agent.local_cnt, agent.cnt, time.time()-agent.s, agent.ep_rew, agent.params['eps']))
        log_file.write("| Q: %10f | won: %r \n" %
                       ((max(agent.Q_global, default=float('nan')), result[1])))
        sys.stdout.write("# %4d | steps: %5d | steps_t: %5d | t: %4f | r: %12f | e: %10f " %
                         (agent.numeps, agent.local_cnt, agent.cnt, time.time()-agent.s, agent.ep_rew, agent.params['eps']))
        sys.stdout.write("| Q: %10f | won: %r \n" %
                         ((max(agent.Q_global, default=float('nan')), result[1])))
        sys.stdout.flush()
        agent.registerInitialState()


start_train()
