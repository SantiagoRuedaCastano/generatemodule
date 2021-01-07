from infrastructure.Logger import Logger
from models.Option import Option


class Action(Option):

    parameters = {}

    def __init__(self, order):
        super().__init__()
        self.order = order
        self.logger = Logger()

    def __str__(self):
        return f'Action Order:{self.order} options: {self.options}'

    def get(self, key:str):
        value:str = self.getOptions().get(key)
        if value == None:
            return value
        return self.searchPattern(value)

    def searchPattern(self, string:str):
        start = string.find("${")
        if start >= 0:
            end = string.find("}", start)
            toFind = string[start + 2:end]
            if self.parameters.get(toFind) == None:
                self.logger.log(f"Var is not defined: {toFind}")
            newstring = string.replace(f"${{{toFind}}}", f"{self.parameters.get(toFind)}")
            return self.searchPattern(newstring)
        return string


    def addParameters(self, dict):
        self.parameters = dict