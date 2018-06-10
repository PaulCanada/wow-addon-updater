import simplejson
import os
import sys
import logging


class Settings:

    def __init__(self):
        self.data = []
        self.initialize_data()

    def initialize_data(self):
        if not os.path.isdir('./config'):
            os.mkdir('./config')
            logging.info("Creating config directory.")


if __name__ == '__main__':
    s = Settings()
    s.initialize_data()
