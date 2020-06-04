from collections import deque

#TODO reference to Neuron objects
class Synapse:
    def __init__(self, **kwargs):
        self.head = kwargs.get("source", "")
        self.tail = kwargs.get("target", "")
        self.number = kwargs.get("number", 1)
        self.type = kwargs.get("type", "")
        self.frequency = kwargs.get("frequency", 1)
        self.values = deque()
        self.next_values = deque()
        self.distribution = []
        self.thresholds = []
        # TODO how to initialize?
        for i in range(int(self.number)):
            self.thresholds.append(0)

    def set_frequency(self):
        self.frequency = 1
        if self.type == "CS":
            self.frequency = 2

    def calc_new_value(self, value):
        if len(self.distribution) != 0:
            pass
        # uniform distribution of value between axons
        else:
            return sum((value for threshold in self.thresholds if value >= threshold)) \
                   / self.number
