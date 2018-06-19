import requests
import requests.exceptions
import logging


logging.basicConfig(level=logging.DEBUG)


class Addon(object):

    curse_project_locator = 'data-name='
    curse_addon_locator = 'file__name full">'
    tukui_locator = 'downloads/'

    def __init__(self, url='', name='', current_version='', latest_version=''):
        self.url = url
        self.name = name
        self.current_version = current_version
        self.latest_version = latest_version
        self.addon_source = ''

        self.valid_url = self.check_for_valid_url()

        if self.valid_url:
            self.name = self.get_name()

            if self.name is False:
                self.valid_url = False

            if self.latest_version == "":
                self.latest_version = self.get_update_version()

                if self.latest_version is None:
                    self.valid_url = False

    def get_version_index(self, addon_path):
        return{
            'curse-projects': self.curse_project_locator,
            'curse-addons': self.curse_addon_locator,
            'tukui': self.tukui_locator
        }.get(addon_path, None)

    def get_update_version(self):

        web_type = self.get_version_index(self.get_website_type())
        logging.debug("Web type: {0}".format(web_type))
        self.addon_source = self.get_website_type()

        if web_type is None:
            return False
        elif web_type == self.tukui_locator:
            uri = ''
        else:
            uri = '/files'

        try:
            page = requests.get(self.url + uri)
        except requests.exceptions.ConnectionError as ce:
            logging.critical(ce)
            return False

        logging.info("Type: {0}".format(web_type))

        content = str(page.content)
        logging.debug("Content of page: {0}".format(content))
        start_ind = content.find(web_type)

        if web_type == self.tukui_locator:
            end_ind = content.find(".zip", start_ind + len(web_type))
            version = content[start_ind + len(web_type):end_ind]
        elif web_type == self.curse_addon_locator:
            start_ind = content.find(web_type) + len(web_type)
            end_ind = content.find("<", start_ind)
            version = content[start_ind:end_ind]
        else:
            start_ind = content.find(web_type, start_ind + 1)
            end_ind = content.find(">", start_ind)
            version = content[start_ind + len(web_type):end_ind].strip("\"")

        logging.info("Version: {0}".format(version))

        return version

    def get_name(self):
        url = self.url

        if url.__contains__('/files'):
            if not url.endswith('/files'):
                logging.critical("Bad URL.")
                return False

        if url.__contains__('tukui'):
            logging.info("URL from tukui found.")
            name = url[url.rfind("=") + 1:].title()
            logging.debug("Name: {0}".format(name))

            return name

        web_type = self.get_version_index(self.get_website_type())

        if web_type is None:
            return False
        else:
            uri = '/files'

        try:
            page = requests.get(self.url + uri)
        except requests.exceptions.ConnectionError as ce:
            logging.critical(ce)
            return False

        content = str(page.content)
        logging.debug("Content of page: {0}".format(content))

        start_ind = content.find(web_type) + len(web_type) + 1
        end_ind = content.find("\"", start_ind)
        name = content[start_ind:end_ind]

        logging.debug("Name: {0}".format(name))

        return name

    def get_website_type(self):
        if 'wow.curseforge.com/projects' in self.url:
            return 'curse-projects'
        elif 'www.curseforge.com/wow/addons' in self.url:
            return 'curse-addons'
        elif 'mods.curse.com/addons/wow' in self.url:
            return 'curse-addons'
        elif 'wowinterface' in self.url:
            return ''
        elif 'tukui.org' in self.url:
            return 'tukui'
        else:
            logging.critical("Could not determine website type.")
            return None

    def check_for_valid_url(self):
        urls_to_check = ["wow.curseforge.com/projects", "www.curseforge.com/wow/addons",
                         "tukui.org/"]
        return any(ext in self.url for ext in urls_to_check)


if __name__ == '__main__':
    # a = Addon(url="https://wow.curseforge.com/projects/deadly-boss-mods")
    a = Addon(url="https://www.tukui.org/download.php?ui=elvui")
    # a = Addon(url="http://www.google.com")
    a.get_name()

    #
    # print("modified addon: {0}".format(a.url))
    # if not a.valid_url:
    #     a.get_name()
    #     a.get_update_version()
    #


