import yaml
import pickle
import json
import os
import jsonpickle
from .obj import Obj

class FileIO:
    @staticmethod
    def read_yaml(filename):
        with open(filename,'r') as file:
            return yaml.load(file)

    @staticmethod
    def read_pickle(filename):
        with open(filename,'rb') as file:
            return pickle.load(file)

    @staticmethod
    def read_json(filename, as_obj = False):
        with open(filename,'r') as file:
            result = json.load(file)
            if as_obj:
                return Obj.create(result)
            else:
                return result


    @staticmethod
    def read_text(filename):
        with open(filename,'r') as file:
            return file.read()

    @staticmethod
    def read_jsonpickle(filename):
        with open(filename,'r') as file:
            return jsonpickle.loads(file.read())

    @staticmethod
    def write_yaml(data, filename):
        with open(filename,'w') as file:
            yaml.dump(data,file)

    @staticmethod
    def write_pickle(data, filename):
        with open(filename,'wb') as file:
            pickle.dump(data,file)

    @staticmethod
    def write_json(data, filename):
        with open(filename,'w') as file:
            json.dump(data,file,indent=1)

    @staticmethod
    def write_text(data, filename):
        with open(filename,'w') as file:
            file.write(data)

    @staticmethod
    def write_jsonpickle(data, filename):
        with open(filename,'w') as file:
            file.write(jsonpickle.dumps(data))

    @staticmethod
    def relative_to_file(file, *path):
        return os.path.join(os.path.dirname(file),*path)


    @staticmethod
    def find_root_folder(root_file_name):
        root_path = './'
        for i in range(100):
            if os.path.isfile(root_path + root_file_name):
                return root_path
            root_path += '../'
        raise ValueError(
            "Cound't find the root {1}. The current directory is {0}".format(os.path.abspath('.'), root_file_name))

