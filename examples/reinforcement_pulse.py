"""
脈波間隔拡張・強化学習・パルス波
"""

import pickle
import traceback
from time import sleep

from hbfb import Agent
from hbfb.params_operators import Reinforcement

agent = Agent()
params = [100, 0.5]
params_info = [[1, 254], [1, 99]]
params_operator = Reinforcement(params, params_info)
params_operator.reset(agent.goal_ibi, agent.ibi)
sync = False
true_count = 0
false_count = 0
first_ibi = agent.ibi

# データ収集
reward_list = []
reward_count = 0
best_ibi = 0

for _ in range(50):
    try:
        done = False
        params = params_operator.action()
        agent.action(params)

        print(params)
        print(agent)
        print("↓")

        success = False
        while not success:
            sleep(5)
            success = agent.observe()

        sync = agent.sync_check()
        print("sync:", sync)
        print(agent)
        print()

        if sync:
            reward = agent.ibi / (first_ibi+100)
            true_count += 1
            false_count = 0
            if best_ibi < agent.ibi:
                best_ibi = agent.ibi
                best_params = params
        else:
            reward = 0
            false_count += 1
        
        if false_count >= 7: #エピソード終了
            done = True
            false_count = 0
            agent.reset()
            if true_count <= 3 and agent.ibi < (first_ibi+100): 
                reward = 2.0 - agent.ibi/first_ibi           
                true_count = 0

        # データ収集
        reward_count += reward
        if done:
            reward_list.append(reward_count)
            reward_count = 0

        params_operator.observe(agent.ibi, agent.goal_ibi, done, reward)

        sleep(5)

    except Exception as e:
        print(traceback.format_exc())

agent.stop()
print(best_params)
print(best_ibi)

with open('pulse_reward.pickle', 'wb') as f:
    pickle.dump(reward_list, f)