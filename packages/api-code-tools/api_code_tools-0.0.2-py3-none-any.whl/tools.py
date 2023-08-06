from sqlitedict import SqliteDict
import random
import subprocess
import re

class sql():
    def __init__(self, param):
        self.param = param

def save(key, value, cache_file="sql/cache.sqlite3"):
    try:
        with SqliteDict(cache_file) as mydict:
            mydict[key] = value # Using dict[key] to store
            mydict.commit() # Need to commit() to actually flush the data
    except Exception as ex:
        #print("Error during storing data (Possibly unsupported):", ex, cache_file)
        pass
def load(key, cache_file="sql/cache.sqlite3"):
    try:
        with SqliteDict(cache_file) as mydict:
            value = mydict[key] # No need to use commit(), since we are only loading data!
        return value
    except Exception as ex:
        #print("Error during loading data:", ex, cache_file)
        pass

def put(var, value, cache_file="sql/cache.sqlite3"):
    sqlite = sql(value)
    save(var, sqlite, cache_file=cache_file)

def get(var, cache_file="sql/cache.sqlite3"):
    try:
        obj2 = load(var, cache_file)
        return obj2.param
    except:
        return 0

def randtext(num):
    arr = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    randtext = ''
    for i in range(num):
        randtext += str(arr[random.randint(0, len(arr) - 1)])
    return randtext


def file_put(filename,data):
    f = open(filename, "w")
    f.write(data)
    f.close()

def file_append(filename,data):
    f = open(filename, "a")
    f.write(data)
    f.close()


def get_int(st):
    num = re.findall(r'\d+', st) 
    return ''.join(num)

  
def read(filename):
    f = open(filename, "r")
    return f.read()

    
def send_command(cmd1, cmd2='not', cmd3='not', cmd4='not', cmd5='not', cmd6='not', cmd7='not'):
    command = 'python3 sign.py '+ cmd1 + ' ' + cmd2 + ' ' + cmd3 + ' ' + cmd4 + ' ' + cmd5 + ' ' + cmd6 + ' ' + cmd7
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, universal_newlines=True).communicate()[0]

def cmd(cmd1, cmd2='not', cmd3='not', cmd4='not', cmd5='not', cmd6='not', cmd7='not'):
    command = cmd1 + ' ' + cmd2 + ' ' + cmd3 + ' ' + cmd4 + ' ' + cmd5 + ' ' + cmd6 + ' ' + cmd7
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, universal_newlines=True).communicate()[0]

def is_int(num):
    try:
        int(num)
        return True
    except:
        return False


def send_shell(*argv):
    subprocess.Popen(argv)


