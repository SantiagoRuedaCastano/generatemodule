from models.Action import Action
from models.Option import Option


class Step(Option):

    path:str = None
    module:str = None

    def __init__(self, order:str, package:str, type:str):
        super().__init__()
        self.order = order
        self.package = package
        self.type = type
        self.actions = list()

    def addAction(self, action:Action):
        self.actions.append(action)

    def getActions(self):
        return self.actions

    def __str__(self):
        return f'\nStep Order:{self.order} Package:{self.package} type:{self.type} options: {self.options}'