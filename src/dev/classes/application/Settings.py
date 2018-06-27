import simplejson
import os
import logging
from sortedcontainers import sorteddict

config_path = './config/config.json'


class Settings(object):

    def __init__(self):
        self.data = sorteddict.SortedDict()
        self.initialize_data()
        self.files_to_update = []
        self.load_config()
        self.check_retro()

    def initialize_data(self):
        if not os.path.isdir('./config'):
            os.mkdir('./config')
            logging.critical("Creating config directory.")
        else:
            logging.info("Config directory exists.")

        if not os.path.exists(config_path):
            self.data['settings'] = {'wow_dir': '', 'prompt_to_close': True}
            self.data['addons'] = {}

            logging.info("Creating config.json file.")
            self.save_config()

    def check_for_wow_directory(self, parent):

        if self.data['settings']['wow_dir'] == '':
            parent.MessageBox.emit("Addons directory not found.",
                                   "Please specify the directory where you want the addons to be downloaded to in "
                                   "the Settings window." 
                                   "\n\nThis is usually: 'World of Warcraft/Interface/AddOns'\n", 'inform')

            return False

        return True

    def check_retro(self):
        if 'settings' not in self.data:
            self.data['settings'] = {}

        if 'wow_dir' not in self.data['settings']:
            self.data['settings']['wow_dir'] = ""
            self.save_config()

        if 'prompt_to_close' not in self.data['settings']:
            self.data['settings']['prompt_to_close'] = True
            self.save_config()

        if 'addons' not in self.data:
            self.data['addons'] = ""
            self.save_config()

    def write_addon_info(self, primary_key, key, info):
        self.data[primary_key][key] = info

    def load_config(self):
        with open(config_path, 'r') as f:
            self.data = simplejson.loads(f.read())

    def save_config(self):
        self.data['addons'] = {k: self.data['addons'][k] for k in sorted(self.data['addons'])}

        with open(config_path, 'w') as f:
            f.write(simplejson.dumps(self.data, indent=4, ensure_ascii=True))

    def get_settings_keys(self):
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
