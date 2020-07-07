class Config(object):
    DEBUG = True
    TESTING = False
    IN_FILES = False


class StoreInFilesConfig(Config):
    IN_FILES = True
