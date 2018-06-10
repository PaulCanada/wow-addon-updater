import simplejson
import os
import sys
import logging

logging.basicConfig(level=logging.DEBUG)
config_path = './config/addons.json'


class Settings(object):

    def __init__(self):
        self.data = {}
        self.initialize_data()
        self.files_to_update = []
        self.load_config()

    def initialize_data(self):
        if not os.path.isdir('./config'):
            os.mkdir('./config')
            logging.critical("Creating config directory.")
        else:
            logging.info("Config directory exists.")

        if not os.path.exists(config_path):
            self.data['addons'] = {}

            logging.info("Creating config.json file.")
            with(open(config_path, 'w')) as f:
                f.write(simplejson.dumps(self.data, indent=4, ensure_ascii=True))

    def write_addon_info(self, key, info):
        # self.data.get('addons').append({key: info})
        self.data['addons'][key] = info

    def load_config(self):
        with open(config_path, 'r') as f:
            self.data = simplejson.loads(f.read())

    def save_config(self):
        with open(config_path, 'w') as f:
            f.write(simplejson.dumps(self.data, indent=4, ensure_ascii=True))

    def get_settings_keys(self):

        if 'raiderio' in self.data['addons']:
            print("DdddFGD")

        for key in self.data['addons']:
            print(key)


if __name__ == '__main__':
    s = Settings()
    # s.get_settings_keys()
    # s.write_addon_info('test', {'url': 'd', 'ver': '4'})
    # s.write_addon_info('test1', {'url': 'd', 'ver': '4'})
    # s.save_config()
    s.load_config()

    s.get_settings_keys()
