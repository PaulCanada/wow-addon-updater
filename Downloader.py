import os
import requests
import logging
from Addon import Addon

logging.basicConfig(level=logging.INFO)
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

    def update_files(self):
        for addon in self.settings.files_to_update:
            print(addon.name)

    def download_from_url(self, addon):
        logging.info("Attemtping to download file: {0}".format(addon.url))

        try:
            if addon.addon_source.__contains__('curse'):
                url_grab_response = requests.get(addon.url + '/files/latest', stream=True)
            else:
                logging.critical("Only mods found from Curse forge are supported at this time.")
                return False

            logging.debug("URL Reponse: {0}".format(url_grab_response))
            local_path = addon.name + '_' + addon.latest_version
            logging.debug("Local path: {0}".format(local_path))

            download_dir = self.zip_dir + '/' + local_path + '.zip'

            with open(download_dir, 'wb') as file:
                for chunk in url_grab_response.iter_content(chunk_size=1024):
                    file.write(chunk)

            return True, download_dir
        except Exception as e:
            logging.critical("Error downloading file: {0}".format(e))
            return False, ''


if __name__ == '__main__':
    from Settings import Settings
    from UpdateChecker import UpdateChecker

    s = Settings()
    s.load_config()
    a = Addon(url=test_url_c)
    updater = UpdateChecker(s)

    d = Downloader(s)
    # d.check_for_updates()
    # d.update_files()
    # d.check_zip_dir()
    d.download_from_url(a)
