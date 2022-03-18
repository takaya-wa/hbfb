import pickle
import traceback
from time import sleep

from hbfb import Agent
from hbfb.params_operators import Reinforcement

agent = Agent(data_interface="ver4")
params = [20, 200, 20]
params_info = [[1, 254], [1, 254], [1, 254]]
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

for _ in range(80):
    try:
        done = False
        params = params_operator.action()
        agent.action(params)

        print(params)
        print(agent)
        goal_ibi = agent.goal_ibi
        ibi = agent.ibi
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
        
        if false_count >= 7: #7回の試行で同期出来なかったら
            done = True
            agent.reset()
            if true_count <= 3 and agent.ibi < (first_ibi+100):
                reward = -1

        # データ収集
        reward_count += reward
        if done:
            reward_list.append(reward_count)
            reward_count = 0

        #報酬
        params_operator.observe(agent.ibi, agent.goal_ibi, done, reward)

        sleep(5)

    except Exception as e:
        print(traceback.format_exc())

agent.stop()
print(best_params)
print(best_ibi)

with open('arbitary_reward.pickle', 'wb') as f:
    pickle.dump(reward_list, f)