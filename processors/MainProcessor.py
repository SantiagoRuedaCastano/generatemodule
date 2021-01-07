from factories.ExecutorFactory import ExecutorFactory
from infrastructure.Logger import Logger
from models.Process import Process
from models.Step import Step


class MainProcessor:

    logger = Logger()

    def __init__(self, factory:ExecutorFactory, process:Process):
        self.process = process
        self.factory = factory


    def run(self):
        steps = self.process.getSteps()

        for key in steps.keys():
            step:Step = steps.get(key)
            step.path = self.process.path
            step.module = self.process.vars.get('module')
            self.logger.log(str(step))
            executor = self.factory.getExecutor(step.package, step.type)
            for action in step.getActions():
                action.addParameters(self.process.vars)
                self.logger.log(str(action))
                executor.execute(step, action)
