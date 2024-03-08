import configparser
config = configparser.ConfigParser()
config.read('config.ini')
ENGINE = config['connectdb']['ENGINE']
NAME = config['connectdb']['NAME']
USER = config['connectdb']['USER']
PASSWORD = config['connectdb']['PASSWORD']
HOST = config['connectdb']['HOST']
PORT = config['connectdb']['PORT']


