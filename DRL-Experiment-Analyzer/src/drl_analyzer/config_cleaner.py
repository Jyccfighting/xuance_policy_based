"""
config_cleaner.py

Clean WandB config format.
"""

from typing import Any


class ConfigCleaner:


    @staticmethod
    def clean(
        config: dict
    ) -> dict:
        """
        Convert wandb config into normal dict.
        """

        cleaned = {}


        for key, value in config.items():


            # remove wandb internal data

            if key.startswith("_"):
                continue



            cleaned[key] = (
                ConfigCleaner._unwrap(
                    value
                )
            )


        return cleaned



    @staticmethod
    def _unwrap(
        value: Any
    ):
        """
        Remove {"value": xxx}
        """

        if isinstance(value, dict):

            if "value" in value:

                return value["value"]


            return {
                k:
                ConfigCleaner._unwrap(v)

                for k, v in value.items()
            }


        return value