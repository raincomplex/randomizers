import re, glob, importlib

modulenames = glob.glob('randos/*.py')
modulenames = [re.sub(r'randos/(.*)\.py$', lambda m: m.group(1), n) for n in modulenames]

modules = {}
for m in modulenames:
    modules[m] = importlib.import_module('randos.' + m)

rands = {}
for name, m in sorted(modules.items()):
    if hasattr(m, 'factory'):
        rands[name] = m.factory
    elif hasattr(m, 'factory1'):
        i = 1
        while hasattr(m, 'factory' + str(i)):
            f = getattr(m, 'factory' + str(i))
            n = name + '/' + (f.__doc__ or str(i))
            rands[n] = f
            i += 1
    elif hasattr(m, 'Randomizer'):
        rands[name] = m.Randomizer
    else:
        print('module has no factory functions or Randomizer class:', name)
