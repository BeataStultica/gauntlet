import numpy as np
import random
#import util
import time
import sys

# Pacman game
#from pacman import Directions
#from game import Agent
#import game

# Replay memory
from collections import deque

# Neural nets
import tensorflow as tf
from DQN import *

params = {
    # Model backups
    'load_file': None,
    'save_file': None,
    'save_interval': 20,

    # Training parameters
    'train_start': 500,    # Episodes before training starts
    'batch_size': 32,       # Replay memory batch size
    'mem_size': 100000,     # Replay memory size

    'discount': 0.95,       # Discount rate (gamma value)
    'lr': .0002,            # Learning reate
    # 'rms_decay': 0.99,      # RMS Prop decay (switched to adam)
    # 'rms_eps': 1e-6,        # RMS Prop epsilon (switched to adam)

    # Epsilon value (epsilon-greedy)
    'eps': 1.0,             # Epsilon start value
    'eps_final': 0.1,       # Epsilon end value
    'eps_step': 10000       # Epsilon steps between start and end (linear)
}


class PacmanDQN():
    def __init__(self, args):

        print("Initialise DQN Agent")

        # Load parameters from user-given arguments
        self.params = params
        self.params['width'] = args['width']
        self.params['height'] = args['height']
        self.params['num_training'] = args['numTraining']

        # Start Tensorflow session
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.1)
        self.sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
        self.qnet = DQN(self.params)

        # time started
        self.general_record_time = time.strftime(
            "%a_%d_%b_%Y_%H_%M_%S", time.localtime())
        # Q and cost
        self.Q_global = []
        self.cost_disp = 0

        # Stats
        self.cnt = self.qnet.sess.run(self.qnet.global_step)
        self.local_cnt = 0

        self.numeps = 0
        self.last_score = 0
        self.s = time.time()
        self.last_reward = 0.

        self.replay_mem = deque()
        self.last_scores = deque()
        self.last_dist = 0
        self.curr_dist = 0
        self.current_score = 0
        self.last_action = None
        self.last_state = None
        self.won = True
        self.ep_rew = 0
        self.terminal = False
        self.frame = 0
        self.current_state = None

    def getMove(self):
        # Exploit / Explore
        if np.random.rand() > self.params['eps']:
            # Exploit action
            self.Q_pred = self.qnet.sess.run(
                self.qnet.y,
                feed_dict={self.qnet.x: np.reshape(self.current_state,
                                                   (1, self.params['width'], self.params['height'], 6)),
                           self.qnet.q_t: np.zeros(1),
                           self.qnet.actions: np.zeros((1, 4)),
                           self.qnet.terminals: np.zeros(1),
                           self.qnet.rewards: np.zeros(1)})[0]

            self.Q_global.append(max(self.Q_pred))
            a_winner = np.argwhere(self.Q_pred == np.amax(self.Q_pred))

            if len(a_winner) > 1:
                move = a_winner[np.random.randint(0, len(a_winner))][0]
            else:
                move = a_winner[0][0]
        else:
            # Random:
            move = np.random.randint(0, 4)

        # Save last_action
        self.last_action = self.get_value(move)

        return move

    def observation_step(self, curr_state, curr_score, curr_dist):
        if self.last_action is not None:
            # Process current experience state
            self.last_state = np.copy(self.current_state)
            self.current_state = curr_state
            self.last_dist = self.curr_dist
            self.curr_dist = curr_dist
            # Process current experience reward
            self.current_score = curr_score
            reward = self.current_score - self.last_score + \
                (self.last_dist - self.curr_dist)*400
            self.last_score = self.current_score

            if reward > 400:
                self.last_reward = 800.    # Eat ghost   (Yum! Yum!)
            elif reward > 0:
                self.last_reward = 200.    # Eat food    (Yum!)
            elif reward < -300:
                self.last_reward = -1000.  # Get eaten   (Ouch!) -500
                self.won = False
            elif reward < 0:
                self.last_reward = -1.    # Punish time (Pff..)

            if(self.terminal and self.won):
                self.last_reward = 10000.
            self.ep_rew += self.last_reward

            # Store last experience into memory
            experience = (self.last_state, float(self.last_reward),
                          self.last_action, self.current_state, self.terminal)
            self.replay_mem.append(experience)
            if len(self.replay_mem) > self.params['mem_size']:
                self.replay_mem.popleft()

            # Save model
            if(params['save_file']):
                if self.local_cnt > self.params['train_start'] and self.local_cnt % self.params['save_interval'] == 0:
                    self.qnet.save_ckpt(
                        'saves/model-' + params['save_file'] + "_" + str(self.cnt) + '_' + str(self.numeps))
                    print('Model saved')

            # Train
            self.train()

        # Next
        self.local_cnt += 1
        self.frame += 1
        self.params['eps'] = max(self.params['eps_final'],
                                 1.00 - float(self.cnt) / float(self.params['eps_step']))

    def observationFunction(self, curr_state, curr_score, curr_dist):
        # Do observation
        self.terminal = False
        self.observation_step(curr_state, curr_score, curr_dist)

    def final(self, curr_state, curr_score, curr_dist):
        # Next
        self.ep_rew += self.last_reward

        # Do observation
        self.terminal = True
        self.observation_step(curr_state, curr_score, curr_dist)

        # Print stats
        log_file = open('./logs/'+str(self.general_record_time)+'-l-'+str(self.params['width'])+'-m-'+str(
            self.params['height'])+'-x-'+str(self.params['num_training'])+'.log', 'a')
        log_file.write("# %4d | steps: %5d | steps_t: %5d | t: %4f | r: %12f | e: %10f " %
                       (self.numeps, self.local_cnt, self.cnt, time.time()-self.s, self.ep_rew, self.params['eps']))
        log_file.write("| Q: %10f | won: %r \n" %
                       ((max(self.Q_global, default=float('nan')), self.won)))
        sys.stdout.write("# %4d | steps: %5d | steps_t: %5d | t: %4f | r: %12f | e: %10f " %
                         (self.numeps, self.local_cnt, self.cnt, time.time()-self.s, self.ep_rew, self.params['eps']))
        sys.stdout.write("| Q: %10f | won: %r \n" %
                         ((max(self.Q_global, default=float('nan')), self.won)))
        sys.stdout.flush()

    def train(self):
        # Train
        if (self.local_cnt > self.params['train_start']):
            batch = random.sample(self.replay_mem, self.params['batch_size'])
            batch_s = []  # States (s)
            batch_r = []  # Rewards (r)
            batch_a = []  # Actions (a)
            batch_n = []  # Next states (s')
            batch_t = []  # Terminal state (t)

            for i in batch:
                batch_s.append(i[0])
                batch_r.append(i[1])
                batch_a.append(i[2])
                batch_n.append(i[3])
                batch_t.append(i[4])
            batch_s = np.array(batch_s)
            batch_r = np.array(batch_r)
            batch_a = self.get_onehot(np.array(batch_a))
            batch_n = np.array(batch_n)
            batch_t = np.array(batch_t)

            self.cnt, self.cost_disp = self.qnet.train(
                batch_s, batch_a, batch_t, batch_n, batch_r)

    def get_onehot(self, actions):
        """ Create list of vectors with 1 values at index of action in list """
        actions_onehot = np.zeros((self.params['batch_size'], 4))
        for i in range(len(actions)):
            actions_onehot[i][int(actions[i])] = 1
        return actions_onehot

    def registerInitialState(self, state):  # inspects the starting state

        # Reset reward
        self.last_score = 0
        self.current_score = 0
        self.last_reward = 0.
        self.ep_rew = 0

        # Reset state
        self.last_state = None
        self.current_state = None

        # Reset actions
        self.last_action = None

        # Reset vars
        self.terminal = None
        self.won = True
        self.Q_global = []
        self.delay = 0

        self.last_dist = 0
        self.curr_dist = 0
        self.current_score = 0
        self.terminal = False
        # Next
        self.frame = 0
        self.numeps += 1
