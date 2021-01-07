class ExecutorFactory(object):
    def getExecutor(self, package, type):
        eval(f"exec('from {package} import {type}')")
        return eval(type)()