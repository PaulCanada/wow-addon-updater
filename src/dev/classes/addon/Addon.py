import requests
import requests.exceptions
import logging


logging.basicConfig(level=logging.DEBUG)


class Addon(object):

    curse_project_locator = 'data-name='
    curse_addon_locator = 'file__name full">'
    wow_ace_locator = ''
    tukui_locator = 'downloads/'

    def __init__(self, url='', name='', current_version='', latest_version=''):
        self.url = url
        self.name = name
        self.current_version = current_version
        self.latest_version = latest_version
        self.addon_source = ''

        self.valid_url = self.check_for_valid_url()

        if self.valid_url and self.name == '':
            self.name = self.get_name()

            if self.name is False:
                self.valid_url = False

            if self.latest_version == '':
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

        return {
            self.curse_addon_locator: self.get_curse_addons_ver(content),
            self.curse_project_locator: self.get_curse_projects_ver(content),
            self.tukui_locator: self.get_tukui_ver(content)
        }.get(web_type, None)
        #
        # # If downloading from Tukui
        # if web_type == self.tukui_locator:
        #     self.get_tukui_ver()
        # # If downloading from Curse Addons
        # elif web_type == self.curse_addon_locator:
        #     self.get_curse_addons_ver(content)
        # # If downloading from Curse Projects (this seems to be the standard)
        # elif web_type == self.curse_project_locator:
        #     self.get_curse_projects_ver(content)
        # else:
        #     logging.critical("Invalid web_type given: {0}".format(web_type))
        #     return None
        #
        # logging.info("Version: {0}".format(version))
        #
        # return version

    def get_curse_addons_ver(self, content):
        start_ind = content.find(self.curse_addon_locator) + len(self.curse_addon_locator)
        end_ind = content.find("<", start_ind)
        version = content[start_ind:end_ind]

        return version

    def get_curse_projects_ver(self, content):
        start_ind = content.find(self.curse_project_locator, content.find('project-file-list-item'))
        end_ind = content.find(">", start_ind)
        version = content[start_ind + len(self.curse_project_locator):end_ind].strip("\"")

        return version

    def get_tukui_ver(self, content):
        start_ind = content.find(self.tukui_locator)
        end_ind = content.find(".zip", start_ind + len(self.tukui_locator))
        version = content[start_ind + len(self.tukui_locator):end_ind]

        return version

    def get_wow_ace_ver(self, content):
        pass

    def get_name(self):
        url = self.url
        uri = '/files'

        if url.__contains__('/files'):
            if not url.endswith('/files'):
                logging.critical("Bad URL.")
                return False

        if url.__contains__('tukui'):
            logging.info("URL from tukui found.")
            name = url[url.rfind("=") + 1:].title()
            logging.debug("Name: {0}".format(name))

            return name

        elif url.__contains__("wow/addons/"):
            web_type = '"og:title" content="'
            ending_pattern = '" />\\r\\n<meta'
        else:
            web_type = '<span class="overflow-tip">'
            ending_pattern = '</span></a>\\r\\n'

        try:
            page = requests.get(self.url + uri)
        except requests.exceptions.ConnectionError as ce:
            logging.critical(ce)
            return False

        content = str(page.content)
        logging.debug("Content of page: {0}".format(content))

        start_ind = content.find(web_type) + len(web_type)
        end_ind = content.find(ending_pattern, start_ind)
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
            return None
        elif 'tukui.org' in self.url:
            return 'tukui'
        elif 'wowace.com' in self.url:
            return 'wow-ace'
        else:
            logging.critical("Could not determine website type.")
            return None

    def check_for_valid_url(self):
        urls_to_check = ["wow.curseforge.com/projects", "www.curseforge.com/wow/addons",
                         "tukui.org/"]
        return any(ext in self.url for ext in urls_to_check)


if __name__ == '__main__':
    # a = Addon(url="https://wow.curseforge.com/projects/deadly-boss-mods")
    a = Addon(url="https://www.curseforge.com/wow/addons/pettracker")
    # a = Addon(url="http://www.google.com")
    a.get_name()
# https://www.wowace.com/projects/silver-dragon
    #
    # print("modified addon: {0}".format(a.url))
    # if not a.valid_url:
    #     a.get_name()
    #     a.get_update_version()
    #


