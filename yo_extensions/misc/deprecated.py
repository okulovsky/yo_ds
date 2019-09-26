
import os
import json
import pickle
from yo_fluq_ds._misc.io import FileIO as IO
from yo_ds import *



def find_root_folder(root_file_name):
    root_path = './'
    for i in range(10):
        if os.path.isfile(root_path+root_file_name):
            return root_path
        root_path+='../'
    raise ValueError("Cound't find the root {1}. The current directory is {0}".format(os.path.abspath('.'), root_file_name))

def load_json(filename, as_obj=False):
    result = None
    with open(filename) as file:
        result = json.load(file)
    if as_obj:
        result = Obj.create(result)
    return result

def save_json(filename, obj):
    with open(filename,'w') as file:
        json.dump(obj,file,indent=1)

def load_pkl(filename):
    with open(filename,'rb') as file:
        return pickle.load(file)


def save_pkl(filename, obj):
    with open(filename,'wb') as file:
        pickle.dump(obj,file)

