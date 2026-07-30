from drl_analyzer.config_cleaner import ConfigCleaner


def main():


    wandb_config = {

        "_wandb":{
            "value":{
                "cli":"0.28"
            }
        },

        "agent":{
            "value":"A2C"
        },

        "gamma":{
            "value":0.98
        },

        "seed":{
            "value":1
        }

    }


    result = ConfigCleaner.clean(
        wandb_config
    )


    print(result)



if __name__ == "__main__":
    main()