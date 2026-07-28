import xuance
runner = xuance.get_runner('PDQN',
                       'Platform',  # Choices: claasi_control, box2d, .
                       'Platform-v0',  # Choices: Platform-v0, Goal-v0, etc.
                       "Platform.yaml",  # The path of my_config.yaml file should be correct.
                       )
runner.run()  # Or runner.benchmark()