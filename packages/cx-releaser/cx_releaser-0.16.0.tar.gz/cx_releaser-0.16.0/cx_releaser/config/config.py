import yaml


class Config:
    def __init__(self, path):
        with open(path, "r") as stream:
            try:
                self.config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def get_by(self, value, by='account_id'):
        if by == 'account_id':
            for conf_name, conf in self.config['aws_envs'].items():
                if conf[by] == value:
                    return conf
            raise ValueError(f'Unknown value {value} for {by}')
        else:
            NotImplemented(f"Only {by} supported")

    def traverse_envs(self):
        for conf_name, conf in self.config['aws_envs'].items():
            yield conf
