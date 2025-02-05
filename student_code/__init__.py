import os as _os
import importlib as _importlib

for file in _os.listdir(_os.path.dirname(__file__)):
    if not file.startswith('_') and file.endswith('.py'):
        mod_name = file[:-3]
        try:
            module = _importlib.import_module('.' + mod_name, package=__name__)
            _importlib.reload(module)
        except Exception as e:
            print(f'Error loading {mod_name}:\n {e}')

# Clean up the namespace
del file
del mod_name
del module
del _os
del _importlib