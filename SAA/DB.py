from table import Table
import os
import time
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

dbfilename = "bruhdb"
n = 0
q = 0
elements = []

def read_input(command, stop, second_stop=""):
    data = ""
    global n
    k = n
    for c in command[k:]:
        n += 1
        if c != stop and c != second_stop:
            if c != " ": 
                data += c 
        else:
            return data 
    return data        

def print_tables():
    global n
    n = 0
    res = os.getxattr(dbfilename, 'user.tables').decode('ascii')
    res = res[:-1]
    return print(res)

def read_element(element, stop):
    data = ""
    global q
    k = q
    for c in element[k:]:
        q += 1
        if c != stop:
            data += c 
        else:
            return data
    return data

while(True):
    command = input('Input comand:')

    command_name = read_input(command, " ")
    if command_name == "CreateTable":
        table_name = read_input(command, "(")
        while(True):
            l = read_input(command, ",", ")")
            if l == "":
                break

            name = read_element(l, ":")
            if "default" in l:
                l = l.replace("default", "")

            ctype = read_element(l, "")    
            q = 0
            elements.append((name, ctype))

        table = Table(table_name)
        table.add_line(elements)
        table.table_to_file(dbfilename)

        elements = []
        n = 0
        tables_count = os.getxattr(dbfilename, 'user.tables')
        table_name += ","
        os.setxattr(dbfilename, 'user.tables', tables_count+table_name.encode('ascii'))

    elif command_name == "DropTable":
        table_name = read_input(command, "")
        table = Table(table_name)
        table.file_to_table(dbfilename)
        element_count = len(table.lines)
        n = 0
        print(element_count)
        if element_count == 0:
            print("No such table.")
        else:
            for i in range(0, element_count):
                table.remove_line(i, dbfilename)
                tables_count = os.getxattr(dbfilename, 'user.tables').decode('ascii')
                tables_count = tables_count.replace((table_name+","), "")
                os.setxattr(dbfilename, 'user.tables', tables_count.encode('ascii'))
                   

    elif command_name.__eq__("ListTables"): print_tables()

    elif command_name == "TableInfo": 
        table_name = read_input(command, "")
        table = Table(table_name)
        table.file_to_table(dbfilename)
        n = 0
        print(f"Name {table.name}, Size({table.size}), Number of lines({len(table.lines)}), Schema:{table.get_line(0)}")   

    elif command_name == "Insert":
        keys = []
        vals = []
        command_name = read_input(command, " ")
        table_name = read_input(command, " ")
        n+=1
        while(True):
            key = read_input(command, ",", ")")
            if "VALUES" in key:
                key = key.replace("VALUES", "")
                n-=len(key)
                break
            else:
                keys.append(key)

        while(True):
            val = read_input(command, ",", ")")
            if val == "":
                break
            else:
                vals.append(val)

        table = Table(table_name)
        table.file_to_table(dbfilename)
        table_keys = table.lines[0].elements.get_keys()

        if len(table_keys) == len(keys):
            for i in range(0, len(keys)):
               elements.append((keys[i], vals[i]))
            table.add_line(elements)   
        elif len(table_keys) < len(keys):
            print("Too many atrs.")
        else:
            missing = len(table_keys)-len(keys)
            for i in range(0, len(table_keys)):
                if i <= missing:
                    if table_keys[i]==keys[i]:
                        elements.append((keys[i], vals[i]))
                    else:
                        keys.remove(table_keys[i])
                        keys.insert(i, table_keys[i])
                else:
                    keys.append(table_keys[i])
                    val = table.lines[0].elements.get_element(table_keys[i])
                    val = val.replace("int", "")
                    val = val.replace("string", "")
                    val = val.replace("date", "")
                    vals.append(val)
                    elements.append((keys[i], vals[i]))

        table.add_line(elements)
        table.table_to_file(dbfilename)                           

    elif command_name == "StopDB":
        break

    else:
        n = 0    
#CreateTable Kiro(Id:int, Name:string, SecondName:string default "Kirov", BirthDate:date default “01.05.2025”)
#CreateTable Sample(Id:int, Name:string, BirthDate:date default “01.01.2022”)
#CreateTable Samples(Id:int, Name:string, BirthDate:date default “01.07.2023”)
#CreateTable Sampled(Id:int, Name:string, BirthDate:date default “01.01.2022”)
#Insert INTO Sampled (Id, Name) VALUES (1, “Иван”)
#TN(4):Kiro|LN(1):0|EL(76):/Id::int/Name::string/SecondName::string"Kirov"/BirthDate::date“01.05.2025”/