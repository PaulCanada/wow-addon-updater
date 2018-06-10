import os
import requests
import logging

logging.basicConfig(level=logging.DEBUG)
test_url_a = "https://wow.curseforge.com/projects/details/files/latest"
test_url_b = "https://www.curseforge.com/wow/addons/file"


class Downloader(object):
    """
    This class attempts to download an updated version of the zip archive of the addon requested.

    Different websites handle storage differently. E.g.
        Curse Project: Find 'data-name=' to get index of page contents where version starts.
        Curse Addon: Find 'file__name full' to get index of page contents where version starts.

    """

    def __init__(self, wow_dir=""):
        self.install_dir = wow_dir
        self.zip_dir = './zips'
        self.url = ''

    def check_zip_dir(self):
        if not os.path.isdir(self.zip_dir):
            os.mkdir(self.zip_dir)

    def download_from_url(self, url):
        logging.info("Attemtping to download file: {0}".format(url))
        url_grab_response = requests.get(url, stream=True)
        local_path = url.split('/')[-1]

        with open(self.zip_dir + '/' + local_path + '.zip', 'wb') as file:
            for chunk in url_grab_response.iter_content(chunk_size=1024):
                file.write(chunk)


if __name__ == '__main__':

    d = Downloader()
    d.check_zip_dir()
    d.download_from_url(test_url_a)
