from src.gui_py.addon_window_gui import Ui_Form
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal
import requests
import requests.exceptions
from src.dev.classes.addon.Addon import Addon
import logging
from src.dev.classes.workers.Worker import Worker

supported_sites = ['curse-projects', 'curse-addons', 'tukui']


class AddonWindow(QDialog):

    MessageBox = pyqtSignal(str, str, str)

    def __init__(self, settings, parent):
        super(QDialog, self).__init__()
        self.worker = Worker(self.add)

        self.window = QDialog()
        self.window.ui = Ui_Form()
        self.window.ui.setupUi(self)
        self.window.ui.buttonBox.accepted.connect(self.worker.start)
        self.window.ui.buttonBox.rejected.connect(self.close)
        self.MessageBox.connect(self.show_message_box)

        self.settings = settings
        self.parent = parent

    def add(self):
        print(self.window.ui.leditAddonUrl.text())
        self.settings.load_config()
        try:
            response = requests.get(self.window.ui.leditAddonUrl.text())

            logging.debug(response)

            if not response:
                logging.critical("Did not get back a 200 OK response.")
                return False

        except requests.exceptions.MissingSchema as e:
            logging.critical(e)
            self.MessageBox.emit("Invalid URL: missing scehma.", "URL is missing 'http' or 'https'.", 'critical')
            return False
        except requests.exceptions.InvalidSchema as ie:
            logging.critical(ie)
            self.MessageBox.emit("Invalid URL: invalid schema.", "Bad URL request.", 'critical')
            return False
        except requests.exceptions.ConnectionError as ce:
            logging.critical(ce)
            self.MessageBox.emit("Invalid URL", "Cannot reach requested URL: {0}".format(
                self.window.ui.leditAddonUrl.text(), 'critical'))
            return False

        current_addon = Addon(url=self.window.ui.leditAddonUrl.text(), current_version="Unknown")
        current_addon.name = current_addon.name.replace(":", "")
        logging.debug("Current addon source: {0}".format(current_addon.addon_source))
        if current_addon.addon_source not in supported_sites:
            self.MessageBox.emit("Host not supported",
                                 "Downloading files from {0} is not currently supported.".format(current_addon.url),
                                 "warn")
            current_addon.valid_url = -1

        if current_addon.valid_url == -1:
            return False
        elif current_addon.valid_url is False:
            self.MessageBox.emit("Invalid URL",
                                 "Invalid WoW Addon URL. If you think this is a mistake, contact developer.",
                                 'critical')
            return False
        else:
            logging.debug("Valid URL.")

        logging.debug("Addon URL: {0}\nAddon name: {1}\nAddon version: {2}".format(current_addon.url,
                                                                                   current_addon.name,
                                                                                   current_addon.latest_version))

        logging.info("Checking if addon: {0} is already in config.".format(current_addon.name))
        exists = self.check_if_addon_in_config(current_addon)
        logging.info("Addon exists: {0}".format(exists))

        if exists:
            self.MessageBox.emit("Addon already added", "This addon is already in your addons list.", 'warn')
            return False
        else:
            logging.debug("Addon is not in list. Adding addon: {0}".format(current_addon.name))
            addon_dict = {'name': current_addon.name,
                          'url': current_addon.url,
                          'current_version': 'Unknown',
                          'latest_version': current_addon.latest_version}

            self.settings.write_addon_info('addons', current_addon.name, addon_dict)
            self.settings.save_config()
            self.settings.load_config()

            self.MessageBox.emit("Addon information added.", "", 'inform')
            self.window.ui.leditAddonUrl.setText("")

            # Save and load the config.
            self.settings.save_config()
            self.settings.load_config()
            self.parent.AddAddon.emit(current_addon, self.parent.window.ui.tviewAddons, self.parent.model)
            return True

    def check_if_addon_in_config(self, addon):
        if addon.name in self.settings.data['addons']:
            return True
        else:
            return False

    @pyqtSlot(str, str, str)
    def show_message_box(self, message='', inform='', message_type='warn'):
        message_box = QMessageBox()

        if message_type == 'inform':
            message_box.setIcon(QMessageBox.Information)
        elif message_type == 'warn':
            message_box.setIcon(QMessageBox.Warning)
        else:
            message_box.setIcon(QMessageBox.Critical)

        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.setText(message)
        message_box.setInformativeText(inform)
        message_box.exec()
