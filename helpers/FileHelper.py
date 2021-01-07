import os
from shutil import copyfile
from pathlib import Path

class FileHelper:

    def readFile(self, path):
        f = open(path, 'r')
        filedata = f.read()
        f.close()
        return filedata

    def writeFile(self, path, data):
        f = open(path, 'w')
        f.write(data)
        f.close()

    def copy(self, path, src, dst):
        copyfile(src, f'{path}/{dst}')

    def delete(self, path):
        if os.path.exists(path):
            os.remove(path)

    def rename(self, src, dst):
        os.rename(src, dst)

    def replace_value(self, path, oldvalue, newvalue):
        originalFile = path
        tmpFile = f'{path}.tmp'
        dataFile = self.readFile(originalFile)
        newdata = dataFile.replace(oldvalue, newvalue)
        self.writeFile(tmpFile, newdata)
        self.delete(originalFile)
        self.rename(tmpFile, originalFile)

    def searchFiles(self, path, extensions):
        for ext in extensions:
            yield from Path(path).glob(f'**/*.{ext}')