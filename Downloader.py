import os
import sys
import requests
import shutil
import logging

logging.basicConfig(level=logging.DEBUG)
test_url_a = "https://wow.curseforge.com/projects/details/files/latest"
test_url_b = "https://www.curseforge.com/wow/addons/file"



class Downloader:
    """
    This class attempts to download an updated version of the zip archive of the addon requested.

    Different websites handle storage differently. E.g.
        Curse Project: Find 'data-name=' to get index of page contents where version starts.
        Curse Addon: Find 'file__name full' to get index of page contents where version starts.

    """

    curse_project_index = 'data-name='
    curse_addon_index = 'file__name full'

    def __init__(self, wow_dir=""):
        self.install_dir = wow_dir
        self.zip_dir = './zips'
        self.version_index = 0
        self.url = ''

    def get_version_index(self, addon_path):
        return{
            'curse-projects': self.curse_project_index,
            'curse-addons': self.curse_addon_index
        }.get(addon_path)

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


def get_version(url):
    page = requests.get(url + '/files')
    page.raise_for_status()

    content = str(page.content)
    logging.debug("Content of page: {0}".format(content))

    index_of_version = content.find('data-name=')
    print(index_of_version)


def get_website_type(url):
    if 'wow.curseforge.com/projects' in url:
        return 'curse-projects'
    elif 'www.curseforge.com/wow/addons' in url:
        return 'curse-addons'
    elif 'mods.curse.com/addons/wow' in url:
        return ''
    elif 'wowinterface' in url:
        return ''
    elif 'git.tikui' in url:
        return ''
    else:
        return None


if __name__ == '__main__':

    # get_version(test_url)

    d = Downloader()
    print(d.get_version_index(get_website_type(test_url_b)))
    # d.check_zip_dir()
    # d.download_from_url(test_url)
