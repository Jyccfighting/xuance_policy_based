import xuance as xp
runner = xp.get_runner('PG',
                       'classic_control',  # Choices: claasi_control, box2d, .
                       'CartPole-v1',  # Choices: acrobot, cartpole, mountaincar, pendulum, .
                       "CartPole-v1.yaml",  # The path of my_config.yaml file should be correct.
                       )
runner.run(mode="train") 