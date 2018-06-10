import os
import requests
import logging
from Addon import Addon

logging.basicConfig(level=logging.DEBUG)
test_url_a = "https://wow.curseforge.com/projects/deadly-boss-mods"
test_url_b = "https://www.curseforge.com/wow/addons/file"
test_url_c = "https://www.tukui.org/download.php?ui=elvui"


class Downloader(object):
    """
    This class attempts to download an updated version of the zip archive of the addon requested.

    Different websites handle storage differently. E.g.
        Curse Project: Find 'data-name=' to get index of page contents where version starts.
        Curse Addon: Find 'file__name full' to get index of page contents where version starts.

    """

    def __init__(self, settings, wow_dir=""):
        self.install_dir = wow_dir
        self.settings = settings
        self.zip_dir = './zips'
        self.url = ''

    def check_zip_dir(self):
        if not os.path.isdir(self.zip_dir):
            os.mkdir(self.zip_dir)

    def check_for_updates(self):
        update_list = []
        for key in self.settings.data['addons']:
            current_addon = Addon(url=self.settings.data['addons'][key]['url'],
                                  current_version=self.settings.data['addons'][key]['current_version'])

            print("Current ver: {0}".format(current_addon.current_version))
            print("Latest ver: {0}".format(current_addon.latest_version))
            print("Name: {0}".format(current_addon.name))

            if current_addon.current_version != current_addon.latest_version:
                logging.info("{0} is out of date!".format(self.settings.data['addons'][key]['name']))
                update_list.append(current_addon)

                self.settings.data['addons'][key]['latest_version'] = current_addon.latest_version
                self.settings.save_config()
                self.settings.load_config()

            else:
                logging.info("{0} is up to date.".format(self.settings.data['addons'][key]['name']))

        self.settings.files_to_update = update_list

    def update_files(self):
        for addon in self.settings.files_to_update:
            print(addon.name)

    def download_from_url(self, addon):
        logging.info("Attemtping to download file: {0}".format(addon.url))

        if addon.addon_source.__contains__('curse'):
            url_grab_response = requests.get(addon.url + '/files/latest', stream=True)
        else:
            logging.critical("Only mods found from Curse forge are supported at this time.")
            return

        logging.debug("URL Reponse: {0}".format(url_grab_response))
        local_path = addon.name + '_' + addon.latest_version
        logging.debug("Local path: {0}".format(local_path))

        with open(self.zip_dir + '/' + local_path + '.zip', 'wb') as file:
            for chunk in url_grab_response.iter_content(chunk_size=1024):
                file.write(chunk)


if __name__ == '__main__':
    from Settings import Settings

    s = Settings()
    s.load_config()
    a = Addon(url=test_url_c)

    d = Downloader(s)
    d.check_for_updates()
    # d.update_files()
    # d.check_zip_dir()
    d.download_from_url(a)
