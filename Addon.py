import requests
import logging


logging.basicConfig(level=logging.DEBUG)


class Addon(object):

    curse_project_index = 'data-name='
    curse_addon_index = 'file__name full'

    def __init__(self, url='', name='', current_version='', latest_version=''):
        self.url = url
        self.name = name
        self.current_version = current_version
        self.latest_version = latest_version

    def get_version_index(self, addon_path):
        return{
            'curse-projects': self.curse_project_index,
            'curse-addons': self.curse_addon_index
        }.get(addon_path)

    def get_update_version(self):
        page = requests.get(self.url + '/files')
        page.raise_for_status()

        content = str(page.content)
        logging.debug("Content of page: {0}".format(content))

        index_of_version = content.find('data-name=')
        print(index_of_version)

        print(self.get_version_index(self.get_website_type()))

    def get_name(self):
        url = self.url
        if url.find('/files'):
            logging.info("URL name contains '/files'")
            url = url[:-6]
            logging.info("New url: {0}".format(url))

        name = url[url.rfind('/') + 1:]
        logging.info(name)
        return name

    def get_website_type(self):
        if 'wow.curseforge.com/projects' in self.url:
            return 'curse-projects'
        elif 'www.curseforge.com/wow/addons' in self.url:
            return 'curse-addons'
        elif 'mods.curse.com/addons/wow' in self.url:
            return ''
        elif 'wowinterface' in self.url:
            return ''
        elif 'git.tikui' in self.url:
            return ''
        else:
            logging.critical("Could not determine website type.")
            return None


if __name__ == '__main__':
    a = Addon(url="https://wow.curseforge.com/projects/deadly-boss-mods/files")
    a.get_name()
    # print(a.get_website_type())
    # soup = BeautifulSoup(requests.get("https://wow.curseforge.com/projects/deadly-boss-mods").content)
    # print(soup)


