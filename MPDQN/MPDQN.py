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
                       "Platform.yaml",  # The path of my_mpdqn_config.yaml file should be correct.
                       )
runner.run(mode='train')  # Or runner.benchmark()