import xuance as xp
runner = xp.get_runner('sac',
                       'classic_control',  # Choices: claasi_control, box2d, .
                       'MountainCar-v0',  # The name of the environment.
                       "./SAC/SAC_MountainCar-v0.yaml",  # The path of my_config.yaml file should be correct.
                       )
runner.run(mode='benchmark')  # Or runner.benchmark()