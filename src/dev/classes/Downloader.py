import os
import requests
import logging
from src.dev.classes.Addon import Addon
import zipfile

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

    def __init__(self, parent):
        self.parent = parent
        self.zip_dir = './downloaded_archives'
        self.check_zip_dir()

    def check_zip_dir(self):
        if not os.path.isdir(self.zip_dir):
            os.mkdir(self.zip_dir)

    def update_addon(self, addon):
        self.parent.OutputUpdater.emit("Downloading files for {0} to {1}".format(addon.name.title(),
                                                                                 os.path.abspath(self.zip_dir)))
        response, file_dir = self.download_from_url(addon)

        if file_dir == '':
            self.parent.OutputUpdater.emit("Download failed: bad URL.")
            return False

        file_dir = os.path.abspath(file_dir)
        logging.info("Item: {0}".format(addon.url))
        logging.debug("File to extract: {0}".format(file_dir))

        if response:
            self.parent.OutputUpdater.emit("Download complete.")
        else:
            self.parent.OutputUpdater.emit("Download failed.")
            return False

        # Unzip the recently downloaded file
        self.parent.OutputUpdater.emit("Extracting files to {0}".format(file_dir))
        try:
            zipper = zipfile.ZipFile(file_dir, 'r')
            zipper.extractall(self.parent.settings.data['settings']['wow_dir'] + '/')
            zipper.close()
            self.parent.OutputUpdater.emit("Extraction complete.")

            # Set the addon's current version to the latest.
            for key in self.parent.settings.data['addons']:
                logging.debug("Key: {0}".format(str(key)))
                logging.debug("Item name: {0}".format(addon.name))
                logging.debug("Transformed name: {0}".format(addon.name.title().replace("-", " ").replace("_", " ")))
                logging.debug("Transformed key: {0}".format(key.title().replace("-", " ").replace("_", " ")))

                if str(key) == addon.name:
                    logging.debug("Addon found for key!")
                    logging.debug("Item's latest version: {0}".format(addon.latest_version))
                    self.parent.settings.data['addons'][key]['current_version'] = addon.latest_version
                    logging.debug("New current version: {0}".format(
                        self.parent.settings.data['addons'][key]['current_version']))

                    self.parent.settings.save_config()
                    self.parent.settings.load_config()

        except Exception as ze:
            logging.critical("Error unzipping addon: {0}".format(ze))
            self.parent.OutputUpdater.emit("Error unzipping addon: {0}".format(ze))

        self.parent.UpdateTreeView.emit()

    def download_from_url(self, addon):
        logging.info("Attemtping to download file: {0}".format(addon.url))
        logging.info("Addon source: {0}".format(addon.addon_source))

        try:
            if addon.addon_source.__contains__('curse-project'):
                if addon.url.endswith("/files"):
                    logging.debug("Attempting to download a file that ends in '/files'.")

                url_grab_response = requests.get(addon.url.replace("/files", "") + '/files/latest', stream=True)
                # TODO: Fix downloading from curse-addons
            elif addon.addon_source.__contains__('curse-addons'):
                url = addon.url
                identifier = '"download__link" href="'

                if not url.endswith('/download'):
                    url += '/download'
                    logging.debug("URL to download: {0}".format(url))

                url_grab_response = requests.get(url).content

                start_ind = str(url_grab_response.decode("utf-8")).find(identifier) + len(identifier)
                logging.debug("Start index: {0}".format(start_ind))

                end_ind = str(url_grab_response.decode("utf-8")).find('"', start_ind)
                logging.debug("End index: {0}".format(end_ind))
                uri = str(url_grab_response.decode("utf-8"))[start_ind:end_ind]

                url = 'https://www.curseforge.com' + uri
                url_grab_response = requests.get(url)

            elif addon.addon_source.__contains__('tukui'):
                uri = '/downloads/' + addon.latest_version + '.zip'
                url = addon.url[:addon.url.find("/download")] + uri
                logging.debug("Tukui url: {0}".format(url))
                url_grab_response = requests.get(url)

            else:
                logging.critical("Only mods found from Curse forge and Tukui are supported at this time.")
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
