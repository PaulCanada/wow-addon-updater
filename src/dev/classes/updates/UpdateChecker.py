from src.dev.classes.addon.Addon import Addon
import logging


class UpdateChecker(object):

    def __init__(self, parent):
        self.parent = parent

    def check_for_updates(self):
        update_list = []
        current_update_val = 1
        max_update_val = len(self.parent.settings.data['addons'])

        # self.parent.UpdateProgressBarValue.emit(0)
        # self.parent.UpdateProgressBarMax.emit(len(self.parent.settings.data['addons']))
        # self.parent.window.ui.progressBar.setVisible(True)
        self.parent.SetUpdateCount.emit(current_update_val, max_update_val)

        for key in self.parent.settings.data['addons']:
            current_addon = Addon(url=self.parent.settings.data['addons'][key]['url'],
                                  name=self.parent.settings.data['addons'][key]['name'],
                                  current_version=self.parent.settings.data['addons'][key]['current_version'])

            print("Current ver: {0}".format(current_addon.current_version))
            print("Latest ver: {0}".format(current_addon.latest_version))
            print("Name: {0}".format(current_addon.name))

            logging.info("Retrieving latest version for addon: {0}".format(current_addon.name))
            current_addon.latest_version = current_addon.get_update_version()

            if current_addon.current_version != current_addon.latest_version:
                logging.info("{0} is out of date!".format(self.parent.settings.data['addons'][key]['name']))
                update_list.append(current_addon)

                self.parent.settings.data['addons'][key]['latest_version'] = current_addon.latest_version
                self.parent.settings.save_config()
                self.parent.settings.load_config()

            else:
                logging.info("{0} is up to date.".format(self.parent.settings.data['addons'][key]['name']))
            current_update_val += 1

            # self.parent.UpdateProgressBarValue.emit(self.parent.window.ui.progressBar.value() + 1)
            self.parent.SetUpdateCount.emit(current_update_val, max_update_val)

        self.parent.settings.files_to_update = update_list
        return update_list
