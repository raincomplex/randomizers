import re, glob, importlib, inspect
import pure

modulenames = glob.glob('randos/*.py')
modulenames = [re.sub(r'randos/(.*)\.py$', lambda m: m.group(1), n) for n in modulenames]

modules = {}
for m in modulenames:
    modules[m] = importlib.import_module('randos.' + m)

def setupobj(m, r):
    if r.__name__.endswith('_pure'):
        r = pure.Factory(r)

    r.name = r.__name__
    r.desc = (r.__doc__ or '').strip()
    if m.__doc__:
        r.desc = m.__doc__.strip() + ('\n\n' + r.desc if r.desc else '')

    r.modname = m.__name__.split('.')[-1]

    c = r
    if hasattr(c, 'getfunc'):
        c = c.getfunc()
    lines, start = inspect.getsourcelines(c)
    r.lineno = start

    return r

rands = {}
for name, m in sorted(modules.items()):
    found = 0
    for rname in dir(m):
        if rname.startswith(name) and re.match(r'\d*(_|$)', rname[len(name):]):
            obj = getattr(m, rname)
            obj = setupobj(m, obj)
            rands[rname] = obj
            found += 1
    if found == 0:
        print('found no randomizers in module:', name)
