from executors.Executor import Executor
from helpers.FileHelper import FileHelper
from models.Action import Action
from models.Step import Step

class FileExecutor(Executor):

    filehelper = FileHelper()

    def execute(self, step:Step, action:Action):
        operation = action.get('operation')
        pathbase = f'{step.path}/'
        src = action.get('src')
        fullpath = f'{pathbase}/{src}'

        if operation == 'copy':
            dst = action.get('dst')
            self.filehelper.copy(pathbase, src, dst)
        if operation == 'replace_value':
            oldvalue = action.get('oldvalue')
            newvalue = action.get('newvalue')
            self.filehelper.replace_value(f'{pathbase}/{src}', oldvalue, newvalue)
        if operation == 'search_and_replace':
            extension = action.get('extension')
            oldvalue = action.get('oldvalue')
            newvalue = action.get('newvalue')
            for file in self.filehelper.searchFiles(f'{pathbase}{src}', [extension]):
                self.filehelper.replace_value(file, oldvalue, newvalue)
        if operation == 'rename':
            oldvalue = action.get('oldvalue')
            newvalue = action.get('newvalue')
            self.filehelper.rename(f'{fullpath}/{oldvalue}', f'{fullpath}/{newvalue}')
