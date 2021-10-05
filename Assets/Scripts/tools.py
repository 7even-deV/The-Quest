class Timer():

    def __init__(self):
        self.counter = 0

    def time(self, timer, *events):
        self.counter += 1
        if self.counter > timer * 100:
            self.counter = 0
            return events
