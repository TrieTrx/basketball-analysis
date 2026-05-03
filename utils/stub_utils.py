import pickle
import os

def save_stub(obj, output_path) :
    if output_path is None :
        return
    if not os.path.exists(os.path.dirname(output_path)) :
        os.mkdir(os.path.dirname(output_path))
    with open(output_path, 'wb') as file :
        pickle.dump(obj, file)

def read_stub(read_from_stub, input_path) :
    if read_from_stub and input_path is not None and os.path.exists(input_path):
        with open(input_path, 'rb') as file :
            return pickle.load(file)
    return None