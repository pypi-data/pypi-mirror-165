from abc import ABCMeta, abstractmethod

class BaseHandler(metaclass=ABCMeta):
    @abstractmethod
    def setLevel(self):
        pass

    @abstractmethod
    def setFormatter(self):
        pass