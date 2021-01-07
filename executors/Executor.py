from abc import ABCMeta, abstractmethod

from infrastructure.Logger import Logger
from models.Action import Action
from models.Step import Step


class Executor(metaclass = ABCMeta):

    def __init__(self):
        self._logger = Logger()

    @abstractmethod
    def execute(self, step:Step, action:Action):
        pass
