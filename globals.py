

class Globals():
    global_vars = dict()
    
    @staticmethod
    def add(key, value):
        Globals.global_vars[key] = value
    
    @staticmethod
    def get(key):
        if key in Globals.global_vars:
            return Globals.global_vars[key]
        
        raise ValueError('No global for that key %s', key)