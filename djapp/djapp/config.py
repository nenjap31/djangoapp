import configparser
import os


class Config:

    def GetConfig():
        env = os.environ.get('DJANGOAPP_ENV', 'development')
        cfg = configparser.ConfigParser()
        path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
        if env == 'production':
            cfg.read(os.path.join(path, 'cfg/config.cfg'))
        elif env == 'testing':
            cfg.read(os.path.join(path, 'cfg/testing.cfg'))
        elif env == 'staging':
            cfg.read(os.path.join(path, 'cfg/staging.cfg'))
        elif env == 'development':
            cfg.read(os.path.join(path, 'cfg/dev.cfg'))
        return cfg
