# import xuance as xp
from pdqn_agent import PDQN_Agent  # 修改后的PDQN代码文件
from spdqn_agent import SPDQN_Agent
from mpdqn_agent import MPDQN_Agent
from xuance.torch.agents import REGISTRY_Agents

REGISTRY_Agents['PDQN'] = PDQN_Agent  # 修改玄策里的Agent注册表
REGISTRY_Agents['SPDQN'] = SPDQN_Agent
REGISTRY_Agents['MPDQN'] = MPDQN_Agent# 修改玄策里的Agent注册表

import xuance as xp
# import gymnasium as gym
# from xuance.environment.single_agent_env.platform import PlatformEnv  # 导入环境类

# # 手动注册环境
# gym.register(
#     id='Platform-v0',                # 必须与配置文件中的 env_id 一致
#     entry_point=PlatformEnv,         # 直接传入类对象
#     max_episode_steps=200,           # 可选，与配置文件保持一致
# )
runner = xp.get_runner('mpdqn',
                       'Platform',  # Choices: parameterised_action_space
                       'Platform-v0',  # Choices: Platform-v0, Goal-v0, etc.
                       "./MPDQN/MPDQN_Platform.yaml",  # The path of my_mpdqn_config.yaml file should be correct.
                       )
runner.run(mode='benchmark')  # Or runner.benchmark()