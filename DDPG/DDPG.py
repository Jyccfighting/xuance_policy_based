import xuance as xp
runner = xp.get_runner('ddpg',
                       'classic_control',  # Choices: claasi_control, box2d, .
                       'Pendulum-v1',  
                       "Pendulum-v1.yaml",  # The path of my_config.yaml file should be correct.
                       )
runner.run(mode='benchmark') 