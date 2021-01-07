from factories.ExecutorFactory import ExecutorFactory
from loaders.ConfigurationLoader import ConfigurationLoader
from processors.MainProcessor import MainProcessor

def main():
    runprocessor()

def runprocessor():
    loader = ConfigurationLoader({'path': 'resources/config.xml'}, 'reading configuration')
    processor = MainProcessor(ExecutorFactory(), loader.load())
    processor.run()

if __name__ == '__main__':
    main();