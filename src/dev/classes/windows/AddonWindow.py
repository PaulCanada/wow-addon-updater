from src.gui_py.addon_window_gui import Ui_AddonWindow
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
import requests
import requests.exceptions
from src.dev.classes.addon.Addon import Addon
import logging
from src.dev.classes.workers.Worker import Worker

supported_sites = ['curse-projects', 'curse-addons', 'tukui']


class AddonWindow(QDialog):


    def __init__(self, settings, parent):
        super(QDialog, self).__init__()
        self.worker = Worker(self.add)

        self.window = QDialog()
        self.window.ui = Ui_AddonWindow()
        self.window.ui.setupUi(self)
        self.window.ui.buttonBox.accepted.connect(self.worker.start)
        self.window.ui.buttonBox.rejected.connect(self.close)

        self.window.ui.buttonBox.button(QDialogButtonBox.Ok).setText("Add")

        self.settings = settings
        self.parent = parent

    def add(self):
        print(self.window.ui.leditAddonUrl.text())
        self.settings.load_config()
        self.window.ui.buttonBox.setDisabled(True)

        try:
            response = requests.get(self.window.ui.leditAddonUrl.text())

            logging.debug(response)

            if not response:
                logging.critical("Did not get back a 200 OK response.")
                self.window.ui.buttonBox.setEnabled(True)
                self.parent.MessageBox.emit("Invalid URL", "Cannot reach requested URL: {0}".format(
                    self.window.ui.leditAddonUrl.text()), 'critical')
                return False

        except requests.exceptions.MissingSchema as e:
            logging.critical(e)
            self.parent.MessageBox.emit("Invalid URL: missing scehma.", "URL is missing 'http://' or 'https://'.",
                                        'critical')
            self.window.ui.buttonBox.setEnabled(True)
            return False
        except (requests.exceptions.InvalidSchema, requests.exceptions.InvalidURL) as ie:
            logging.critical(ie)
            self.parent.MessageBox.emit("Invalid URL: invalid schema.", "Bad URL request.", 'critical')
            self.window.ui.buttonBox.setEnabled(True)
            return False
        except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout) as ce:
            logging.critical(ce)
            self.parent.MessageBox.emit("Invalid URL", "Cannot reach requested URL: {0}".format(
                self.window.ui.leditAddonUrl.text()), 'critical')
            self.window.ui.buttonBox.setEnabled(True)
            return False

        current_addon = Addon(url=self.window.ui.leditAddonUrl.text(), current_version="Unknown")
        logging.debug("Current addon source: {0}".format(current_addon.addon_source))

        if current_addon.addon_source not in supported_sites:
            self.parent.MessageBox.emit("Host not supported",
                                 "Downloading files from {0} is not currently supported.".format(current_addon.url),
                                 "warn")
            current_addon.valid_url = -1
            self.window.ui.buttonBox.setEnabled(True)
            return False

        if current_addon.valid_url is False:
            self.parent.MessageBox.emit("Invalid URL",
                                 "Invalid WoW Addon URL. If you think this is a mistake, contact developer.",
                                 'critical')
            self.window.ui.buttonBox.setEnabled(True)
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
            self.parent.MessageBox.emit("Addon already added", "Cannot add this AddOn. This addon is already in your "
                                                        "AddOns list.", 'warn')
            self.window.ui.buttonBox.setEnabled(True)
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

            self.parent.MessageBox.emit("Addon information added.", "", 'inform')
            self.window.ui.leditAddonUrl.setText("")

            # Save and load the config.
            self.settings.save_config()
            self.settings.load_config()
            self.parent.AddAddon.emit(current_addon, self.parent.window.ui.tviewAddons, self.parent.model)
            self.window.ui.buttonBox.setEnabled(True)
            return True

    def check_if_addon_in_config(self, addon):
        if addon.name in self.settings.data['addons']:
            return True
        else:
            return False
