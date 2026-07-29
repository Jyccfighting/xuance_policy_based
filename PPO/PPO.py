import xuance
runner = xuance.get_runner('ppo',
                           'classic_control',  # 可选项：classic_control、box2d、atari 等。
                           'Acrobot-v1',  # 可选项：CartPole-v1、Acrobot-v1 等。
                           "./PPO/PPO_Acrobot-v1.yaml",  # 请确保 my_config.yaml 文件的路径正确。
                          )
runner.run(mode='benchmark')  # 也可以使用 runner.benchmark()