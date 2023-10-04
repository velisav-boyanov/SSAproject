import os
import sys
from dict import MyDict

class Line():
    def __init__(self, table_name, line_number, elements=[], is_first=False):
        self.line_number = line_number
        self.table_name = table_name
        self.elements = MyDict(is_first)
        for e in elements:
            self.elements.add_element(e[0], e[1])

        self.place_in_file = 0

    def line_to_str(self):
        result = f"TN({len(str(self.table_name))}):{self.table_name}|"
        result += f"LN({len(str(self.line_number))}):{self.line_number}|"
        result += f"EL({len(self.elements.pretty())}):{self.elements.pretty()}\n"
        return result

    def get_keys(self):
    	return self.elements.get_keys()	

    def add_to_file(self, file_name):
        line_string = self.line_to_str()
        offsets = self.read_from_file(file_name, True)
        offset = offsets[0]
        if offset == 0:
            offset = os.path.getsize(file_name)

        with open(file_name, "r+") as f:
            if offset != 0: f.read(offset)  
            f.write(line_string)
            self.place_in_file = f.tell()
        return len(line_string)    

    def read_from_file(self, file_name, delete=False):
        skip = 0
        line_string = self.line_to_str()
        length = ""        
        with open(file_name, "r+") as f:
            f.seek(0, 0)
            while(True):
                self.place_in_file = f.tell()
                if os.path.getsize(file_name) == 0: break
                types = f.read(2)
                if types == "TN":
                    f.read(1)
                    while(True):
                        num = f.read(1)
                        if(num.isnumeric()):
                            length += num
                        else:
                            break
                    length = int(length)
                    f.read(1)
                    table_name = f.read(length)
                    length=""
                    #table name
                    f.read(4)
                    while(True):
                        num = f.read(1)
                        if(num.isnumeric()):
                            length += num
                        else:
                            break
                    length = int(length)
                    f.read(1)
                    line_number = f.read(length)
                    #line number
                    f.read(4)
                    length = ""
                    while(True):
                        num = f.read(1)
                        if(num.isnumeric()):
                            length += num
                        else:
                            break	
                    length = int(length)
                    f.read(1)
                    elements_str = f.read(length)
                    length = ""
                    if int(self.line_number) == int(line_number) and (self.table_name == table_name):
                        if delete == True:
                            start = self.rewrite(self.place_in_file-skip, f.tell()-(skip+3), file_name)
                            return (start, 0)
                        else:
                            self.elements.reverse_pretty(elements_str)
                            return (1, len(elements_str))
                    else:
                        skip+=4
                        f.read(1)        
                else:
                    break
        return (0, 0)

    def rewrite(self, start, end, file_name):
        #print(start)
        #print(end)
        with open(file_name, "r") as f:
            before = f.read(start)
            f.read(end-start)
            after = f.read()
            f.close()

        with open(file_name, "w") as f:
            f.write(before)
            f.write(after)
            f.close

        return start

