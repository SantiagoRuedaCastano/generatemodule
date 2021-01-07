import xml.etree.ElementTree as ET

from infrastructure.Logger import Logger
from models.Action import Action
from models.Process import Process
from models.Step import Step


class ConfigurationLoader:

    logger = Logger()

    def __init__(self, action:{str, str}, message=''):
        self.logger.log(message)
        self.process = Process()
        self.path = action['path']

    def load(self):
        self.__readConfigurationFile(self.path)
        return self.process

    def formatArgs(self, vars:str):
        dict = {}
        varslst = vars.split(";")
        for var in varslst:
            keyvalue = var.split('=')
            dict.setdefault(keyvalue[0], keyvalue[1])
        return dict

    def __readConfigurationFile(self, path):
        root = ET.parse(path).getroot()
        for element in root.findall('process'):
            project = element.attrib
            self.process.path = project.get('path')
            self.process.vars = self.formatArgs(project.get('args'))

        # iterate over child nodes
        for element in root.findall('step'):
            step = self.__getStep(element)

            actions = element.findall('action')
            for elementchild in actions:
                step.addAction(self.__getAction(elementchild))
            self.process.addStep(step.order, step)


    def __getAction(self, element):
        attributes = element.attrib
        order = attributes.get('order')
        action = Action(order)
        for attribute in attributes:
            action.addOption(attribute, attributes.get(attribute))
        return action

    def __getStep(self, element):
        attributes = element.attrib
        order = attributes.get('order')
        package = attributes.get('package')
        type = attributes.get('type')
        step = Step(order, package, type)
        for attribute in attributes:
            step.addOption(attribute, attributes.get(attribute))
        return step