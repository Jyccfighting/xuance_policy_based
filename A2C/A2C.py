import xuance as xp
runner = xp.get_runner('A2C',
                       'classic_control',  # Choices: claasi_control, box2d, .
                       'Acrobot-v1',  
                       "./A2C/A2C_Acrobot-v1.yaml",  # The path of my_config.yaml file should be correct.
                       )
runner.run(mode='benchmark') 