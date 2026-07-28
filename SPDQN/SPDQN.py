import xuance as xp
runner = xp.get_runner('spdqn',
                       'Platform',  # Choices: parameterised_action_space
                       'Platform-v0',  # Choices: Platform-v0, Goal-v0, etc.
                       "Platform.yaml",  # The path of my_config.yaml file should be correct.
                       )
runner.run(mode='benchmark')  # Or runner.benchmark()