class Option:

    def __init__(self):
        self.options = {}

    def addOption(self, key:str, value:str):
        self.options.setdefault(key, value)

    def getOptions(self):
        return self.options