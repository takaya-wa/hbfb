import random

import pfrl
from pfrl import q_functions
import torch
import torch.nn
import numpy as np
import gym

from hbfb.params_operator import ParamsOperator
from hbfb.utils import clip, params_info_to_min_max_list

class Reinforcement(ParamsOperator):
    def __init__(self, params, params_info, n_layers=3, n_channels=10):
        super().__init__(params, params_info)
        
        min, max = params_info_to_min_max_list(params_info)
        action_space = gym.spaces.Box(low=np.array(min), high=np.array(max), shape=(len(params),))
        q_func = q_functions.FCQuadraticStateQFunction(
            len(params) + 2,
            len(params),
            n_channels,
            n_layers,
            action_space
        )
        ou_sigma = (action_space.high - action_space.low) * 0.2
        explorer = pfrl.explorers.AdditiveOU(sigma=ou_sigma)

        self.agent = pfrl.agents.DQN(
            q_func,
            optimizer=torch.optim.Adam(q_func.parameters(), eps=1e-2),
            replay_buffer=pfrl.replay_buffers.ReplayBuffer(capacity=10 ** 6),
            gpu=-1,
            gamma=0.9,
            explorer=explorer,
            replay_start_size=500,
            target_update_interval=100,
            update_interval=1,
            minibatch_size=32,
            target_update_method="hard",
            soft_update_tau=1e-2,
        )

    def random_action_func(self): # パラメータの無作為決定
        return [random.uniform(info[0], info[1]) for info in self.params_info]
        
    def action(self, normalize=True):
        """
        func => params正規化の関数
        """
        self.params = self.agent.act(self.obs)
        self.params = clip(self.params, self.params_info)
        params = self.params.copy()
        if normalize:
            for i, info in enumerate(self.params_info):
                self.params[i] /= info[1]
        return params

    def observe(self, goal_ibi, ibi, done, reward):
        self.reset(goal_ibi, ibi)
        self.agent.observe(self.obs, reward, done, False)

    def reset(self, goal_ibi, ibi):
        self.obs = np.asarray([goal_ibi/1200, ibi/1200, *self.params], dtype=np.float32) # ibiを1200で割り正規化。