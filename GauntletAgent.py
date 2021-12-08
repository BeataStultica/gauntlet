import numpy as np
import random
#import util
import time
import sys


# Replay memory
from collections import deque

# Neural nets
import tensorflow as tf
from DQN import *

params = {
    # Model backups
    'load_file': None,
    'save_file': 'dqn_model',
    'save_interval': 1000,

    # Training parameters
    'train_start': 50,    # Episodes before training starts
    'batch_size': 32,       # Replay memory batch size
    'mem_size': 100000,     # Replay memory size

    'discount': 0.95,       # Discount rate (gamma value)
    'lr': .0002,            # Learning reate
    # 'rms_decay': 0.99,      # RMS Prop decay (switched to adam)
    # 'rms_eps': 1e-6,        # RMS Prop epsilon (switched to adam)

    # Epsilon value (epsilon-greedy)
    'eps': 1.0,             # Epsilon start value
    'eps_final': 0.1,       # Epsilon end value
    'eps_step': 100       # Epsilon steps between start and end (linear)
}


class AgentDQN():
    def __init__(self, args):

        print("Initialise DQN Agent")

        # Load parameters from user-given arguments
        self.params = params
        self.params['width'] = args['width']
        self.params['height'] = args['height']
        self.params['num_training'] = args['numTraining']
        self.params['load_file'] = args['load_file']
        self.params['eps'] = args['eps']
        self.params['eps_step'] = args['eps_step']

        # Start Tensorflow session
        gpu_options = tf.compat.v1.GPUOptions(
            per_process_gpu_memory_fraction=0.1)
        self.sess = tf.compat.v1.Session(
            config=tf.compat.v1.ConfigProto(gpu_options=gpu_options))
        self.qnet = DQN(self.params)

        # time started
        self.general_record_time = time.strftime(
            "%a_%d_%b_%Y_%H_%M_%S", time.localtime())
        # Q and cost
        self.Q_global = []
        self.cost_disp = 0
        self.r = False
        # Stats
        self.cnt = self.qnet.sess.run(self.qnet.global_step)
        self.local_cnt = 0
        self.maps = None
        self.player = None

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
        self.last_player_hp = 999

    def getMove(self, state, person):
        if np.random.rand() > self.params['eps'] and state is not None:
            self.Q_pred = self.qnet.sess.run(
                self.qnet.y,
                feed_dict={self.qnet.x: np.reshape(state,
                                                   (1, self.params['width'], self.params['height'], 1)),
                           self.qnet.q_t: np.zeros(1),
                           self.qnet.actions: np.zeros((1, 4)),
                           self.qnet.terminals: np.zeros(1),
                           self.qnet.rewards: np.zeros(1)})[0]

            self.Q_global.append(max(self.Q_pred))
            a_winner = np.argwhere(self.Q_pred == np.amax(self.Q_pred))
            self.r = True

            if len(a_winner) > 1:
                move = a_winner[np.random.randint(0, len(a_winner))][0]

            else:
                move = a_winner[0][0]
        else:
            self.r = False
            awailable_move = []
            x = int(person.rect.centerx/40)
            y = int(person.rect.centery/40)
            if state is not None:
                if state[y-1][x] != 1:
                    awailable_move.append(2)
                if state[y+1][x] != 1:
                    awailable_move.append(3)
                if state[y][x-1] != 1:
                    awailable_move.append(0)
                if state[y][x+1] != 1:
                    awailable_move.append(1)
            else:
                awailable_move = [0, 1, 2, 3]
            move = np.random.choice(awailable_move)

        self.last_action = move
        ac = {0: "left", 1: "right", 2: "top", 3: "bottom"}
        if self.r:
            print("Q :" + str(max(self.Q_pred)) +
                  " | action: "+ac[self.last_action] + " | eps: " + str(self.params['eps']))
        else:
            print("Q : None | action: " +
                  ac[self.last_action] + " | eps: " + str(self.params['eps']))
        return self.last_action

    def observation_step(self, curr_state, curr_score, curr_dist, curr_player_hp):
        if self.last_action is not None and self.current_state is not None:
            # Process current experience state
            self.last_state = np.copy(self.current_state)
            self.current_state = np.copy(curr_state)
            # if curr_state == self.last_state:
            #    print('+')
            # else:
            #    print('-')
            self.last_dist = self.curr_dist
            self.curr_dist = curr_dist
            # Process current experience reward
            self.current_score = curr_score
            reward = self.current_score - self.last_score + \
                (self.last_dist - self.curr_dist)*400 - \
                (self.last_player_hp - curr_player_hp)*5
            self.last_score = self.current_score
            self.last_player_hp = curr_player_hp
            # print('dist')
            # print(self.last_dist)
            # print(self.curr_dist)
            if reward > 300:
                self.last_reward = 8000.
            elif reward > 0:
                self.last_reward = 200.
            elif reward < -300:
                self.last_reward = -8000.
                self.won = False
            else:
                self.last_reward = -30000.
            if(self.terminal and self.won):
                self.last_reward = 100000.
            self.ep_rew += self.last_reward
            '''
            for j in range(len(self.last_state)):
                if 12 in self.last_state[j]:
                    for k in range(len(self.last_state[j])):
                        if self.last_state[j][k] == 12:
                            x_p = k
                    y_p = j
                
            # print(x_p)
            # print(y_p)
            flag = True

            if self.current_state[y_p][x_p+1] == 12:
                # print('+x')
                # print(self.current_state[y_p][x_p+1])
                move = 1
            elif self.current_state[y_p][x_p-1] == 12:
                # print('-x')
                # print(self.current_state[y_p][x_p-1])
                move = 0
            elif self.current_state[y_p-1][x_p] == 12:
                # print('-y')
                # print(self.current_state[y_p-1][x_p])
                move = 2
            elif self.current_state[y_p+1][x_p] == 12:
                # print('+y')
                # print(self.current_state[y_p+1][x_p])
                move = 3
            else:
                move = self.last_action
            '''
            # Store last experience into memory

            experience = (self.last_state, float(self.last_reward),
                          self.last_action, self.current_state, self.terminal)
            # print('start')
            # print('--------')
            # for i in self.last_state:
            #    print(list(i))
            # print('+++++++')
            # for j in self.current_state:
            #    print(list(j))
            # print(self.last_action)
            # print(move)
            # print(self.last_reward)
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
        # print('++++lcnt')
        # print(self.local_cnt)
        self.frame += 1
        self.params['eps'] = max(self.params['eps_final'],
                                 1.00 - float(self.cnt) / float(self.params['eps_step']))

    def observationFunction(self, curr_state, curr_score, curr_dist, player_hp):
        # Do observation
        self.terminal = False
        self.observation_step(curr_state, curr_score, curr_dist, player_hp)

    def final(self, curr_state, curr_score, curr_dist, player_hp):
        # Next
        self.ep_rew += self.last_reward

        # Do observation
        self.terminal = True
        self.observation_step(curr_state, curr_score, curr_dist, player_hp)

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
            batch_s = np.reshape(
                batch_s[0], (1, self.params['width'], self.params['height'], 1))
            batch_r = np.array(batch_r)
            batch_a = self.get_onehot(np.array(batch_a))
            batch_n = np.reshape(
                batch_n[0], (1, self.params['width'], self.params['height'], 1))
            batch_t = np.array(batch_t)

            self.cnt, self.cost_disp = self.qnet.train(
                batch_s, batch_a, batch_t, batch_n, batch_r)

    def get_onehot(self, actions):
        """ Create list of vectors with 1 values at index of action in list """
        actions_onehot = np.zeros((self.params['batch_size'], 4))
        for i in range(len(actions)):
            actions_onehot[i][int(actions[i])] = 1
        return actions_onehot

    def registerInitialState(self):  # inspects the starting state

        # Reset reward
        self.last_score = 0
        self.current_score = 0
        self.last_reward = 0.
        self.ep_rew = 0
        self.s = time.time()
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
        self.cnt = self.qnet.sess.run(self.qnet.global_step)
        self.last_dist = 0
        self.curr_dist = 0
        self.current_score = 0
        self.terminal = False
        self.local_cnt = 0
        # Next
        self.frame = 0
        self.numeps += 1
