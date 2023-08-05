import os
import pickle
import shutil

# Path Manager
class PathManager:
    def __init__(self, path, mode='binary', save=True):
        self.path = path
        self.mode = mode
        self.save = save
        # Make sure path exists
        if not os.path.exists(path):
            os.mkdir(path)
    def __setitem__(self, name, value) -> None:
        name = str(name)
        if self.mode == 'binary':
            with open(os.path.join(self.path, name), 'wb') as f:
                pickle.dump(value, f)
        else:
            with open(os.path.join(self.path, name), 'w') as f:
                f.write(value)
    def __getitem__(self, name):
        name = str(name)
        # if file exists return sub manager
        subpath = os.path.join(self.path, name)
        if os.path.isfile(subpath):
            if self.mode == 'binary':
                with open(subpath, 'rb') as f:
                    return pickle.load(f)
            else:
                with open(subpath, 'r') as f:
                    return f.read()
        else:
            # Create sub manager with path of current path + name or create new folder and return sub manager
            if not os.path.exists(subpath):
                os.mkdir(subpath)
            return PathManager(subpath)
    def __delitem__(self, name):
        os.remove(os.path.join(self.path, name))
    def __contains__(self, name):
        return os.listdir(self.path)
    def __iter__(self):
        return iter(os.listdir(self.path))
    def __len__(self):
        return len(os.listdir(self.path))
    def __str__(self):
        return str(os.listdir(self.path))
    def __repr__(self):
        return str(os.listdir(self.path))
    def __del__(self):
        shutil.rmtree(self.path) if not self.save else None