import simplejson
import os
import logging
from sortedcontainers import sorteddict
import datetime

config_path = './config/'
config_file_name = 'config.json'
addons_file_name = 'addons.json'


class Settings(object):

    def __init__(self):
        self.config = sorteddict.SortedDict()
        self.addons = sorteddict.SortedDict()
        self.initialize_data()
        self.files_to_update = []
        self.load_config()
        self.load_addons()
        self.check_retro()

    def initialize_data(self):
        if not os.path.isdir('./config'):
            os.mkdir('./config')
            logging.critical("Creating config directory.")
        else:
            logging.info("Config directory exists.")

        if not os.path.exists(config_path + config_file_name):
            self.config['settings'] = {'wow_dir': '', 'prompt_to_close': True, "remove_old_archive": True}

            logging.info("Creating config.json file.")
            self.save_config()

        if not os.path.exists(config_path + addons_file_name):
            self.addons['addons'] = {}
            logging.info("Creating addons.json file.")

            self.save_addons()

    def check_for_wow_directory(self, parent):

        if self.config['settings']['wow_dir'] == '':
            parent.MessageBox.emit("Addons directory not found.",
                                   "Please specify the directory where you want the addons to be downloaded to in "
                                   "the Settings window." 
                                   "\n\nThis is usually: 'World of Warcraft/Interface/AddOns'\n", 'inform')

            return False

        return True

    def check_retro(self):
        if 'settings' not in self.config:
            self.config['settings'] = {}

        if 'wow_dir' not in self.config['settings']:
            self.config['settings']['wow_dir'] = ""
            self.save_config()

        if 'prompt_to_close' not in self.config['settings']:
            self.config['settings']['prompt_to_close'] = True
            self.save_config()

        if 'remove_old_archive' not in self.config['settings']:
            self.config['settings']['remove_old_archive'] = True
            self.save_config()

        if 'addons' not in self.addons:
            self.addons['addons'] = ""
            self.save_addons()

        # Check if addon information is in the config.json file.
        if 'addons' in self.config:
            print("Addons in config.")

            self.addons['addons'] = self.config['addons']
            self.config.pop('addons', None)
            self.save_config()
            self.save_addons()

        now = datetime.datetime.now()
        for addon in self.addons['addons']:
            if 'last_update_date' not in self.addons['addons'][addon]:
                self.addons['addons'][addon]['last_update_date'] = "{0}/{1}/{2}".format(now.month, now.day, now.year)
            self.save_addons()

    def write_addon_info(self, key, info):
        self.addons['addons'][key] = info

    def load_config(self):
        with open(config_path + config_file_name, 'r') as f:
            self.config = simplejson.loads(f.read())

    def load_addons(self):
        with open(config_path + addons_file_name, 'r') as f:
            self.addons = simplejson.loads(f.read())

    def save_config(self):
        with open(config_path + config_file_name, 'w') as f:
            f.write(simplejson.dumps(self.config, indent=4, ensure_ascii=True))

    def save_addons(self):
        self.addons['addons'] = {k: self.addons['addons'][k] for k in sorted(self.addons['addons'])}

        with open(config_path + addons_file_name, 'w') as f:
            f.write(simplejson.dumps(self.addons, indent=4, ensure_ascii=True))

    def get_settings_keys(self):
        for key in self.addons['addons']:
            print(key)


if __name__ == '__main__':
    s = Settings()
    # s.get_settings_keys()
    # s.write_addon_info('test', {'url': 'd', 'ver': '4'})
    # s.write_addon_info('test1', {'url': 'd', 'ver': '4'})
    # s.save_config()
    s.load_config()

    s.get_settings_keys()
