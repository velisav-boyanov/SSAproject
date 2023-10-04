from dict_element import DictElement 

class MyDict():
    def __init__(self, first):
        self.first = first
        self.elements = []

    def add_element(self, key, val=None):
        self.elements.append(DictElement(key, val))
        return key

    def get_element(self, key):
        for e in self.elements:
            if e.get_key() == key:
                return e.get_data()
        print("Element was not found.")          
    
    def get_keys(self):
        keys = []
        for e in self.elements:
            keys.append(e.get_key())
        return keys    

    def set_element(self, key, val):
        for e in self.elements:
            if e.get_key() == key:
                e.set_data(val)
                return 0
        print("Element was not found.")

    def pretty(self):
        result = "/"
        for e in self.elements:
            #print(e.get_key)
            result += f"{e.get_key()}::{e.get_data()}/"    
        return result

    def reverse_pretty(self, pretty):
        i = 0
        length = len(pretty)
        key = ""
        val = ""
        while(True):
            if length == i:
                break
            if pretty[i] == "/":
                i += 1
                if len(pretty) <= i: return 0
                while(True):
                    if pretty[i] == ":":
                        i += 2
                        while(True):
                            if pretty[i] != "/":
                                val += pretty[i]
                                i += 1
                            else:
                                break    
                    elif pretty[i] != "/":
                        key += pretty[i]
                        i += 1
                    else:
                        self.add_element(key, val)
                        key = ""
                        val = ""
                        break
            elif pretty[i] == ":":
                i += 2
                if len(pretty) <= i: return 0
                while(True):
                    if pretty[i] != "/":
                        val += pretty[i]
                        i += 1
                    else:
                        print(f"{key},,, {val}")
                        self.set_element(key, val)
                        key = ""
                        val = ""
                        break    

##TN(6):Sample|LN(1):0|EL(50):/Id::int/Name::string/BirthDate::date“01.01.2022”/
##TN(7):Samples|LN(1):0|EL(50):/Id::int/Name::string/BirthDate::date“01.01.2022”/
