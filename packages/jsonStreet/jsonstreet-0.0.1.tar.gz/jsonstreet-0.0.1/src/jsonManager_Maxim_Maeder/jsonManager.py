from pprint import pprint
from json import loads as jsonLoad
from json import dumps as jsonDump
from os.path import exists as pathExists

class jsonManager():
    def __init__(self, startingData) -> None:
        
        if pathExists(str(startingData)):
            self.open(startingData)
        else:
            self.data = startingData

        self.defaults = {
            'hey': 191092,
        }
        




    def get(self, path, default=None):
        string = self.buildPath(path)
        returnValue = eval(string)

        if not returnValue and default != None:
            self.set(path, default)
            return default

        return returnValue

    def set(self, path, value):
        string = self.buildPath(path)

        if isinstance(value, str):
            value = f'"{value}"'

        exec(f'{string} = {value}')




    def buildPath(self, path):
        string = ''
        for i in path.split('/'):
            if i.isnumeric():
                string += f'[{i}]'
                self.checkSave(string, 'list')
            else:
                string += f'["{i}"]'
                self.checkSave(string, 'dict')

        string = 'self.data'+string

        return string

    def checkSave(self, path, type):
        try:
            eval('self.data'+path)
        except:

            try:
                l = eval(f'self.defaults{path}')
                exec('self.data'+path+f' = {l}')
            except:
                if type == 'list':

                    exec('self.data'+path+' = []')
                else:
                    exec('self.data'+path+' = {}')


    def open(self, path):
        with open(path, 'r') as f:
            self.data = jsonLoad(f.read())


    def save(self, path):
        with open(path, 'w') as f:
            f.write(jsonDump(self.data))


    def log(self, string=None):
        if string:
            print(string)
        else:
            pprint(self.data)

m = jsonManager({
    'fas': ['fasdf'],
    'fasf': 10,
})


m.open('jsonjson_v2.json')
m.log()
print(m.get('hey'))
m.log()