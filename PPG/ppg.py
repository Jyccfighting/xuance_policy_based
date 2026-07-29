import xuance as xp
runner = xp.get_runner('ppg',
                       'classic_control',  # Choices: claasi_control, box2d, atari.
                       'Acrobot-v1',  # Choices: CartPole-v1, Acrobot-v1, Pendulum-v1, MountainCar-v0, etc.
                       "./PPG/PPG_Acrobot-v1.yaml", 
                       )# The path of my_config.yaml file should be correct.)
runner.run(mode='benchmark')  # Or runner.benchmark()