from PyQt5.QtCore import QThread


class Worker(QThread):
    def __init__(self, function, *args, **kwargs):
        super(QThread, self).__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.function(*self.args, **self.kwargs)
