import requests
import requests.exceptions
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

        self.valid_url = self.check_for_valid_url()

        if self.valid_url:
            self.name = self.get_name()
            self.latest_version = self.get_update_version()

    def get_version_index(self, addon_path):
        return{
            'curse-projects': self.curse_project_index,
            'curse-addons': self.curse_addon_index
        }.get(addon_path, None)

    def get_update_version(self):
        try:
            page = requests.get(self.url + '/files')
        except requests.exceptions.ConnectionError as ce:
            logging.critical(ce)
            return None

        type = self.get_version_index(self.get_website_type())
        logging.info("Type: {0}".format(type))

        content = str(page.content)
        logging.debug("Content of page: {0}".format(content))

        start_ind = content.rfind(type)

        end_ind = content.find(">", start_ind)
        version = content[start_ind + len(type):end_ind].strip("\"")

        logging.info("Version: {0}".format(version))

        return version

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

    def check_for_valid_url(self):
        urls_to_check = ["wow.curseforge.com/projects", "www.curseforge.com/wow/addons"]
        return any(ext in self.url for ext in urls_to_check)


if __name__ == '__main__':
    a = Addon(url="https://wow.curseforge.com/projects/deadly-boss-mods/files")
    # a = Addon(url="http://www.google.com")
    if not a.valid_url:
        a.get_name()
        a.get_update_version()


