"""
脈波間隔拡張・単純探索法・パルス波
"""

import traceback
from time import sleep

from hbfb import Agent
from hbfb.params_operators import SimpleSearch

agent = Agent(data_interface="ver3_2")
params = {"vol":100, "pulse_rate":0.5}
params_info = {"vol":[1, 254], "pulse_rate":[0.01, 0.99]}
diff = {"vol":10, "pulse_rate":0.1}
params_operator = SimpleSearch(params, params_info, diff)
sync = False

for _ in range(50):
    try:
        params_operator.observe(sync)
        params = params_operator.action()
        print(params)
        agent.action(params)

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

        sleep(5)

    except Exception as e:
        print(traceback.format_exc())
        
agent.stop()
print(params_operator.params)
print(agent.ibi)