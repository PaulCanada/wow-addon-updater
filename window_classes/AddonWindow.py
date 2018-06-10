from gui_py.addon_window_gui import Ui_Form
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal
import requests
import requests.exceptions
from Addon import Addon
import logging


class AddonWindow(QDialog):

    MessageBox = pyqtSignal(str, str, str)

    def __init__(self, settings, parent):
        super(QDialog, self).__init__()

        self.window = QDialog()
        self.window.ui = Ui_Form()
        self.window.ui.setupUi(self)
        self.window.ui.buttonBox.accepted.connect(self.add)
        self.window.ui.buttonBox.rejected.connect(self.close)
        self.MessageBox.connect(self.show_message_box)

        self.settings = settings
        self.parent = parent

    def add(self):
        print(self.window.ui.leditAddonUrl.text())
        try:
            response = requests.get(self.window.ui.leditAddonUrl.text())

            logging.debug(response)

            if not response:
                logging.critical("Did not get back a 200 OK response.")
                return

        except requests.exceptions.MissingSchema as e:
            logging.critical(e)
            self.MessageBox.emit("Invalid URL: missing scehma.", "URL is missing 'http' or 'https'.", 'critical')
            return
        except requests.exceptions.ConnectionError as ce:
            logging.critical(ce)
            self.MessageBox.emit("Invalid URL", "Cannot reach requested URL: {0}".format(
                self.window.ui.leditAddonUrl.text(), 'critical'))
            return

        current_addon = Addon(url=self.window.ui.leditAddonUrl.text())

        if not current_addon.valid_url:
            self.MessageBox.emit("Invalid URL",
                               "Invalid WoW Addon URL. If you think this is a mistake, contact developer.", 'critical')
            return False

        logging.debug("Addon URL: {0}\nAddon name: {1}\nAddon version: {2}".format(current_addon.url,
                                                                                   current_addon.name,
                                                                                   current_addon.latest_version))

        logging.info("Checking if addon: {0} is already in config...".format(current_addon.name))
        exists = self.check_if_addon_in_config(current_addon)

        if exists:
            self.MessageBox.emit("Addon already added", "This addon is already in your addons list.", 'warn')
            return False
        else:
            addon_dict = {'name': current_addon.name.title().replace("-", " ").replace("_", " "),
                          'current_version': 'Unknown',
                          'latest_version': current_addon.latest_version}

            self.settings.write_addon_info(current_addon.name, addon_dict)
            self.settings.save_config()
            self.settings.load_config()

            self.MessageBox.emit("Addon added.", "", 'inform')
            return True

    def check_if_addon_in_config(self, addon):
        if addon.name in self.settings.data['addons']:
            return True
        else:
            return False

    @pyqtSlot(str, str, str)
    def show_message_box(self, message='', inform='', type=QMessageBox.Warning):
        message_box = QMessageBox()
        if type == 'inform':
            message_box.setIcon(QMessageBox.Information)
        elif type == 'warn':
            message_box.setIcon(QMessageBox.Warning)
        else:
            message_box.setIcon(QMessageBox.Critical)

        message_box.setText(message)
        message_box.setInformativeText(inform)
        message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        message_box.exec()
