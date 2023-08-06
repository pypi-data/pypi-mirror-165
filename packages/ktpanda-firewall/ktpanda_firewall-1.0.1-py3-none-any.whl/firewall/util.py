import asyncio

__all__ = ['public', 'update']

class Result(asyncio.Event):
    def __init__(self):
        super().__init__()
        self._result = None

    def set(self, val=None):
        self._result = val
        super().set()

    async def wait(self):
        await super().wait()
        return self._result

def public(globs):
    all = globs['__all__'] = []
    def ret(f):
        all.append(f.__name__ if hasattr(f, '__name__') else f)
        return f
    return ret

def update(globs):
    all = globs['__all__']
    name = globs['__name__']
    for k, v in globs.items():
        if isinstance(v, type):
            if v.__module__ == name and hasattr(v, 'public') and v.public is True:
                all.append(k)
        if k.upper() == k and not k.startswith('_'):
            all.append(k)
            
