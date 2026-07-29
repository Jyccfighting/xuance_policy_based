import xuance as xp
runner = xp.get_runner('sac',
                       'classic_control',  # Choices: claasi_control, box2d, .
                       'Pendulum-v1',  # The name of the environment.
                       "./SAC/SAC_Pendulum-v1.yaml",  # The path of my_config.yaml file should be correct.
                       )
runner.run(mode='benchmark')  # Or runner.benchmark()