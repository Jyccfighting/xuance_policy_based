import xuance as xp
runner = xp.get_runner('sac',
                       'classic_control',  # Choices: claasi_control, box2d, .
                       'CartPole-v1',  # The name of the environment.
                       "CartPole-v1.yaml",  # The path of my_config.yaml file should be correct.
                       )
runner.run(mode="train")  # Or runner.benchmark()