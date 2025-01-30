import os as _os
import importlib as _importlib

#__globals = globals()

#print('Names:')
#print('file:', __file__)
#print('name:', __name__)

#print('\nLoading...')
for file in _os.listdir(_os.path.dirname(__file__)):
    if not file.startswith('_') and file.endswith('.py'):
        mod_name = file[:-3]   # strip .py at the end
        #print(mod_name)
        #__globals[mod_name] = importlib.import_module('.' + mod_name, package=__name__)
        module = _importlib.import_module('.' + mod_name, package=__name__)
        _importlib.reload(module)

# Clean up the namespace
del file
del mod_name
del module
del _os
del _importlib