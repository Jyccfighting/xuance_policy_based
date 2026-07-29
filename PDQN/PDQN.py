import xuance
from pdqn_agent import PDQN  # 修改后的PDQN代码文件
from xuance.torch.agents import REGISTRY_Agents

REGISTRY_Agents['PDQN'] = PDQN 
runner = xuance.get_runner('PDQN',
                       'Platform',  # Choices: claasi_control, box2d, .
                       'Platform-v0',  # Choices: Platform-v0, Goal-v0, etc.
                       "./PDQN/PDQN_Platform.yaml",  # The path of my_config.yaml file should be correct.
                       )
runner.run(mode='benchmark')  # Or runner.benchmark()