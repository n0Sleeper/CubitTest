import os
import configparser as cfg
from ttkbootstrap.dialogs import Messagebox

#fofa接口API存储函数
def fofa_write(email,API):
    config = cfg.ConfigParser()
    config.add_section('fofa')

    config['fofa']['email'] = email
    config['fofa']['key'] = API

    with open('./config/fofa.ini','w') as configFile:
        config.write(configFile)


def fofa_read():
    config = cfg.ConfigParser()
    config.read('./config/fofa.ini')
    email = config['fofa']['email']
    key = config['fofa']['key']
    ls = {'email':email, 'key':key}
    return ls


#shodan接口处理函数
def shodan_write(Key):
    config = cfg.ConfigParser()
    config.add_section('shodan')

    config['shodan']['KEY'] = Key

    with open('./config/shodan.ini','w') as configFile:
        config.write(configFile)

def shodan_read():
    config = cfg.ConfigParser()
    config.read('./config/shodan.ini')
    KEY = config['shodan']["KEY"]

    return KEY


#zoomEye接口处理函数




