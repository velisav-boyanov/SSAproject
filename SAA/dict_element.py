class DictElement(object):

    def __init__(self, key, val):
        self.val = val
        self.key = key

    def get_data(self):
        return self.val

    def set_data(self, val):
        self.val = val
 
    def get_key(self):
        return self.key
 
    def set_key(self, key):
        self.key = key
