from models.Step import Step


class Process:

    path:str = None
    vars: {} = None

    def __init__(self):
        self.steps = {}

    def addStep(self, key:str, step:Step):
        self.steps.setdefault(key, step)

    def getSteps(self):
        return self.steps