import yaml


class Configuration:
    __configuration = None

    @classmethod
    def load_from_file(cls):
        if not cls.__configuration:
            with open('configuration/configuration.yaml') as file:
                configuration = yaml.safe_load(file)
            cls.__configuration = configuration[configuration['active']]
        return cls.__configuration
