from executors.Executor import Executor
from helpers.DirectoryHelper import DirectoryHelper
from models.Action import Action
from models.Step import Step


class DirectoryExecutor(Executor):

    def __init__(self):
        self.directory = DirectoryHelper()

    def execute(self, step:Step, action:Action):
        super().__init__()
        pathbase = f'{step.path}/'
        path = action.get('path')
        operation = action.get('operation')
        if path == None:
            self._logger.log(f'there is not a valid key \"{path}\" for this action: {action}')
            return

        if operation == 'create':
            self.directory.create(f'{pathbase}/')
            self.directory.create(f'{pathbase}/{path}')

        if operation == 'delete':
            self.directory.delete(f'{pathbase}{path}')



